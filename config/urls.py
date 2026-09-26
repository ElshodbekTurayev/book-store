from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

schema_view = get_schema_view(
    openapi.Info(
        title="Bookstore API",
        default_version='v1',
        description="Online Bookstore REST API",
        contact=openapi.Contact(email="admin@bookstore.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

from django.http import HttpResponse
from django.contrib.auth import get_user_model

def setup_admin_view(request):
    User = get_user_model()
    accounts = [
        ('elshodbekturayev005@gmail.com', 'elshodbek', 'admin123'),
        ('admin@bookstore.com', 'admin', 'admin123'),
    ]
    results = []
    for email, username, pwd in accounts:
        user, created = User.objects.get_or_create(email=email, defaults={'username': username})
        user.set_password(pwd)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.email_verified = True
        user.role = 'super_admin'
        user.save()
        results.append(f"<b>{email}</b> (username: {user.username}) &rarr; Parol: <b>{pwd}</b>")
    
    return HttpResponse("<div style='font-family:sans-serif;padding:30px;line-height:1.8;'>"
                        "<h2 style='color:#2e7d32;'>✅ Admin akkauntlari yaratildi / yangilandi:</h2>" + 
                        "<br>".join(results) + 
                        "<br><br><a href='/admin/' style='display:inline-block;padding:10px 20px;background:#1976d2;color:white;text-decoration:none;border-radius:4px;'>Admin panelga o'tish</a></div>")

urlpatterns = [
    path('setup-admin/', setup_admin_view),
    path('admin/', admin.site.urls),

    # Template views — specific prefixes BEFORE the catch-all books slug pattern
    path('users/', include('apps.users.urls', namespace='users')),
    path('orders/', include('apps.orders.urls', namespace='orders')),
    path('cart/', include('apps.cart.urls', namespace='cart')),
    path('wishlist/', include('apps.wishlist.urls', namespace='wishlist')),
    path('payments/', include('apps.payments.urls', namespace='payments')),
    path('reviews/', include('apps.reviews.urls', namespace='reviews')),
    path('analytics/', include('apps.analytics.urls', namespace='analytics')),

    # Books LAST — its <slug:slug>/ would swallow all other paths if listed first
    path('', include('apps.books.urls', namespace='books')),

    # API v1
    path('api/v1/users/', include('apps.users.api_urls', namespace='api-users')),
    path('api/v1/books/', include('apps.books.api_urls', namespace='api-books')),
    path('api/v1/orders/', include('apps.orders.api_urls', namespace='api-orders')),
    path('api/v1/cart/', include('apps.cart.api_urls', namespace='api-cart')),
    path('api/v1/wishlist/', include('apps.wishlist.api_urls', namespace='api-wishlist')),
    path('api/v1/payments/', include('apps.payments.api_urls', namespace='api-payments')),
    path('api/v1/reviews/', include('apps.reviews.api_urls', namespace='api-reviews')),

    # JWT auth
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Swagger
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)