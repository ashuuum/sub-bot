from aiogram import Router

# Импортируем роутеры из отдельных файлов
from .start import router as start_router
from .add_sub import router as add_subscription_router
from .list_sub import router as list_subscriptions_router
from .del_sub import router as remove_subscription_router
from .edit_sub import router as edit_subscription_router

# Главный роутер, объединяющий все
router = Router()
router.include_router(start_router)
router.include_router(add_subscription_router)
router.include_router(list_subscriptions_router)
router.include_router(remove_subscription_router)
router.include_router(edit_subscription_router)