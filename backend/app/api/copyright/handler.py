"""Handler for copyright watermark functionality."""
import os
import io
import base64
import logging
from typing import Dict, Any, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import svgwrite
from svgwrite.text import Text

# Setup logging
logger = logging.getLogger(__name__)

class WatermarkHandler:
    """Handler for creating watermarks and applying them to images."""
    
    def __init__(self):
        """Initialize the watermark handler."""
        # Default font selection
        self.default_font = None
        self.font_size = 24
        
        # Try to load a default font
        try:
            # Check for system fonts
            font_paths = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
                "/Library/Fonts/Arial.ttf",  # macOS
                "C:\\Windows\\Fonts\\arial.ttf"  # Windows
            ]
            
            for path in font_paths:
                if os.path.exists(path):
                    self.default_font = path
                    break
            
            if not self.default_font:
                logger.warning("No system fonts found, using default PIL font")
        except Exception as e:
            logger.error(f"Error initializing font: {e}")
    
    def apply_watermark(self, 
                        image_data: bytes, 
                        text: str, 
                        position: str = "bottom-right", 
                        opacity: float = 0.7, 
                        size: int = 24) -> bytes:
        """
        Apply text watermark to an image.
        
        Args:
            image_data: Raw image data
            text: Watermark text
            position: Position (top-left, top-center, etc.)
            opacity: Opacity of watermark (0.0-1.0)
            size: Font size
            
        Returns:
            Watermarked image data as bytes
        """
        try:
            # Open the image
            img = Image.open(io.BytesIO(image_data))
            
            # Create a transparent overlay for the watermark
            overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            
            # Load font
            font = None
            if self.default_font:
                try:
                    font = ImageFont.truetype(self.default_font, size)
                except Exception as e:
                    logger.error(f"Error loading font: {e}")
                    
            if font is None:
                # Fall back to default PIL font
                font = ImageFont.load_default()
                
            # Calculate text size
            text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:4]
            
            # Calculate position
            width, height = img.size
            x, y = self._calculate_position(position, width, height, text_width, text_height)
            
            # Draw text with shadow for better visibility
            shadow_color = (0, 0, 0, int(255 * opacity * 0.7))
            text_color = (255, 255, 255, int(255 * opacity))
            
            # Draw shadow first
            draw.text((x+2, y+2), text, font=font, fill=shadow_color)
            
            # Draw main text
            draw.text((x, y), text, font=font, fill=text_color)
            
            # Composite the watermark onto the image
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
                
            watermarked = Image.alpha_composite(img, overlay)
            
            # Convert back to bytes
            output = io.BytesIO()
            watermarked.save(output, format='PNG')
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"Error applying watermark: {e}")
            raise
    
    def create_transparent_watermark(self, 
                                    text: str,
                                    width: int = 800, 
                                    height: int = 600, 
                                    position: str = "bottom-right",
                                    size: int = 24,
                                    color: str = "#FFFFFF",
                                    font_family: str = "Arial, sans-serif") -> str:
        """
        Create a transparent SVG watermark.
        
        Args:
            text: Watermark text
            width: Width of the canvas
            height: Height of the canvas
            position: Position of the watermark
            size: Font size
            color: Color of the watermark text
            font_family: CSS font-family string
            
        Returns:
            SVG content as string
        """
        try:
            # Create SVG drawing
            dwg = svgwrite.Drawing(size=(width, height), profile='full', debug=False)
            
            # Calculate position (approximate since SVG text metrics are different)
            # We'll assume the text width is roughly 10 pixels per character
            text_width = len(text) * size * 0.6
            text_height = size
            
            x, y = self._calculate_position(position, width, height, text_width, text_height)
            
            # Add drop shadow (using a slightly darker version of the chosen color or black)
            # For simplicity, shadow is black here, but could be derived from 'color'
            shadow_opacity = 0.5 # Keep shadow opacity fixed or make it a parameter
            shadow_fill = "black" 

            shadow = dwg.text(text, insert=(x+2, y+2), 
                           fill=shadow_fill, opacity=shadow_opacity, 
                           style=f'font-size:{size}px; font-family:{font_family}')
            dwg.add(shadow)
            
            # Add main text
            text_elem = dwg.text(text, insert=(x, y), 
                              fill=color,  # Use the color parameter
                              style=f'font-size:{size}px; font-family:{font_family}') # Use font_family
            dwg.add(text_elem)
            
            # Return SVG as string
            return dwg.tostring()
            
        except Exception as e:
            logger.error(f"Error creating transparent watermark: {e}")
            raise
    
    def _calculate_position(self, 
                           position: str, 
                           width: int, 
                           height: int, 
                           text_width: int, 
                           text_height: int) -> Tuple[int, int]:
        """
        Calculate the position coordinates based on the selected position.
        
        Args:
            position: Named position (top-left, bottom-right, etc.)
            width: Image width
            height: Image height
            text_width: Width of the text
            text_height: Height of the text
            
        Returns:
            Tuple of (x, y) coordinates
        """
        # Padding from edge
        padding = 20
        
        # Determine x position
        if position.endswith('left'):
            x = padding
        elif position.endswith('right'):
            x = width - text_width - padding
        else:
            # Center
            x = (width - text_width) / 2
        
        # Determine y position
        if position.startswith('top'):
            y = text_height + padding
        elif position.startswith('bottom'):
            y = height - padding
        else:
            # Middle
            y = height / 2
            
        return int(x), int(y) 