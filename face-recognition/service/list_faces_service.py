from db.nguoi_repository import NguoiRepository

nguoi_repo = NguoiRepository()


def list_faces_service(user_id: int, include_image_base64: bool = False):
    try:
        faces = nguoi_repo.get_khuonmats_by_user(int(user_id))
        result = [f.to_dict(include_image_base64=include_image_base64) for f in faces]
        return {"success": True, "faces": result}
    except Exception as e:
        return {"success": False, "message": f"Lỗi khi lấy danh sách khuôn mặt: {e}", "status_code": 500}
