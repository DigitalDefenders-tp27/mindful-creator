# Copyright Watermark API

This module provides API endpoints for adding watermarks to images and generating transparent SVG watermarks with copyright notices.

## Features

- Add text watermarks to uploaded images
- Create transparent SVG watermarks that can be used as overlays
- Customizable watermark positioning, opacity, and size
- Support for Australian copyright format

## API Endpoints

### Apply Watermark to Image

```
POST /api/copyright/apply-watermark
```

Apply a text watermark to an uploaded image.

**Parameters:**

- `image`: The image file to watermark (multipart/form-data)
- `text`: Watermark text (e.g., "© 2025 Your Name. All rights reserved.")
- `position`: Position of watermark (default: "bottom-right")
  - Options: "top-left", "top-center", "top-right", "middle-left", "middle-center", "middle-right", "bottom-left", "bottom-center", "bottom-right"
- `opacity`: Opacity of watermark (0.0-1.0, default: 0.7)
- `size`: Font size of watermark (default: 24)

**Response:**

Returns the watermarked image as a PNG file.

### Create Transparent SVG Watermark

```
POST /api/copyright/create-watermark-svg
```

Create a transparent SVG watermark that can be used as an overlay.

**Parameters:**

- `text`: Watermark text (e.g., "© 2025 Your Name. All rights reserved.")
- `width`: Width of the canvas (default: 800)
- `height`: Height of the canvas (default: 600)
- `position`: Position of watermark (default: "bottom-right")
  - Options: "top-left", "top-center", "top-right", "middle-left", "middle-center", "middle-right", "bottom-left", "bottom-center", "bottom-right"
- `size`: Font size of watermark (default: 24)

**Response:**

Returns an SVG file with a transparent background and the watermark text.

### Health Check

```
GET /api/copyright/health
```

Check the health status of the watermark service.

**Response:**

```json
{
  "status": "ok",
  "default_font_available": true,
  "font_path": "/path/to/font.ttf"
}
```

## Usage Examples

### With cURL

Apply watermark to an image:

```bash
curl -X POST \
  http://localhost:8000/api/copyright/apply-watermark \
  -F "image=@/path/to/image.jpg" \
  -F "text=© 2025 Your Name. All rights reserved." \
  -F "position=bottom-right" \
  -F "opacity=0.7" \
  -F "size=24" \
  -o watermarked-image.png
```

Create a transparent SVG watermark:

```bash
curl -X POST \
  http://localhost:8000/api/copyright/create-watermark-svg \
  -F "text=© 2025 Your Name. All rights reserved." \
  -F "width=800" \
  -F "height=600" \
  -F "position=bottom-right" \
  -F "size=24" \
  -o watermark.svg
```

### With JavaScript Fetch API

```javascript
// Apply watermark to an image
async function applyWatermark(imageFile, text) {
  const formData = new FormData();
  formData.append('image', imageFile);
  formData.append('text', text);
  formData.append('position', 'bottom-right');
  formData.append('opacity', '0.7');
  formData.append('size', '24');
  
  const response = await fetch('/api/copyright/apply-watermark', {
    method: 'POST',
    body: formData
  });
  
  if (response.ok) {
    const blob = await response.blob();
    // Create a URL for the blob
    const url = URL.createObjectURL(blob);
    return url;
  } else {
    throw new Error('Failed to apply watermark');
  }
}

// Create transparent SVG watermark
async function createSvgWatermark(text) {
  const formData = new FormData();
  formData.append('text', text);
  formData.append('width', '800');
  formData.append('height', '600');
  formData.append('position', 'bottom-right');
  formData.append('size', '24');
  
  const response = await fetch('/api/copyright/create-watermark-svg', {
    method: 'POST',
    body: formData
  });
  
  if (response.ok) {
    const svgText = await response.text();
    return svgText;
  } else {
    throw new Error('Failed to create SVG watermark');
  }
}
```

## Dependencies

This module requires the following Python packages:

- fastapi
- python-multipart
- Pillow
- svgwrite

These are automatically installed when you install the requirements for the backend. 