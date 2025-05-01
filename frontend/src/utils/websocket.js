/**
 * WebSocket Connection Utility
 * Used to establish WebSocket connections with the backend
 */

class WebSocketService {
  constructor() {
    this.socket = null;
    this.isConnected = false;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 3000; // 3 seconds
    this.pingInterval = null;
    this.listeners = new Map();
  }

  /**
   * Initialises WebSocket connection
   * @param {string} url - WebSocket server URL (use wss:// instead of ws://)
   * @param {Object} options - Connection options
   * @param {boolean} options.enablePing - Enable ping/pong to keep connection alive
   * @param {number} options.pingIntervalMs - Ping interval in milliseconds (default: 30000)
   */
  connect(url, options = {}) {
    if (this.socket) {
      this.disconnect();
    }

    // Reset state
    this.reconnectAttempts = 0;
    clearInterval(this.pingInterval);
    this.pingInterval = null;

    // Connection options
    const enablePing = options.enablePing !== undefined ? options.enablePing : true;
    const pingIntervalMs = options.pingIntervalMs || 30000; // Default 30 seconds

    // Ensure WSS is used in HTTPS environments
    if (window.location.protocol === 'https:' && !url.startsWith('wss://')) {
      url = url.replace('ws://', 'wss://');
    }

    // Check if URL is valid
    if (!url || !url.startsWith('wss://')) {
      console.error('Invalid WebSocket URL. Must start with wss:// in HTTPS environments');
      this._notifyListeners('error', { message: 'Invalid WebSocket URL format' });
      return false;
    }

    try {
      console.log(`Attempting to connect to WebSocket: ${url}`);
      this.socket = new WebSocket(url);
      
      // Set timeout for connection attempt
      const connectionTimeout = setTimeout(() => {
        if (this.socket && this.socket.readyState !== WebSocket.OPEN) {
          console.warn('WebSocket connection timeout - closing socket');
          this.socket.close(4000, 'Connection timeout');
          this._notifyListeners('error', { message: 'Connection timeout' });
        }
      }, 10000); // 10 seconds timeout
      
      this.socket.onopen = () => {
        clearTimeout(connectionTimeout);
        console.log('WebSocket connection established');
        this.isConnected = true;
        this.reconnectAttempts = 0;
        this._notifyListeners('open');
        
        // Set up ping interval to keep connection alive if enabled
        if (enablePing) {
          this.startPingInterval(pingIntervalMs);
        }
      };
      
      this.socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this._notifyListeners('message', data);
        } catch (e) {
          this._notifyListeners('message', event.data);
        }
      };
      
