"""Routes for copyright watermark functionality."""
import os
import logging
from fastapi import APIRouter, File, Form, UploadFile, HTTPException, Depends, Response
from fastapi.responses import StreamingResponse, Response
from typing import Optional
import io

# Import the watermark handler
from .handler import WatermarkHandler

# Setup logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Create a shared instance of the watermark handler
watermark_handler = WatermarkHandler()

def get_watermark_handler():
    """Dependency to get the watermark handler."""
    return watermark_handler

@router.post("/apply-watermark", summary="Apply watermark to an image")
async def apply_watermark(
    image: UploadFile = File(...),
    text: str = Form(...),
    position: str = Form("bottom-right"),
    opacity: float = Form(0.7),
    size: int = Form(24),
    handler: WatermarkHandler = Depends(get_watermark_handler)
):
    """
    Apply a text watermark to an uploaded image.
    
    Args:
        image: Image file to watermark
        text: Watermark text
        position: Position of watermark (top-left, top-center, top-right, middle-left, etc.)
        opacity: Opacity of watermark (0.0-1.0)
        size: Font size of watermark
        
    Returns:
        Watermarked image
    """
    try:
        # Validate parameters
        if opacity < 0.0 or opacity > 1.0:
            raise HTTPException(status_code=400, detail="Opacity must be between 0.0 and 1.0")
            
        if size < 8 or size > 100:
            raise HTTPException(status_code=400, detail="Size must be between 8 and 100")
            
        valid_positions = [
            "top-left", "top-center", "top-right", 
            "middle-left", "middle-center", "middle-right", 
            "bottom-left", "bottom-center", "bottom-right"
        ]
        if position not in valid_positions:
            raise HTTPException(status_code=400, detail=f"Position must be one of: {', '.join(valid_positions)}")
        
        # Read image data
        image_data = await image.read()
        if not image_data:
            raise HTTPException(status_code=400, detail="Empty image file")
            
        # Apply watermark
        watermarked_image = handler.apply_watermark(
            image_data=image_data,
            text=text,
            position=position,
            opacity=opacity,
            size=size
        )
        
        # Return the watermarked image
        return StreamingResponse(
            io.BytesIO(watermarked_image),
            media_type="image/png"
        )
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error applying watermark: {e}")
        raise HTTPException(status_code=500, detail=f"Error applying watermark: {str(e)}")

@router.post("/create-watermark-svg", summary="Create a transparent watermark SVG")
async def create_watermark_svg(
    text: str = Form(...),
    width: int = Form(800),
    height: int = Form(600),
    position: str = Form("bottom-right"),
    size: int = Form(24),
    color: Optional[str] = Form("#FFFFFF"),
    font_family: Optional[str] = Form("Arial, sans-serif"),
    handler: WatermarkHandler = Depends(get_watermark_handler)
):
    """
    Create a transparent SVG watermark.
    
    Args:
        text: Watermark text
        width: Width of the canvas
        height: Height of the canvas
        position: Position of watermark
        size: Font size
        color: Color of the watermark
        font_family: Font family of the watermark
        
    Returns:
        SVG watermark
    """
    try:
        # Validate parameters
        if width < 100 or width > 3000:
            raise HTTPException(status_code=400, detail="Width must be between 100 and 3000")
            
        if height < 100 or height > 3000:
            raise HTTPException(status_code=400, detail="Height must be between 100 and 3000")
            
        if size < 8 or size > 100:
            raise HTTPException(status_code=400, detail="Size must be between 8 and 100")
        
        valid_positions = [
            "top-left", "top-center", "top-right", 
            "middle-left", "middle-center", "middle-right", 
            "bottom-left", "bottom-center", "bottom-right"
        ]
        if position not in valid_positions:
            raise HTTPException(status_code=400, detail=f"Position must be one of: {', '.join(valid_positions)}")
        
        # Create watermark SVG
        svg_content = handler.create_transparent_watermark(
            text=text,
            width=width,
            height=height,
            position=position,
            size=size,
            color=color if color else "#FFFFFF",
            font_family=font_family if font_family else "Arial, sans-serif"
        )
        
        # Return the SVG content
        return Response(
            content=svg_content,
            media_type="image/svg+xml"
        )
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error creating watermark SVG: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating watermark SVG: {str(e)}")

@router.get("/health", summary="Health check for the watermark service")
async def health_check(handler: WatermarkHandler = Depends(get_watermark_handler)):
    """Health check endpoint for the watermark service."""
    return {
        "status": "ok",
        "default_font_available": handler.default_font is not None,
        "font_path": handler.default_font or "default PIL font",
    } 