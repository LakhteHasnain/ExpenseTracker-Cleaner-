from sqlalchemy.orm import Session
from src.images.image_model import Image
from src.images.imgbb_service import ImgBBService
from fastapi import HTTPException
from typing import List

class ImageController:
    
    @staticmethod
    def upload_image(image_data: bytes, name: str = None, expiration: int = None, transaction_id = None, db: Session = None) -> Image:
        """
        Upload image to ImgBB and save metadata to database
        
        Args:
            image_data: Binary image data
            name: Optional image name
            expiration: Optional expiration time in seconds
            transaction_id: Optional transaction ID to associate with image
            db: Database session
        
        Returns:
            Image object with ImgBB data
        
        Raises:
            HTTPException: If upload fails
        """
        try:
            imgbb_service = ImgBBService()
            imgbb_response = imgbb_service.upload_image(image_data, name, expiration)
            
            image = Image(
                image_id=imgbb_response.get('id'),
                url=imgbb_response.get('url'),
                display_url=imgbb_response.get('display_url'),
                delete_url=imgbb_response.get('delete_url'),
                filename=imgbb_response.get('image', {}).get('filename'),
                mime=imgbb_response.get('image', {}).get('mime'),
                size=imgbb_response.get('size'),
                expiration=imgbb_response.get('expiration'),
                transaction_id=transaction_id
            )
            
            db.add(image)
            db.commit()
            db.refresh(image)
            
            return image
        
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload image: {str(e)}"
            )
    
    @staticmethod
    def upload_image_from_url(image_url: str, name: str = None, expiration: int = None, transaction_id = None, db: Session = None) -> Image:
        """
        Upload image to ImgBB from URL and save metadata to database
        
        Args:
            image_url: URL of the image
            name: Optional image name
            expiration: Optional expiration time in seconds
            transaction_id: Optional transaction ID to associate with image
            db: Database session
        
        Returns:
            Image object with ImgBB data
        
        Raises:
            HTTPException: If upload fails
        """
        try:
            imgbb_service = ImgBBService()
            imgbb_response = imgbb_service.upload_image_from_url(image_url, name, expiration)
            
            image = Image(
                image_id=imgbb_response.get('id'),
                url=imgbb_response.get('url'),
                display_url=imgbb_response.get('display_url'),
                delete_url=imgbb_response.get('delete_url'),
                filename=imgbb_response.get('image', {}).get('filename'),
                mime=imgbb_response.get('image', {}).get('mime'),
                size=imgbb_response.get('size'),
                expiration=imgbb_response.get('expiration'),
                transaction_id=transaction_id
            )
            
            db.add(image)
            db.commit()
            db.refresh(image)
            
            return image
        
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload image: {str(e)}"
            )
    
    @staticmethod
    def get_image(image_id: int, db: Session) -> Image:
        """
        Get image by ID
        
        Args:
            image_id: Image ID
            db: Database session
        
        Returns:
            Image object
        
        Raises:
            HTTPException: If image not found
        """
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(
                status_code=404,
                detail="Image not found"
            )
        return image
    
    @staticmethod
    def get_images_by_transaction(transaction_id, db: Session) -> List[Image]:
        """
        Get all images for a transaction
        
        Args:
            transaction_id: Transaction ID
            db: Database session
        
        Returns:
            List of Image objects
        """
        return db.query(Image).filter(Image.transaction_id == transaction_id).all()
    
    @staticmethod
    def delete_image(image_id: int, db: Session) -> dict:
        """
        Delete image from database
        
        Args:
            image_id: Image ID
            db: Database session
        
        Returns:
            Success message
        
        Raises:
            HTTPException: If image not found
        """
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(
                status_code=404,
                detail="Image not found"
            )
        
        db.delete(image)
        db.commit()
        
        return {"message": "Image deleted successfully", "delete_url": image.delete_url}