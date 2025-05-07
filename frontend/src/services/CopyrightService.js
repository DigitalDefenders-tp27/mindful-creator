/**
 * Service for interacting with the copyright watermark API
 */

/**
 * Apply watermark to an image
 * 
 * @param {File} imageFile - The image file to watermark
 * @param {string} text - The watermark text
 * @param {string} position - Position of the watermark
 * @param {number} opacity - Opacity of the watermark (0.0-1.0)
 * @param {number} size - Font size of the watermark
 * @returns {Promise<Blob>} - Promise resolving to the watermarked image blob
 */
export async function applyWatermark(imageFile, text, position = 'bottom-right', opacity = 0.7, size = 24) {
  try {
    const formData = new FormData();
    formData.append('image', imageFile);
    formData.append('text', text);
    formData.append('position', position);
    formData.append('opacity', opacity);
    formData.append('size', size);
    
    const response = await fetch('/api/copyright/apply-watermark', {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to apply watermark');
    }
    
    return await response.blob();
  } catch (error) {
    console.error('Error applying watermark:', error);
    throw error;
  }
}

/**
 * Create a transparent SVG watermark
 * 
 * @param {string} text - The watermark text
 * @param {number} width - Width of the canvas
 * @param {number} height - Height of the canvas
 * @param {string} position - Position of the watermark
 * @param {number} size - Font size of the watermark
 * @returns {Promise<string>} - Promise resolving to the SVG content
 */
export async function createSvgWatermark(text, width = 800, height = 600, position = 'bottom-right', size = 24) {
  try {
    const formData = new FormData();
    formData.append('text', text);
    formData.append('width', width);
    formData.append('height', height);
    formData.append('position', position);
    formData.append('size', size);
    
    const response = await fetch('/api/copyright/create-watermark-svg', {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to create SVG watermark');
    }
    
    return await response.text();
  } catch (error) {
    console.error('Error creating SVG watermark:', error);
    throw error;
  }
}

/**
 * Check the health of the watermark service
 * 
 * @returns {Promise<Object>} - Promise resolving to the health check response
 */
export async function checkWatermarkHealth() {
  try {
    const response = await fetch('/api/copyright/health');
    
    if (!response.ok) {
      throw new Error('Watermark service health check failed');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error checking watermark service health:', error);
    throw error;
  }
} 