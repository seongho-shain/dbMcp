"""
Gallery API Views - FastAPI endpoints for gallery functionality
"""
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional
import json

from app.controllers.gallery_controller import GalleryController
from app.services.database_service import DatabaseService


router = APIRouter()
db_service = DatabaseService()
gallery_controller = GalleryController(db_service)


@router.post("/upload")
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
        validation = gallery_controller.validate_image_file(image_data)
        if not validation["valid"]:
            raise HTTPException(status_code=400, detail=validation["error"])
        
        # Create gallery item
        result = gallery_controller.create_gallery_item(
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
            return JSONResponse(
                status_code=201,
                content={
                    "success": True,
                    "message": "Gallery item created successfully",
                    "item": result["item"]
                }
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
        
        result = gallery_controller.get_session_gallery_items(
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
        
        result = gallery_controller.delete_gallery_item(
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
        
        # Get the item first
        item = db_service.get_gallery_item_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Gallery item not found")
        
        # Validate session access
        result = gallery_controller.get_session_gallery_items(
            session_id=item["session_id"],
            user_id=user_id,
            user_type=user_type
        )
        
        if not result["success"]:
            raise HTTPException(status_code=403, detail=result["error"])
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "item": item
            }
        )
        
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
        
        result = gallery_controller.get_session_gallery_items(
            session_id=session_id,
            user_id=user_id,
            user_type=user_type
        )
        
        if not result["success"]:
            raise HTTPException(status_code=403, detail=result["error"])
        
        items = result["items"]
        
        # Calculate stats
        total_items = len(items)
        student_items = len([item for item in items if item["user_type"] == "student"])
        teacher_items = len([item for item in items if item["user_type"] == "teacher"])
        
        # Get unique contributors
        contributors = set()
        for item in items:
            contributors.add(f"{item['user_name']}_{item['user_type']}")
        
        stats = {
            "total_items": total_items,
            "student_items": student_items,
            "teacher_items": teacher_items,
            "unique_contributors": len(contributors),
            "session_id": session_id
        }
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "stats": stats
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")