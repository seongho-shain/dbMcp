"""
Gallery service
Business logic for gallery operations
"""
import os
import uuid
import base64
import io
from typing import List, Optional, Dict, Any
from datetime import datetime
from PIL import Image

from app.core.services.database_service import DatabaseService


class GalleryService:
    """
    갤러리 관련 비즈니스 로직을 처리하는 서비스
    이미지 업로드, 조회, 삭제 기능을 담당
    """
    
    def __init__(self):
        self.db_service = DatabaseService()

    def create_gallery_item(
        self,
        session_id: int,
        user_id: int,
        user_name: str,
        user_type: str,
        image_data: bytes,
        prompt: str,
        title: Optional[str] = None,
        image_format: str = "PNG"
    ) -> dict:
        """
        Create a new gallery item with image upload
        """
        try:
            # Validate session exists and user has access
            session = self.db_service.get_session_by_id(session_id)
            if not session:
                return {"success": False, "error": "Session not found"}
            
            # Validate user access to session
            if user_type == "student":
                student = self.db_service.get_student_by_session_and_name(session_id, user_name)
                if not student:
                    return {"success": False, "error": "Student not found in this session"}
            elif user_type == "teacher":
                if session.get("teacher_id") != user_id:
                    return {"success": False, "error": "Teacher not authorized for this session"}
            
            # Process and validate image
            try:
                # Open image with PIL for validation and processing
                image = Image.open(io.BytesIO(image_data))
                
                # Convert to RGB if necessary
                if image.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', image.size, (255, 255, 255))
                    if image.mode == 'P':
                        image = image.convert('RGBA')
                    background.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
                    image = background
                elif image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Resize if too large (max 1920x1920)
                max_size = (1920, 1920)
                if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
                    image.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Convert back to bytes
                img_buffer = io.BytesIO()
                image.save(img_buffer, format=image_format, quality=85, optimize=True)
                processed_image_data = img_buffer.getvalue()
                
            except Exception as e:
                return {"success": False, "error": f"Invalid image format: {str(e)}"}
            
            # Convert image to base64 for storage (temporary solution)
            # In production, you would upload to cloud storage (S3, Cloudinary, etc.)
            image_base64 = base64.b64encode(processed_image_data).decode('utf-8')
            image_url = f"data:image/{image_format.lower()};base64,{image_base64}"
            
            # Save to database
            gallery_item = self.db_service.create_gallery_item(
                session_id=session_id,
                user_id=user_id,
                user_name=user_name,
                user_type=user_type,
                image_url=image_url,
                prompt=prompt,
                title=title
            )
            
            if gallery_item:
                return {"success": True, "item": gallery_item}
            else:
                return {"success": False, "error": "Failed to create gallery item"}
                
        except Exception as e:
            return {"success": False, "error": f"Server error: {str(e)}"}

    def get_session_gallery_items(self, session_id: int, user_id: int, user_type: str) -> dict:
        """
        Get all gallery items for a specific session
        """
        try:
            # Validate session exists and user has access
            session = self.db_service.get_session_by_id(session_id)
            if not session:
                return {"success": False, "error": "Session not found"}
            
            # Validate user access to session
            if user_type == "student":
                student = self.db_service.get_student_by_id(user_id)
                if not student or student.get("session_id") != session_id:
                    return {"success": False, "error": "Access denied to this session"}
            elif user_type == "teacher":
                if session.get("teacher_id") != user_id:
                    return {"success": False, "error": "Access denied to this session"}
            
            # Get gallery items
            items = self.db_service.get_gallery_items_by_session(session_id)
            
            return {"success": True, "items": items}
            
        except Exception as e:
            return {"success": False, "error": f"Server error: {str(e)}"}

    def delete_gallery_item(self, item_id: int, user_id: int, user_type: str) -> dict:
        """
        Delete a gallery item (only by the creator or teacher of the session)
        """
        try:
            # Get the gallery item
            item = self.db_service.get_gallery_item_by_id(item_id)
            if not item:
                return {"success": False, "error": "Gallery item not found"}
            
            # Check permissions
            can_delete = False
            
            if user_type == "teacher":
                # Teachers can delete items in their sessions
                session = self.db_service.get_session_by_id(item["session_id"])
                if session and session.get("teacher_id") == user_id:
                    can_delete = True
            elif user_type == "student":
                # Students can only delete their own items
                if item["user_id"] == user_id and item["user_type"] == "student":
                    can_delete = True
            
            if not can_delete:
                return {"success": False, "error": "Access denied"}
            
            # Delete the item
            success = self.db_service.delete_gallery_item(item_id)
            
            if success:
                return {"success": True, "message": "Gallery item deleted successfully"}
            else:
                return {"success": False, "error": "Failed to delete gallery item"}
                
        except Exception as e:
            return {"success": False, "error": f"Server error: {str(e)}"}

    def get_gallery_item(self, item_id: int, user_id: int, user_type: str) -> dict:
        """
        Get a specific gallery item (with session access validation)
        """
        try:
            # Get the item first
            item = self.db_service.get_gallery_item_by_id(item_id)
            if not item:
                return {"success": False, "error": "Gallery item not found"}
            
            # Validate session access
            result = self.get_session_gallery_items(
                session_id=item["session_id"],
                user_id=user_id,
                user_type=user_type
            )
            
            if not result["success"]:
                return {"success": False, "error": result["error"]}
            
            return {"success": True, "item": item}
            
        except Exception as e:
            return {"success": False, "error": f"Server error: {str(e)}"}

    def get_session_gallery_stats(self, session_id: int, user_id: int, user_type: str) -> dict:
        """
        Get statistics for a session's gallery
        """
        try:
            # Validate user_type and access
            if user_type not in ["student", "teacher"]:
                return {"success": False, "error": "Invalid user type"}
            
            result = self.get_session_gallery_items(
                session_id=session_id,
                user_id=user_id,
                user_type=user_type
            )
            
            if not result["success"]:
                return {"success": False, "error": result["error"]}
            
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
            
            return {"success": True, "stats": stats}
            
        except Exception as e:
            return {"success": False, "error": f"Server error: {str(e)}"}

    def validate_image_file(self, file_data: bytes, max_size_mb: int = 5) -> dict:
        """
        Validate uploaded image file
        """
        try:
            # Check file size
            file_size_mb = len(file_data) / (1024 * 1024)
            if file_size_mb > max_size_mb:
                return {"valid": False, "error": f"File too large. Maximum size is {max_size_mb}MB"}
            
            # Check if it's a valid image
            try:
                image = Image.open(io.BytesIO(file_data))
                image.verify()  # Verify it's a valid image
                
                # Check format
                allowed_formats = ['JPEG', 'PNG', 'WebP']
                if image.format not in allowed_formats:
                    return {"valid": False, "error": f"Unsupported format. Allowed: {', '.join(allowed_formats)}"}
                
                return {"valid": True, "format": image.format, "size": image.size}
                
            except Exception:
                return {"valid": False, "error": "Invalid image file"}
                
        except Exception as e:
            return {"valid": False, "error": f"File validation error: {str(e)}"}