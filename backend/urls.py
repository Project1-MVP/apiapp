from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from tenant_management.views import TenantViewSet, TenantUserViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'tenants', TenantViewSet)
router.register(r'users', TenantUserViewSet, basename='tenant-users')


@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'detail': 'CSRF cookie set'})

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="My API description",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="Awesome License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

from rest_framework.permissions import AllowAny, IsAuthenticated
from tenant_management.permissions import IsTenantOwner

# Public URLs (Before Authentication)
urlpatterns = [
    path('api/tenants/create/', TenantViewSet.as_view({'post': 'create'}), name='tenant-create'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   # path('api/password/forgot/', PasswordResetView.as_view(), name='password-reset'),
]

# Protected URLs (After Authentication)
urlpatterns += [
    path('inventory_svs/', include('inventory_svs.urls')),
    path('orders_svs/', include('orders_svs.urls')),
]

# Tenant Owner Only URLs
tenant_management_urls = [
    path('api/tenants/<uuid:tenant_id>/users/', 
         TenantUserViewSet.as_view({'post': 'create', 'get': 'list'}),
         name='tenant-users'),
    path('api/tenants/<uuid:tenant_id>/users/<uuid:pk>/',
         TenantUserViewSet.as_view({'put': 'update', 'delete': 'destroy'}),
         name='tenant-user-detail'),
]

urlpatterns += [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('get-csrf-token/', get_csrf_token, name='get-csrf-token'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)