from db import nguoi_repository

nguoi_repository = nguoi_repository.NguoiRepository()

def get_nguoi_info_service(
    query: str = "",
    page: int = 1,
    page_size: int = 15,
    sort_by: str = "full_name_asc"
):
    try:
        result = nguoi_repository.search_nguoi_paged(query, page, page_size, sort_by)
        return {
            "nguoi_list": [n.to_dict(include_avatar_base64=True) for n in result['nguoi_list']],
            "total": result['total']
        }
    except Exception as e:
        return {"error": str(e)}
