"""
Anti-spoofing service using DeepFace extract_faces with graceful fallback
"""
import io
import os
import cv2
import numpy as np
from tempfile import NamedTemporaryFile
from PIL import Image

# Try to import DeepFace, fallback if not available
try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
    print("✅ DeepFace imported successfully for anti-spoofing")
except ImportError as e:
    DEEPFACE_AVAILABLE = False
    print(f"⚠️ DeepFace not available: {e}")
    print("🔄 Anti-spoofing will use fallback method")

class AntiSpoofingService:
    def __init__(self):
        """Initialize anti-spoofing service"""
        self.deepface_available = DEEPFACE_AVAILABLE
        
    async def check_spoof(self, image_file):
        """
        Check if an uploaded image contains a spoofed face
        Uses DeepFace extract_faces with anti_spoofing=True if available
        
        Args:
            image_file: UploadFile from FastAPI
            
        Returns:
            dict: Results containing anti-spoofing check results
        """
        # Validate file extension
        if not image_file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
            return {
                "error": "Only JPG/PNG images are supported",
                "status_code": 400,
                "is_real": False
            }

        try:
            # Read and validate image
            contents = await image_file.read()
            img = Image.open(io.BytesIO(contents)).convert("RGB")
            img = img.resize((224, 224))  # Resize như code mẫu
            
            if self.deepface_available:
                return await self._check_with_deepface_extract_faces(img)
            else:
                return await self._check_with_fallback(img)
            
        except Exception as e:
            return {
                "error": f"Invalid image file: {str(e)}",
                "status_code": 400,
                "is_real": False
            }
    
    async def _check_with_deepface_extract_faces(self, img):
        """Check using DeepFace extract_faces with anti_spoofing=True"""
        try:
            # Save temporary image for DeepFace
            with NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                tmp_path = tmp.name
                img.save(tmp_path)
            
            try:
                # Use DeepFace extract_faces with anti_spoofing=True (như code mẫu)
                faces = DeepFace.extract_faces(
                    img_path=tmp_path,
                    enforce_detection=False,
                    align=False, 
                    anti_spoofing=True
                )
                
                if faces:
                    is_real = faces[0].get("is_real", False)
                    results = "REAL" if is_real else "SPOOF"
                    confidence = 0.8 if is_real else 0.2
                else:
                    results = "NO_FACE"
                    is_real = False
                    confidence = 0.0
                
                return {
                    "is_real": is_real,
                    "status_code": 200,
                    "message": results,
                    "confidence": confidence,
                    "method": "DeepFace extract_faces anti-spoofing"
                }
                
            finally:
                # Clean up temporary file
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
                    
        except Exception as e:
            print(f"DeepFace extract_faces error: {e}")
            # Fallback to basic method if DeepFace fails
            return await self._check_with_fallback(img)
    
    async def _check_with_fallback(self, img):
        """Fallback method using basic image analysis"""
        try:
            # Convert PIL to numpy for basic analysis
            img_array = np.array(img)
            height, width = img_array.shape[:2]
            
            # Basic checks for image quality and consistency  
            if height < 100 or width < 100:
                return {
                    "is_real": False,
                    "status_code": 200,
                    "message": "SPOOF (image too small)",
                    "confidence": 0.7,
                    "method": "Fallback - Size Check"
                }
            
            # Convert to grayscale for analysis
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            
            # Check image sharpness (blurry images might be photos of photos)
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            if laplacian_var < 100:  # Very blurry image
                return {
                    "is_real": False,
                    "status_code": 200,
                    "message": "SPOOF (image too blurry)",
                    "confidence": 0.6,
                    "method": "Fallback - Blur Detection"
                }
            
            # If passes basic checks, assume real
            return {
                "is_real": True,
                "status_code": 200,
                "message": "REAL (basic validation passed)",
                "confidence": 0.5,
                "method": "Fallback - Basic Validation"
            }
            
        except Exception as e:
            return {
                "is_real": True,  # Default to real if checks fail
                "status_code": 200,
                "message": f"REAL (fallback error: {str(e)})",
                "confidence": 0.3,
                "method": "Fallback - Error Recovery"
            }
                
spoof_detection_service = AntiSpoofingService()
