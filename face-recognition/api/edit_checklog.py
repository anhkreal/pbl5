from fastapi import APIRouter, Depends, Path, Body
from auth.mysql_auth import get_current_user_mysql
from service.edit_checklog_service import edit_checklog_by_id, edit_checklog_by_user_and_date
from db.nguoi_repository import NguoiRepository

router = APIRouter()
nguoi_repo = NguoiRepository()


def _resolve_edited_by(current_user):
    # current_user is username string in this auth implementation
    if not current_user:
        return None
    try:
        nguoi = nguoi_repo.get_by_username(current_user)
        return nguoi.id if nguoi else None
    except Exception:
        return None


@router.put('/edit-checklog/{id}', summary='Chỉnh sửa checklog theo id (status)')
def edit_checklog_id(id: int = Path(...), status: str = Body(...), note: str = Body(None), current_user=Depends(get_current_user_mysql)):
    edited_by = _resolve_edited_by(current_user)
    res = edit_checklog_by_id(row_id=id, status=status, edited_by=edited_by, note=note)
    return res


@router.put('/edit-checklog', summary='Chỉnh sửa checklog theo user_id + date')
def edit_checklog_user_date(user_id: int = Body(...), date: str = Body(...), status: str = Body(...), note: str = Body(None), current_user=Depends(get_current_user_mysql)):
    edited_by = _resolve_edited_by(current_user)
    res = edit_checklog_by_user_and_date(user_id=user_id, date=date, status=status, edited_by=edited_by, note=note)
    return res
