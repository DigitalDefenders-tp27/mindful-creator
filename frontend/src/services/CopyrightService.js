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
 * @param {string} color - Color of the watermark text
 * @param {string} fontFamily - Font family of the watermark text
 * @returns {Promise<string>} - Promise resolving to the SVG content
 */
export async function createSvgWatermark(text, width = 800, height = 600, position = 'bottom-right', size = 24, color = '#FFFFFF', fontFamily = 'Arial, sans-serif') {
  try {
    const formData = new FormData();
    formData.append('text', text);
    formData.append('width', width);
    formData.append('height', height);
    formData.append('position', position);
    formData.append('size', size);
    formData.append('color', color);
    formData.append('font_family', fontFamily);

    const response = await fetch('/api/copyright/create-watermark-svg', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      let errorDetailMessage = `Failed to create SVG watermark. Status: ${response.status}`;
      const responseForJson = response.clone(); // Clone for JSON parsing
      const responseForText = response.clone(); // Clone for text parsing

      try {
        // Try to parse as JSON first, as some APIs might return JSON error details
        const errorData = await responseForJson.json();
        errorDetailMessage = errorData.detail || errorData.message || JSON.stringify(errorData);
      } catch (jsonError) {
        // If JSON parsing fails, read as text (e.g., for HTML error pages or plain text errors)
        try {
          const textError = await responseForText.text();
          // Use the textError if it's not empty, otherwise stick with the status message
          if (textError && textError.trim() !== '') {
            errorDetailMessage = textError;
          }
        } catch (textParseError) {
          // If reading as text also fails, log this and stick with the status code message
          console.error('Failed to parse error response as JSON or text:', textParseError);
        }
      }
      throw new Error(errorDetailMessage);
    }

    return await response.text();
  } catch (error) {
    console.error('Error creating SVG watermark:', error);
    // Ensure the error propagated is useful
    if (error instanceof Error) {
        throw error;
    } else {
        throw new Error(String(error));
    }
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