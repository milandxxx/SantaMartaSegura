from .lugares import router as lugares_router
from .alertas import router as alertas_router
from .emergencias import router as emergencias_router
from .admin import router as admin_router

__all__ = [
    "lugares_router",
    "alertas_router",
    "emergencias_router",
    "admin_router",
]