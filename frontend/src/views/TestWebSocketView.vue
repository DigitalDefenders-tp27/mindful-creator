<template>
  <div class="websocket-test-container">
    <h1>WebSocket Connection Test</h1>
    
    <div class="connection-panel">
      <div class="url-input">
        <label for="ws-url">WebSocket URL:</label>
        <input 
          id="ws-url" 
          type="text" 
          v-model="wsUrl" 
          placeholder="Enter WebSocket URL, e.g.: wss://gleaming-celebration.railway.internal/ws"
          class="url-input-field"
        />
      </div>
      
      <div class="connection-options">
        <div class="option">
          <input type="checkbox" id="enable-ping" v-model="enablePing">
          <label for="enable-ping">Enable ping messages</label>
        </div>
        <div class="option" v-if="enablePing">
          <label for="ping-interval">Ping interval (ms):</label>
          <input 
            type="number" 
            id="ping-interval" 
            v-model="pingIntervalMs" 
            min="5000" 
            max="60000" 
            step="1000"
          >
        </div>
      </div>
      
      <div class="connection-controls">
        <button 
          @click="connectWebSocket" 
          :disabled="isConnected" 
          class="connect-button"
        >
          Connect
        </button>
        <button 
          @click="disconnectWebSocket" 
          :disabled="!isConnected" 
          class="disconnect-button"
        >
          Disconnect
        </button>
        <button 
          @click="testConnection" 
          :disabled="!isConnected" 
          class="test-button"
        >
          Send Test Message
        </button>
      </div>
    </div>
    
    <div class="connection-status" :class="{ 'connected': isConnected, 'disconnected': !isConnected }">
      <div class="status-indicator"></div>
      <span>{{ connectionStatus }}</span>
    </div>
    
    <div class="message-panel">
      <div class="message-input">
        <input 
          type="text" 
          v-model="messageToSend" 
          placeholder="Enter message to send" 
          :disabled="!isConnected"
          @keyup.enter="sendMessage"
          class="message-input-field"
        />
        <button 
          @click="sendMessage" 
          :disabled="!isConnected || !messageToSend.trim()" 
          class="send-button"
        >
          Send
        </button>
      </div>
      
      <div class="message-log">
        <h3>Message Log</h3>
        <div class="messages-container">
          <div 
            v-for="(message, index) in messages" 
            :key="index" 
            class="message-item"
            :class="{ 'sent': message.type === 'sent', 'received': message.type === 'received', 'error': message.type === 'error', 'info': message.type === 'info' }"
          >
            <div class="message-header">
              <span class="message-type">{{ message.type === 'sent' ? 'Sent' : message.type === 'received' ? 'Received' : message.type === 'error' ? 'Error' : 'Info' }}</span>
              <span class="message-time">{{ message.time }}</span>
            </div>
            <div class="message-content">{{ message.content }}</div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="connection-info">
      <h3>Connection Information</h3>
      <div v-if="connectionError" class="error-box">
        <h4>Connection Error</h4>
        <pre>{{ connectionError }}</pre>
      </div>
      <div class="tips-box">
        <h4>Debugging Tips for Railway WebSockets</h4>
        <ul>
          <li>For Railway deployments, WebSocket URLs should start with <code>wss://</code></li>
          <li>Before connecting, the app checks if the endpoint is available using <code>/ws-test</code></li>
          <li>Ping messages are sent automatically to keep the connection alive</li>
          <li>If you see 1006 errors, check if the backend is properly deployed with WebSocket support</li>
          <li>Enable the "Always On" option in Railway settings to prevent service hibernation</li>
          <li>Check the Railway logs for any backend errors</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onBeforeUnmount, onMounted } from 'vue';
import websocketService from '@/utils/websocket';

// WebSocket connection state
const socket = ref(null);
const isConnected = ref(false);
const connectionError = ref(null);
const messages = ref([]);
const wsUrl = ref('wss://gleaming-celebration.railway.internal/ws');
const messageToSend = ref('');
const enablePing = ref(true);
const pingIntervalMs = ref(20000); // 20 seconds

// Computed property: Connection status text
const connectionStatus = computed(() => {
  if (isConnected.value) {
    return 'Connected';
  } else if (connectionError.value) {
    return 'Connection Failed';
  } else {
    return 'Not Connected';
  }
});

// Add message to the list
function addMessage(content, type = 'info') {
  const now = new Date();
  const timeString = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;
  
  messages.value.push({
    content,
    type,
    time: timeString
  });
  
  // Scroll to bottom
  setTimeout(() => {
    const container = document.querySelector('.messages-container');
    if (container) {
      container.scrollTop = container.scrollHeight;
    }
  }, 50);
}

