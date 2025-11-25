from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
import numpy as np
import cv2
import time
from service.face_query_service import query_face_service as face_query_service
from service.add_embedding_simple_service import simple_add_embedding_service
from service.anti_spoofing_service import spoof_detection_service
from service.checkin_service import checkin_service as svc_checkin
from service.checkout_service import checkout as svc_checkout

router = APIRouter()

@router.post(
    '/query',
    summary="Nhận diện khuôn mặt với Auto-Add",
    description="""
    **Nhận diện khuôn mặt từ ảnh tải lên với tính năng tự động thêm mới**
    
    API này sẽ:
    - Nhận ảnh chứa khuôn mặt từ người dùng
    - Trích xuất đặc trưng khuôn mặt từ ảnh
    - Tìm kiếm khuôn mặt tương tự trong cơ sở dữ liệu
    - **🚀 TỰ ĐỘNG THÊM MỚI**: Nếu không tìm thấy (score < 0.5), tự động gọi API `/add_embedding_simple` để thêm người mới
    - Trả về thông tin chi tiết của người được nhận diện hoặc thông tin người vừa được thêm
    
    **Tính năng mới:**
    - 🔍 **Tìm kiếm trước**: Kiểm tra xem có người phù hợp không
    - ➕ **Tự động thêm**: Nếu không tìm thấy, tự động tạo profile mới với AI prediction
    - 📊 **Thống kê**: Cho biết đây là kết quả tìm kiếm hay người mới được thêm
    
    **Lưu ý:**
    - Ảnh phải chứa ít nhất 1 khuôn mặt rõ ràng
    - Hỗ trợ các định dạng: JPG, PNG, WEBP
    - Kích thước file tối đa: 10MB
    - Threshold nhận diện: 0.5 (có thể điều chỉnh)
    """,
    response_description="Kết quả nhận diện khuôn mặt hoặc thông tin người mới được thêm tự động",
    tags=["👤 Nhận Diện Khuôn Mặt"]
)
async def query_face(
    image: UploadFile = File(
        ..., 
        description="File ảnh chứa khuôn mặt cần nhận diện (JPG, PNG, WEBP)",
        media_type="image/*"
    )
):
    """
    🔍 Nhận diện khuôn mặt với tính năng auto-add
    
    1. Kiểm tra ảnh giả mạo
    2. Nếu là ảnh thật, tiến hành tìm kiếm
    3. Nếu không tìm thấy, tự động thêm mới
    4. Trả về kết quả tương ứng
    """
    # Bước 1: Kiểm tra chống giả mạo
    await image.seek(0)
    spoof_check = await spoof_detection_service.check_spoof(image)

    # Bước 2: Thực hiện query face bình thường
    # ensure file pointer is at beginning because spoof_detection_service may have read the file
    await image.seek(0)
    result = await face_query_service(image)

    # Bước 3: Kiểm tra kết quả
    if result and not result.get("error"):
        # Có kết quả tìm thấy - chỉ trả về thông tin cơ bản
        basic_result = {
            "action": "face_recognized",
            "message": f"Đã nhận diện thành công với score: {result.get('score', 'N/A')}",
            "class_id": result.get("class_id"),
            "image_id": result.get("image_id"),
            "score": result.get("score")
        }

        # Thêm thông tin người nếu có
        if result.get("nguoi"):
            nguoi_info = result["nguoi"]
            basic_result.update({
                "full_name": nguoi_info.get("full_name"),
                "age": nguoi_info.get("age"),
                "gender": nguoi_info.get("gender"),
                "avatar_base64": nguoi_info.get("avatar_base64")
            })

        # Thêm trường cảm xúc nếu service trả về
        if 'emotion' in result:
            basic_result['emotion'] = result.get('emotion')
            print(f"[debug] Adding emotion to response: {basic_result['emotion']}")
        if result.get('matched_image_emotion'):
            basic_result['matched_image_emotion'] = result.get('matched_image_emotion')

        result = basic_result
        status_code = 200
    else:
        # Không tìm thấy hoặc có lỗi, thực hiện auto-add
        await image.seek(0)
        add_result = await simple_add_embedding_service(image)

        if add_result.get("status_code") and add_result["status_code"] != 200:
            # Có lỗi khi thêm mới
            result = {
                "action": "auto_add_failed",
                "error": f"Không tìm thấy kết quả và thêm mới thất bại: {add_result.get('message', 'Unknown error')}"
            }
            status_code = add_result.get("status_code", 500)
        else:
            # Thêm mới thành công - chỉ trả về thông tin cơ bản
            nguoi_info = add_result.get("nguoi_info", {})
            result = {
                "action": "auto_added",
                "message": "Không tìm thấy kết quả phù hợp, đã tự động thêm người mới vào hệ thống",
                "class_id": add_result.get("class_id"),
                "image_id": add_result.get("image_id"),
                "full_name": nguoi_info.get("full_name"),
                "age": nguoi_info.get("age"),
                "gender": nguoi_info.get("gender"),
                "avatar_base64": nguoi_info.get("avatar_base64"),
                "predict_used": add_result.get("predict_used", False)
            }
            status_code = 200
    
    # Loại bỏ status_code khỏi response body
    if "status_code" in result:
        result = {k: v for k, v in result.items() if k != "status_code"}
    
    return JSONResponse(content=result, status_code=status_code)


@router.post('/query/checkin', summary='Nhận diện và tạo check-in nếu match')
async def query_and_checkin(
    image: UploadFile = File(..., description="File ảnh chứa khuôn mặt cần nhận diện", media_type="image/*")
):
    await image.seek(0)
    spoof_check = await spoof_detection_service.check_spoof(image)
    await image.seek(0)
    result = await face_query_service(image)
    if result and not result.get('error'):
        # only proceed if we have a class_id
        class_id = result.get('class_id')
        if class_id:
            try:
                checkin_res = svc_checkin(user_id=int(class_id), edited_by=None, note=None)
            except Exception as e:
                checkin_res = {"success": False, "message": f"Lỗi khi checkin: {e}"}
        else:
            checkin_res = {"success": False, "message": "Không xác định class_id"}
        # merge results
        merged = {**result, 'checkin': checkin_res}
        return JSONResponse(content=merged, status_code=200)
    else:
        return JSONResponse(content={"success": False, "message": "Không nhận diện được user"}, status_code=404)


@router.post('/query/checkout', summary='Nhận diện và tạo check-out nếu match')
async def query_and_checkout(
    image: UploadFile = File(..., description="File ảnh chứa khuôn mặt cần nhận diện", media_type="image/*")
):
    await image.seek(0)
    spoof_check = await spoof_detection_service.check_spoof(image)
    await image.seek(0)
    result = await face_query_service(image)
    if result and not result.get('error'):
        class_id = result.get('class_id')
        if class_id:
            try:
                checkout_res = svc_checkout(user_id=int(class_id), edited_by=None, note=None)
            except Exception as e:
                checkout_res = {"success": False, "message": f"Lỗi khi checkout: {e}"}
        else:
            checkout_res = {"success": False, "message": "Không xác định class_id"}
        merged = {**result, 'checkout': checkout_res}
        return JSONResponse(content=merged, status_code=200)
    else:
        return JSONResponse(content={"success": False, "message": "Không nhận diện được user"}, status_code=404)
