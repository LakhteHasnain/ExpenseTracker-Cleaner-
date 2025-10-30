import requests
import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class ImgBBService:
    BASE_URL = "https://api.imgbb.com/1/upload"
    
    def __init__(self):
        self.api_key = os.getenv("IMAGE_API_KEY")
        if not self.api_key:
            raise ValueError("IMAGE_API_KEY not found in environment variables")
    
    def upload_image(
        self,
        image_data: bytes,
        name: Optional[str] = None,
        expiration: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Upload an image to ImgBB
        
        Args:
            image_data: Binary image data
            name: Optional name for the image
            expiration: Optional expiration time in seconds (60-15552000)
        
        Returns:
            Dictionary containing the ImgBB API response data
        
        Raises:
            requests.RequestException: If the API call fails
            ValueError: If the response indicates an error
        """
        files = {
            'image': image_data
        }
        
        data = {
            'key': self.api_key
        }
        
        if name:
            data['name'] = name
        
        if expiration:
            if not (60 <= expiration <= 15552000):
                raise ValueError("Expiration must be between 60 and 15552000 seconds")
            data['expiration'] = expiration
        
        try:
            response = requests.post(self.BASE_URL, files=files, data=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if not result.get('success'):
                raise ValueError(f"ImgBB API error: {result.get('error', 'Unknown error')}")
            
            return result.get('data', {})
        
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to upload image to ImgBB: {str(e)}")
    
    def upload_image_from_url(
        self,
        image_url: str,
        name: Optional[str] = None,
        expiration: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Upload an image to ImgBB from a URL
        
        Args:
            image_url: URL of the image to upload
            name: Optional name for the image
            expiration: Optional expiration time in seconds (60-15552000)
        
        Returns:
            Dictionary containing the ImgBB API response data
        
        Raises:
            requests.RequestException: If the API call fails
            ValueError: If the response indicates an error
        """
        data = {
            'key': self.api_key,
            'image': image_url
        }
        
        if name:
            data['name'] = name
        
        if expiration:
            if not (60 <= expiration <= 15552000):
                raise ValueError("Expiration must be between 60 and 15552000 seconds")
            data['expiration'] = expiration
        
        try:
            response = requests.post(self.BASE_URL, data=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if not result.get('success'):
                raise ValueError(f"ImgBB API error: {result.get('error', 'Unknown error')}")
            
            return result.get('data', {})
        
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to upload image to ImgBB: {str(e)}")
