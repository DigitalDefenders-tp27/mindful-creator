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
 * Calculate the position coordinates for SVG text
 * 
 * @param {string} position - Position name (top-left, bottom-right, etc.)
 * @param {number} width - Canvas width 
 * @param {number} height - Canvas height
 * @param {number} textWidth - Estimated text width
 * @param {number} textHeight - Text height
 * @returns {Object} - {x, y} coordinates
 */
function calculatePosition(position, width, height, textWidth, textHeight) {
  // Padding from edge
  const padding = 20;
  
  // Determine x position
  let x;
  if (position.endsWith('left')) {
    x = padding;
  } else if (position.endsWith('right')) {
    x = width - textWidth - padding;
  } else {
    // Center
    x = (width - textWidth) / 2;
  }
  
  // Determine y position
  let y;
  if (position.startsWith('top')) {
    y = textHeight + padding;
  } else if (position.startsWith('bottom')) {
    y = height - padding;
  } else {
    // Middle
    y = height / 2;
  }
  
  return { x: Math.round(x), y: Math.round(y) };
}

/**
 * Generate SVG watermark locally (client-side fallback)
 * 
 * @param {string} text - The watermark text
 * @param {number} width - Width of the canvas 
 * @param {number} height - Height of the canvas
 * @param {string} position - Position of the watermark
 * @param {number} size - Font size of the watermark
 * @param {string} color - Color of the watermark text
 * @param {string} fontFamily - Font family of the watermark text
 * @returns {string} - SVG content as string
 */
function generateLocalSvg(text, width, height, position, size, color, fontFamily) {
  // Estimate text width (very rough approximation)
  const textWidth = text.length * size * 0.6;
  const textHeight = size;
  
  // Calculate position
  const { x, y } = calculatePosition(position, width, height, textWidth, textHeight);
  
  // Create SVG content
  const svgContent = `<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
  <!-- Shadow -->
  <text x="${x + 2}" y="${y + 2}" font-family="${fontFamily}" font-size="${size}px" fill="rgba(0,0,0,0.5)">${text}</text>
  <!-- Main text -->
  <text x="${x}" y="${y}" font-family="${fontFamily}" font-size="${size}px" fill="${color}">${text}</text>
</svg>`;
  
  return svgContent;
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
      // If API call fails, generate SVG locally as fallback
      console.warn("Failed to create SVG watermark from API, falling back to client-side generation");
      return generateLocalSvg(text, width, height, position, size, color, fontFamily);
    }

    return await response.text();
  } catch (error) {
    console.error('Error creating SVG watermark from API:', error);
    // If any error occurs, fall back to client-side SVG generation
    console.warn("Using client-side SVG generation as fallback");
    return generateLocalSvg(text, width, height, position, size, color, fontFamily);
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