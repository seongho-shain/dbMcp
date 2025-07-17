"""
Gallery routes
API endpoints for gallery operations
"""
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional

from .service import GalleryService
from .models import (
    GalleryUploadResponse,
    GallerySessionResponse,
    GalleryDeleteResponse,
    GalleryStatsResponse
)

router = APIRouter(prefix="/gallery", tags=["gallery"])
gallery_service = GalleryService()


@router.post("/upload", response_model=GalleryUploadResponse)
async def upload_gallery_item(
    image: UploadFile = File(...),
    session_id: int = Form(...),
    user_id: int = Form(...),
    user_name: str = Form(...),
    user_type: str = Form(...),
    prompt: str = Form(...),
    title: Optional[str] = Form(None)
):
    """
    Upload a new gallery item with image and prompt
    """
    try:
        # Validate user_type
        if user_type not in ["student", "teacher"]:
            raise HTTPException(status_code=400, detail="Invalid user type")
        
        # Validate file type
        if not image.content_type or not image.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image data
        image_data = await image.read()
        
        # Validate image
        validation = gallery_service.validate_image_file(image_data)
        if not validation["valid"]:
            raise HTTPException(status_code=400, detail=validation["error"])
        
        # Create gallery item
        result = gallery_service.create_gallery_item(
            session_id=session_id,
            user_id=user_id,
            user_name=user_name,
            user_type=user_type,
            image_data=image_data,
            prompt=prompt,
            title=title,
            image_format=validation.get("format", "PNG")
        )
        
        if result["success"]:
            return GalleryUploadResponse(
                success=True,
                message="Gallery item created successfully",
                item=result["item"]
            )
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@router.get("/session/{session_id}")
async def get_session_gallery(
    session_id: int,
    user_id: int,
    user_type: str
):
    """
    Get all gallery items for a specific session
    """
    try:
        # Validate user_type
        if user_type not in ["student", "teacher"]:
            raise HTTPException(status_code=400, detail="Invalid user type")
        
        result = gallery_service.get_session_gallery_items(
            session_id=session_id,
            user_id=user_id,
            user_type=user_type
        )
        
        if result["success"]:
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "items": result["items"],
                    "session_id": session_id
                }
            )
        else:
            raise HTTPException(status_code=403, detail=result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@router.delete("/{item_id}")
async def delete_gallery_item(
    item_id: int,
    user_id: int,
    user_type: str
):
    """
    Delete a gallery item (only by creator or session teacher)
    """
    try:
        # Validate user_type
        if user_type not in ["student", "teacher"]:
            raise HTTPException(status_code=400, detail="Invalid user type")
        
        result = gallery_service.delete_gallery_item(
            item_id=item_id,
            user_id=user_id,
            user_type=user_type
        )
        
        if result["success"]:
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "message": result["message"]
                }
            )
        else:
            raise HTTPException(status_code=403, detail=result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@router.get("/item/{item_id}")
async def get_gallery_item(
    item_id: int,
    user_id: int,
    user_type: str
):
    """
    Get a specific gallery item (with session access validation)
    """
    try:
        # Validate user_type
        if user_type not in ["student", "teacher"]:
            raise HTTPException(status_code=400, detail="Invalid user type")
        
        result = gallery_service.get_gallery_item(
            item_id=item_id,
            user_id=user_id,
            user_type=user_type
        )
        
        if result["success"]:
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "item": result["item"]
                }
            )
        else:
            raise HTTPException(status_code=403, detail=result["error"])
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@router.get("/session/{session_id}/stats")
async def get_session_gallery_stats(
    session_id: int,
    user_id: int,
    user_type: str
):
    """
    Get statistics for a session's gallery
    """
    try:
        # Validate user_type and access
        if user_type not in ["student", "teacher"]:
            raise HTTPException(status_code=400, detail="Invalid user type")
        
        result = gallery_service.get_session_gallery_stats(
            session_id=session_id,
            user_id=user_id,
            user_type=user_type
        )
        
        if result["success"]:
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "stats": result["stats"]
                }
            )
        else:
            raise HTTPException(status_code=403, detail=result["error"])
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")