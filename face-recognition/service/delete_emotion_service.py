from db.nguoi_repository import NguoiRepository

nguoi_repo = NguoiRepository()


def delete_emotion_service(emotion_id: int):
    try:
        affected = nguoi_repo.delete_emotion_by_id(int(emotion_id))
        if affected > 0:
            return {"success": True, "message": "Xóa emotion log thành công"}
        else:
            return {"success": False, "message": "Không tìm thấy bản ghi hoặc không thể xóa", "status_code": 404}
    except Exception as e:
        return {"success": False, "message": f"Lỗi khi xóa emotion log: {e}", "status_code": 500}
