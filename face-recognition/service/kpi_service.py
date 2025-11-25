from db.nguoi_repository import NguoiRepository

nguoi_repo = NguoiRepository()


def query_kpis_service(date: str = None, month: str = None, full_name: str = None, limit: int = 100, offset: int = 0):
    try:
        kpis = nguoi_repo.query_kpis(date=date, month=month, full_name=full_name, limit=limit, offset=offset)
        # Convert to dicts
        result = []
        for k in kpis:
            item = k.to_dict() if hasattr(k, 'to_dict') else k.__dict__.copy()
            # Ensure date is serializable
            if 'date' in item and item['date'] is not None:
                try:
                    item['date'] = item['date'].isoformat()
                except Exception:
                    item['date'] = str(item['date'])
            # Attach user_name from nhanvien
            try:
                nguoi = nguoi_repo.get_by_id(item.get('user_id'))
                item['user_name'] = getattr(nguoi, 'username', None) if nguoi else None
            except Exception:
                item['user_name'] = None
            result.append(item)
        return {"success": True, "kpis": result}
    except Exception as e:
        return {"success": False, "message": f"Lỗi khi truy vấn KPI: {e}", "status_code": 500}


def query_kpis_for_user_service(user_id: int, date: str = None, month: str = None, limit: int = 100, offset: int = 0):
    try:
        kpis = nguoi_repo.query_kpis(date=date, month=month, user_id=user_id, limit=limit, offset=offset)
        result = []
        # If user_id provided, fetch username once
        user_name = None
        if user_id is not None:
            try:
                nguoi = nguoi_repo.get_by_id(user_id)
                user_name = getattr(nguoi, 'username', None) if nguoi else None
            except Exception:
                user_name = None

        for k in kpis:
            item = k.to_dict() if hasattr(k, 'to_dict') else k.__dict__.copy()
            if 'date' in item and item['date'] is not None:
                try:
                    item['date'] = item['date'].isoformat()
                except Exception:
                    item['date'] = str(item['date'])
            # Attach user_name (from cached user_name if available, otherwise lookup)
            if user_name is not None:
                item['user_name'] = user_name
            else:
                try:
                    nguoi = nguoi_repo.get_by_id(item.get('user_id'))
                    item['user_name'] = getattr(nguoi, 'username', None) if nguoi else None
                except Exception:
                    item['user_name'] = None
            result.append(item)
        return {"success": True, "kpis": result}
    except Exception as e:
        return {"success": False, "message": f"Lỗi khi truy vấn KPI cho user {user_id}: {e}", "status_code": 500}
