from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import JSONResponse
from service.add_face_service import add_face_service
from service.list_faces_service import list_faces_service
from service.delete_faces_service import delete_faces_for_user

faces_router = APIRouter()


@faces_router.post('/faces', summary='Thêm khuôn mặt cho người (ảnh + user_id) (multipart/form-data)')
def add_face(user_id: int = Form(...), image: UploadFile = File(...)):
    # Read uploaded file bytes here and pass blob to service
    try:
        try:
            image.file.seek(0)
        except Exception:
            pass
        image_bytes = image.file.read()
    except Exception as e:
        return JSONResponse(content={'success': False, 'message': f'Không đọc được file ảnh: {e}'}, status_code=400)

    # no authentication required for adding faces
    result = add_face_service(user_id, image_bytes)
    status_code = result.get('status_code', 200)
    body = {k: v for k, v in result.items() if k != 'status_code'}
    return JSONResponse(content=body, status_code=status_code)



@faces_router.get('/faces/{user_id}', summary='Lấy danh sách khuôn mặt của nhân viên (yêu cầu đăng nhập)')
def list_faces(user_id: int, include_image_base64: bool = False):
    # no authentication required for listing faces
    result = list_faces_service(user_id, include_image_base64)
    status_code = result.get('status_code', 200)
    body = {k: v for k, v in result.items() if k != 'status_code'}
    return JSONResponse(content=body, status_code=status_code)


@faces_router.delete('/faces/{user_id}', summary='Xóa tất cả khuôn mặt của user (FAISS + DB)')
def delete_faces(user_id: int):
    result = delete_faces_for_user(user_id)
    status_code = result.get('status_code', 200)
    body = {k: v for k, v in result.items() if k != 'status_code'}
    return JSONResponse(content=body, status_code=status_code)