      this.socket.onclose = (event) => {
        clearTimeout(connectionTimeout);
        clearInterval(this.pingInterval);
        this.pingInterval = null;
        this.isConnected = false;
        
        console.log(`WebSocket connection closed: ${event.code} ${event.reason}`);
        this._notifyListeners('close', event);
        
        // Attempt reconnection if not a normal closure and not a manual disconnect
        if (event.code !== 1000 && event.code !== 4000) {
          if (this.reconnectAttempts < this.maxReconnectAttempts) {
            const delay = this.calculateReconnectDelay();
            this.reconnectAttempts++;
            console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts}) after ${delay}ms`);
            setTimeout(() => this.connect(url, options), delay);
          } else {
            console.warn('Maximum reconnect attempts reached');
            this._notifyListeners('maxReconnectAttemptsReached');
          }
        }
      };
      
      this.socket.onerror = (error) => {
        console.error('WebSocket error:', error);
        this._notifyListeners('error', error);
      };
      
      return true;
    } catch (error) {
      console.error('Error creating WebSocket connection:', error);
      this._notifyListeners('error', { message: error.message });
      return false;
    }
  }

  /**
   * Calculate reconnect delay with exponential backoff
   * @private
   */
  calculateReconnectDelay() {
    // Exponential backoff: 3s, 6s, 12s, 24s, 48s
    return Math.min(30000, this.reconnectDelay * Math.pow(2, this.reconnectAttempts));
  }
  
  /**
   * Start ping interval to keep connection alive
   * @private
   */
  startPingInterval(interval) {
    this.pingInterval = setInterval(() => {
      if (this.isConnected && this.socket.readyState === WebSocket.OPEN) {
        try {
          // Send a ping message to keep the connection alive
          this.socket.send(JSON.stringify({ type: 'ping', timestamp: Date.now() }));
        } catch (error) {
          console.error('Error sending ping:', error);
        }
      } else {
        // Clear interval if connection is lost
        clearInterval(this.pingInterval);
        this.pingInterval = null;
      }
    }, interval);
  }

  /**
   * Disconnects WebSocket connection
   */
  disconnect() {
    clearInterval(this.pingInterval);
    this.pingInterval = null;
    
    if (this.socket) {
      if (this.socket.readyState === WebSocket.OPEN || this.socket.readyState === WebSocket.CONNECTING) {
        this.socket.close(1000, 'Client initiated disconnect');
      }
      this.socket = null;
    }
    this.isConnected = false;
  }

  /**
   * Sends message to the server
   * @param {Object|string} data - Data to send
   */
  send(data) {
    if (!this.isConnected || !this.socket || this.socket.readyState !== WebSocket.OPEN) {
      console.error('WebSocket not connected, cannot send message');
      return false;
    }
    
    try {
      const message = typeof data === 'object' ? JSON.stringify(data) : data;
      this.socket.send(message);
      return true;
    } catch (error) {
      console.error('Error sending WebSocket message:', error);
      return false;
    }
  }

  /**
   * Adds event listener
   * @param {string} event - Event name ('open', 'message', 'close', 'error', 'maxReconnectAttemptsReached')
   * @param {Function} callback - Callback function
   */
  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(callback);
  }

  /**
   * Removes event listener
   * @param {string} event - Event name
   * @param {Function} callback - Callback function to remove
   */
  off(event, callback) {
    if (!this.listeners.has(event)) return;
    
    const callbacks = this.listeners.get(event);
    const index = callbacks.indexOf(callback);
    
    if (index !== -1) {
      callbacks.splice(index, 1);
    }
  }

  /**
   * Notifies all listeners of a specific event
   * @private
   */
  _notifyListeners(event, data) {
    if (!this.listeners.has(event)) return;
    
    const callbacks = this.listeners.get(event);
    callbacks.forEach(callback => {
      try {
        callback(data);
      } catch (error) {
        console.error(`Error executing WebSocket ${event} callback:`, error);
      }
    });
  }
}

// Create singleton instance
const websocketService = new WebSocketService();
export default websocketService;

// Usage example:
// 
// import websocketService from '@/utils/websocket';
// 
// // Connect to backend WebSocket with ping enabled to keep connection alive
// websocketService.connect('wss://mindful-creator-production-e20c.up.railway.app/ws', {
//   enablePing: true,
//   pingIntervalMs: 20000 // 20 seconds
// });
// 
// // Listen for messages
// websocketService.on('message', (data) => {
//   console.log('Received message:', data);
// });
// 
// // Send message
// websocketService.send({ type: 'hello', content: 'world' });
// 
// // Disconnect
// websocketService.disconnect();

/*
 * Railway Configuration Guide:
 * 
 * To enable WebSocket support on Railway, ensure:
 * 
 * 1. You've redeployed the backend code with the WebSocket endpoint
 *    The code should include a WebSocket endpoint like this:
 *    @app.websocket("/ws")
 *    async def websocket_endpoint(websocket: WebSocket):
 *        await websocket.accept()
 *        try:
 *            while True:
 *                data = await websocket.receive_text()
 *                await websocket.send_text(f"Echo: {data}")
 *        except Exception:
 *            pass
 * 
 * 2. Check the network configuration in Railway project "Settings":
 *    - Ensure there are no proxies blocking WebSocket connections
 *    - Check if there's a custom domain and try connecting with it
 * 
 * 3. WebSocket URL format should be:
 *    wss://mindful-creator-production-e20c.up.railway.app/ws
 *    Note: URL must use wss:// rather than ws:// or https://
 * 
 * 4. If you still get 403 or 1006 errors:
 *    - Redeploy the backend project in Railway
 *    - Check Railway logs for error messages
 *    - Try restarting the service using Railway's "Advanced Settings"
 *    - Ensure "Always On" is enabled in Railway service settings
 *    - Try connecting through a test endpoint first: 
 *      https://mindful-creator-production-e20c.up.railway.app/ws-test
 */ 