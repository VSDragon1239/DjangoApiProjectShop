# shop/api.py
from ninja import NinjaAPI, Router
from ninja.security import HttpBearer
from rest_framework_simplejwt.tokens import AccessToken
from django.db.models import Q

from .models import User, Product
from .schemas import UserOut, ProductOut, ProductFilter

api = NinjaAPI()  # главный API


# Класс для JWT‑аутентификации нужно объявить первым
class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            validated = AccessToken(token)
            user = User.objects.get(id=validated['user_id'])
            request.user = user
            return user
        except Exception:
            return None


# создаём Router для защищённых маршрутов
secured_router = Router(auth=JWTAuth())


class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            validated = AccessToken(token)
            user = User.objects.get(id=validated['user_id'])
            request.user = user
            return user
        except Exception:
            return None


# Эндпоинт для менеджеров: список подчинённых
@secured_router.get("/subordinates", response=list[UserOut])
def list_subordinates(request):
    if request.user.role != 'manager':
        return {"detail": "Forbidden"}, 403
    return User.objects.filter(manager=request.user)


# Эндпоинт продуктов с фильтрами
@secured_router.get("/products", response=list[ProductOut])
def list_products(request, filters: ProductFilter = ProductFilter()):
    qs = Product.objects.all()
    if filters.min_price is not None:
        qs = qs.filter(price__gte=filters.min_price)
    if filters.max_price is not None:
        qs = qs.filter(price__lte=filters.max_price)
    if filters.search:
        qs = qs.filter(
            Q(name__icontains=filters.search) |
            Q(description__icontains=filters.search)
        )
    return qs


# встраиваем secured_router в главный api
api.add_router("/secured/", secured_router)
