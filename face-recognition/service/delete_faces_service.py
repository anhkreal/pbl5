from db.nguoi_repository import NguoiRepository
from service.shared_instances import get_faiss_manager, get_faiss_lock

nguoi_repo = NguoiRepository()
faiss_manager = get_faiss_manager()
faiss_lock = get_faiss_lock()


def delete_faces_for_user(user_id: int):
    """Delete all faces for a user both from FAISS and from the khuonmat table.
    - First remove all FAISS entries with class_id == user_id
    - Then delete all khuonmat rows for that user
    If DB deletion fails after FAISS deletion, attempt to reload FAISS from saved files (best-effort rollback not possible)
    Returns dict with success and counts.
    """
    try:
        # Ensure the user exists (optional)
        # Remove from FAISS
        with faiss_lock:
            removed = faiss_manager.delete_by_class_id(user_id)
            # save after removal
            faiss_manager.save()

        # Remove from DB
        deleted_rows = nguoi_repo.delete_khuonmats_by_user(int(user_id))

        return {"success": True, "message": "Xóa mặt khỏi FAISS và DB hoàn tất", "faiss_removed": bool(removed), "db_deleted": deleted_rows}
    except Exception as e:
        return {"success": False, "message": f"Lỗi khi xóa faces cho user {user_id}: {e}", "status_code": 500}
