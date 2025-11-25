import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from service.kpi_service import query_kpis_service, query_kpis_for_user_service
import json
print('ALL KPI sample:')
print(json.dumps(query_kpis_service(limit=2), indent=2))
print('\nKPI for user 2:')
print(json.dumps(query_kpis_for_user_service(2, limit=2), indent=2))