// Connect to WebSocket using our improved service
function connectWebSocket() {
  // Check connection URL first
  if (!wsUrl.value.trim().startsWith('wss://')) {
    connectionError.value = 'Invalid WebSocket URL. Must start with wss:// in HTTPS environments';
    addMessage('Invalid WebSocket URL format', 'error');
    return;
  }
  
  // Reset status
  isConnected.value = false;
  connectionError.value = null;
  
  // First test if the ws-test endpoint is available
  addMessage(`Testing endpoint availability at ${wsUrl.value.replace('/ws', '/ws-test')}...`, 'info');
  
  fetch(wsUrl.value.replace('wss://', 'https://').replace('/ws', '/ws-test'))
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      addMessage(`WebSocket endpoint test successful: ${JSON.stringify(data)}`, 'info');
      
      // Set up event listeners
      websocketService.on('open', handleWebSocketOpen);
      websocketService.on('message', handleWebSocketMessage);
      websocketService.on('close', handleWebSocketClose);
      websocketService.on('error', handleWebSocketError);
      websocketService.on('maxReconnectAttemptsReached', handleMaxReconnectAttemptsReached);
      
      // Attempt to connect
      addMessage(`Connecting to: ${wsUrl.value}`, 'info');
      
      // Connect with ping options
      websocketService.connect(wsUrl.value, {
        enablePing: enablePing.value,
        pingIntervalMs: parseInt(pingIntervalMs.value)
      });
    })
    .catch(error => {
      connectionError.value = `WebSocket endpoint not available: ${error.message}`;
      addMessage(`WebSocket endpoint test failed: ${error.message}`, 'error');
      addMessage('Make sure the backend is deployed and the WebSocket endpoint is configured correctly', 'error');
    });
}

// WebSocket event handlers
function handleWebSocketOpen() {
  isConnected.value = true;
  addMessage('WebSocket connection established', 'info');
}

function handleWebSocketMessage(data) {
  if (typeof data === 'object') {
    // If it's a ping response, don't show it
    if (data.type === 'pong') return;
    
    addMessage(JSON.stringify(data, null, 2), 'received');
  } else {
    addMessage(data, 'received');
  }
}

function handleWebSocketClose(event) {
  isConnected.value = false;
  addMessage(`WebSocket connection closed: Code=${event.code}, Reason=${event.reason || 'None'}`, 'info');
  
  if (event.code !== 1000) {
    // Abnormal closure
    connectionError.value = `WebSocket connection unexpectedly closed (Code: ${event.code})`;
    if (event.code === 1006) {
      connectionError.value += ' - Connection abnormally closed, possibly due to network issues or server rejection';
      addMessage('A code 1006 error typically means that the connection was closed without a proper close frame', 'error');
      addMessage('Try the following solutions:', 'info');
      addMessage('1. Make sure the backend is deployed and running', 'info');
      addMessage('2. Check if Railway has WebSocket support enabled', 'info');
      addMessage('3. Try redeploying the backend application', 'info');
      addMessage('4. Enable the "Always On" option in Railway settings', 'info');
      addMessage('5. Check Railway logs for errors', 'info');
    } else if (event.code === 1008 || event.code === 1011) {
      connectionError.value += ' - Server returned an error';
    } else if (event.code === 1012) {
      connectionError.value += ' - Server is restarting';
    } else if (event.code === 1013) {
      connectionError.value += ' - Server is overloaded';
    }
  }
}

function handleWebSocketError(error) {
  connectionError.value = 'WebSocket connection error';
  addMessage(`WebSocket error: ${error.message || 'Unknown error'}`, 'error');
}

function handleMaxReconnectAttemptsReached() {
  addMessage('Maximum reconnection attempts reached', 'error');
  addMessage('Please check the server status and try connecting again manually', 'info');
}

// Disconnect WebSocket
function disconnectWebSocket() {
  if (isConnected.value) {
    addMessage('Disconnecting from WebSocket...', 'info');
    
    // Remove event listeners
    websocketService.off('open', handleWebSocketOpen);
    websocketService.off('message', handleWebSocketMessage);
    websocketService.off('close', handleWebSocketClose);
    websocketService.off('error', handleWebSocketError);
    websocketService.off('maxReconnectAttemptsReached', handleMaxReconnectAttemptsReached);
    
    // Disconnect
    websocketService.disconnect();
    isConnected.value = false;
    addMessage('WebSocket disconnected', 'info');
  }
}

