import os
import sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
	sys.path.insert(0, ROOT)

import json
from service.kpi_service import query_kpis_service

res = query_kpis_service(limit=1)
print(json.dumps(res))
