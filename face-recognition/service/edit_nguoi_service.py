from db.nguoi_repository import NguoiRepository
from db.models import Nguoi
from service.performance_monitor import track_operation
import os
import shutil
from datetime import datetime

nguoi_repo = NguoiRepository()

@track_operation("edit_nguoi")
def edit_nguoi_service(input, file=None):
    """
    Service để chỉnh sửa thông tin người theo class_id
    Có thể kèm theo file ảnh mới
    """
    try:
        # Kiểm tra class_id có tồn tại không (map to id)
        existing_nguoi = nguoi_repo.get_by_id(int(input.class_id))
        if not existing_nguoi:
            return {
                "success": False,
                "message": f"Không tìm thấy người với class_id={input.class_id}",
                "status_code": 404
            }
        
        # Xử lý file ảnh mới nếu có
        image_data = existing_nguoi.avatar_url  # bytes
        image_url = None  # Đường dẫn file để trả về response
        
        if file and file.filename:
            
            # Tạo thư mục uploads nếu chưa có
            upload_dir = "uploads/nguoi"
            os.makedirs(upload_dir, exist_ok=True)
            
            # Tạo tên file unique
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_extension = os.path.splitext(file.filename)[1]
            new_filename = f"{input.class_id}_{timestamp}{file_extension}"
            file_path = os.path.join(upload_dir, new_filename)
            
            # Lưu file và đọc bytes
            with open(file_path, "wb") as buffer:
                file_content = file.file.read()
                buffer.write(file_content)
                
            # Cập nhật image data (bytes) cho database
            image_data = file_content
            image_url = f"/{file_path}"
        
        # Tạo đối tượng Nguoi với thông tin mới
        updated_nguoi = Nguoi(
            id=int(input.class_id),
            username=existing_nguoi.username if hasattr(existing_nguoi, 'username') else None,
            pin=existing_nguoi.pin if hasattr(existing_nguoi, 'pin') else None,
            full_name=getattr(input, 'full_name', None) or existing_nguoi.full_name,
            age=getattr(input, 'age', None) or existing_nguoi.age,
            address=getattr(input, 'address', None) or existing_nguoi.address,
            phone=existing_nguoi.phone if hasattr(existing_nguoi, 'phone') else None,
            gender=getattr(input, 'gender', None) or existing_nguoi.gender,
            role=existing_nguoi.role if hasattr(existing_nguoi, 'role') else 'user',
            shift=existing_nguoi.shift if hasattr(existing_nguoi, 'shift') else 'day',
            status=existing_nguoi.status if hasattr(existing_nguoi, 'status') else 'working',
            avatar_url=image_data,
            created_at=existing_nguoi.created_at if hasattr(existing_nguoi, 'created_at') else None,
            updated_at=None
        )

        # Cập nhật vào database
        affected_rows = nguoi_repo.update_by_id(int(input.class_id), updated_nguoi)
        
        if affected_rows > 0:
            
            # Tạo response an toàn cho JSON serialization
            result = {
                "success": True,
                "message": f"Đã cập nhật thông tin người với class_id={input.class_id}",
                "class_id": input.class_id,
                "status": "success",
                "updated_info": {
                    "full_name": getattr(input, 'full_name', None),
                    "age": getattr(input, 'age', None),
                    "gender": getattr(input, 'gender', None),
                    "address": getattr(input, 'address', None),
                    "image_path": image_url if image_url else None
                }
            }
            
            if file and file.filename:
                result["image_uploaded"] = True
                result["new_image_path"] = image_url
            
            return result
        else:
            return {
                "success": False,
                "message": f"Không thể cập nhật thông tin cho class_id={input.class_id}",
                "status_code": 500
            }
            
    except Exception as e:
        print(f"Lỗi khi cập nhật class_id={input.class_id}: {e}")
        return {
            "success": False,
            "message": f"Lỗi cập nhật thông tin: {str(e)}",
            "status_code": 500
        }
