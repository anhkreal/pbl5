from fastapi import APIRouter, Path
from service.checkout_service import checkout as checkout_service
from db.nguoi_repository import NguoiRepository

router = APIRouter()
nguoi_repo = NguoiRepository()


def _resolve_user_id(current_user):
    # current_user may be a username or None; if None return None
    if not current_user:
        return None
    try:
        nguoi = nguoi_repo.get_by_username(current_user)
        return nguoi.id if nguoi else None
    except Exception:
        return None


@router.post('/checkout')
def do_checkout():
    # No authentication required: perform checkout for anonymous/current context is unsupported
    # Caller must supply the intended user via other means; here we return an informative error
    return {"success": False, "message": "Endpoint requires a user id; use /checkout/{id} for checkout by user id", "status_code": 400}


@router.post('/checkout/{id}', summary='Checkout user by id')
def do_checkout_for_user(id: int = Path(...)):
    # No authentication required for this endpoint per request; edited_by will be None
    result = checkout_service(user_id=int(id), edited_by=None)
    return result
