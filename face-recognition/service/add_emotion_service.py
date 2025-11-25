from db.nguoi_repository import NguoiRepository

nguoi_repo = NguoiRepository()


def add_emotion_service(user_id: int = None, camera_id: int = None, emotion_type: str = None, confidence: float = None, image_file=None, note: str = None):
    try:
        # read image bytes defensively
        image_bytes = None
        if image_file is not None:
            try:
                image_file.file.seek(0)
            except Exception:
                pass
            image_bytes = image_file.file.read()

        rowid = nguoi_repo.add_emotion_log(user_id=user_id, camera_id=camera_id, emotion_type=emotion_type, confidence=confidence, image_bytes=image_bytes, note=note)
        if rowid:
            return {"success": True, "message": "Đã lưu log cảm xúc", "id": rowid}
        else:
            return {"success": False, "message": "Không thể lưu log cảm xúc", "status_code": 500}
    except Exception as e:
        return {"success": False, "message": f"Lỗi khi lưu log: {e}", "status_code": 500}
