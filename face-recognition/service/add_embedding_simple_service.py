from fastapi import APIRouter, File, UploadFile, Form, Depends
from fastapi.responses import JSONResponse
import numpy as np
import cv2
from service.shared_instances import get_extractor, get_faiss_manager, get_faiss_lock
from db.nguoi_repository import NguoiRepository
from db.models import Nguoi
from Depend.depend import AddEmbeddingInput, SimpleAddEmbeddingInput
from service.predict_service import predict_service
from service.add_embedding_service import add_embedding_service as core_add_embedding_service

add_router = APIRouter() 

# ✅ Sử dụng shared instances
extractor = get_extractor()
faiss_manager = get_faiss_manager()
faiss_lock = get_faiss_lock()
nguoi_repo = NguoiRepository()

async def simple_add_embedding_service(file: UploadFile = File(...)):
    """
    Simplified service - chỉ cần file upload, tất cả thông tin khác tự động generate
    """
    # Tạo SimpleAddEmbeddingInput với tất cả giá trị None
    input = SimpleAddEmbeddingInput(
        image_id=None,
        image_path=None,
        class_id=None,
        full_name=None,
        gender=None,
        age=None,
        address=None
    )
    
    # Sử dụng lại logic từ add_embedding_service (delegate)
    return await core_add_embedding_service(input, file)

async def add_embedding_service(
    input: SimpleAddEmbeddingInput = Depends(SimpleAddEmbeddingInput.as_form),
    file: UploadFile = File(...)
):
    # Delegate to the centralized implementation
    return await core_add_embedding_service(input, file)

# fe cần phải truyền về api toàn bộ trường, không được bỏ trống thông tin
# nếu như chỉ thêm ảnh (class_id đã tồn tại) --> điền dữ liệu rác