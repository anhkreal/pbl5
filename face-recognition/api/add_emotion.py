from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import JSONResponse
from service.add_emotion_service import add_emotion_service

add_emotion_router = APIRouter()


@add_emotion_router.post('/add-emotion', summary='Gửi log cảm xúc (ảnh + emotion_type + camera_id + confidence)')
def add_emotion(
    user_id: int = Form(None),
    camera_id: int = Form(None),
    emotion_type: str = Form(...),
    confidence: float = Form(...),
    image: UploadFile = File(None),
    note: str = Form(None),
    # no authentication required
    current_user: str = None
):
    result = add_emotion_service(user_id=user_id, camera_id=camera_id, emotion_type=emotion_type, confidence=confidence, image_file=image, note=note)
    status_code = result.get('status_code', 200)
    body = {k: v for k, v in result.items() if k != 'status_code'}
    return JSONResponse(content=body, status_code=status_code)
