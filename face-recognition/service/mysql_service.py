from db.nguoi_repository import NguoiRepository


def get_all_nguoi_service():
    """Return all people using the repository (maps to `nhanvien`)."""
    repo = NguoiRepository()
    try:
        nguoi_list = repo.search_nguoi()
        return [n.to_dict(include_avatar_base64=True) for n in nguoi_list]
    except Exception as e:
        # Return empty list or raise depending on expected behavior
        print(f"Error fetching nguoi list: {e}")
        return []