// Send message
function sendMessage() {
  if (!isConnected.value) {
    addMessage('Cannot send message: WebSocket not connected', 'error');
    return;
  }
  
  const message = messageToSend.value.trim();
  if (!message) return;
  
  try {
    const success = websocketService.send(message);
    if (success) {
      addMessage(message, 'sent');
      messageToSend.value = ''; // Clear input field
    } else {
      addMessage('Failed to send message', 'error');
    }
  } catch (error) {
    addMessage(`Failed to send message: ${error.message}`, 'error');
  }
}

// Test connection
function testConnection() {
  messageToSend.value = 'Hello Server!';
  sendMessage();
}

// Component cleanup
onBeforeUnmount(() => {
  disconnectWebSocket();
});

// Add welcome message after component mount
onMounted(() => {
  addMessage('Welcome to the WebSocket Testing Tool', 'info');
  addMessage('Click the "Connect" button to begin testing', 'info');
  addMessage('Backend address: gleaming-celebration.railway.internal', 'info');
  addMessage('Ping messages are enabled to keep the connection alive', 'info');
});
</script>

<style scoped>
.websocket-test-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
  font-family: Arial, sans-serif;
}

h1 {
  text-align: center;
  margin-bottom: 2rem;
  color: #333;
}

.connection-panel {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding: 1.5rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.url-input {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.url-input label {
  font-weight: bold;
  color: #555;
}

.url-input-field {
  padding: 0.75rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
}

.connection-options {
  margin-top: 1rem;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.option label {
  margin-bottom: 0;
}

.option input[type="number"] {
  width: 100px;
  padding: 0.3rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.connection-controls {
  display: flex;
  gap: 1rem;
}

button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

button:not(:disabled):hover {
  transform: translateY(-2px);
}

.connect-button {
  background-color: #28a745;
  color: white;
}

.connect-button:not(:disabled):hover {
  background-color: #218838;
}

.disconnect-button {
  background-color: #dc3545;
  color: white;
}

.disconnect-button:not(:disabled):hover {
  background-color: #c82333;
}

.test-button {
  background-color: #17a2b8;
  color: white;
}

.test-button:not(:disabled):hover {
  background-color: #138496;
}

.connection-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  margin-bottom: 1.5rem;
  border-radius: 4px;
  background-color: #f8f9fa;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: #dc3545;
}

.connection-status.connected .status-indicator {
  background-color: #28a745;
}

.message-panel {
  margin-bottom: 1.5rem;
}

.message-input {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.message-input-field {
  flex: 1;
  padding: 0.75rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.send-button {
  background-color: #007bff;
  color: white;
}

.send-button:not(:disabled):hover {
  background-color: #0069d9;
}

.message-log {
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow: hidden;
}

.message-log h3 {
  margin: 0;
  padding: 0.75rem;
  background-color: #f8f9fa;
  border-bottom: 1px solid #ddd;
}

.messages-container {
  height: 300px;
  overflow-y: auto;
  padding: 0.75rem;
  background-color: #fff;
}

.message-item {
  margin-bottom: 0.75rem;
  padding: 0.75rem;
  border-radius: 4px;
  border-left: 4px solid #ccc;
  background-color: #f8f9fa;
}

.message-item.sent {
  border-left-color: #007bff;
  background-color: #e7f5ff;
}

.message-item.received {
  border-left-color: #28a745;
  background-color: #e7f7ef;
}

.message-item.error {
  border-left-color: #dc3545;
  background-color: #feecef;
}

.message-item.info {
  border-left-color: #17a2b8;
  background-color: #e7f6f8;
}

.message-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  color: #666;
}

.message-type {
  font-weight: bold;
}

.message-content {
  word-break: break-word;
}

.connection-info {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.connection-info h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #333;
}

.connection-info h4 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  color: #555;
}

.error-box {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background-color: #feecef;
  border-left: 4px solid #dc3545;
  border-radius: 4px;
}

.tips-box {
  padding: 1rem;
  background-color: #e7f5ff;
  border-left: 4px solid #007bff;
  border-radius: 4px;
}

.tips-box ul {
  margin: 0;
  padding-left: 1.5rem;
}

.tips-box li {
  margin-bottom: 0.5rem;
}

.tips-box li:last-child {
  margin-bottom: 0;
}

code {
  background-color: #eee;
  padding: 0.1rem 0.3rem;
  border-radius: 3px;
  font-family: monospace;
}

pre {
  white-space: pre-wrap;
  word-break: break-word;
  margin: 0;
  padding: 0.5rem;
  background-color: #f5f5f5;
  border-radius: 4px;
}
</style> 