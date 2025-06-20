from fastapi import APIRouter
from api.v1.endpoints.category import router as category_router
from api.v1.endpoints.assignment import router as assignment_router
from api.v1.endpoints.asset import router as asset_router
from api.v1.endpoints.request import router as request_router
from api.v1.endpoints.user import router as user_router
from api.v1.endpoints.report import router as report_router
from api.v1.endpoints.auth import router as auth_router
# from api.v1.endpoints.user import router as user_router
# etc...

router = APIRouter(prefix="/v1")

router.include_router(auth_router)
router.include_router(category_router)
router.include_router(assignment_router)
router.include_router(asset_router)
router.include_router(request_router)
router.include_router(user_router)
router.include_router(report_router)
# router.include_router(user_router)
# etc...
