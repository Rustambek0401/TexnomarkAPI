from django.conf.urls.static import static
from rest_framework.authtoken import views
from config import settings
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('texnomark-uz/', include("texnomark.urls")),
    path('api-token-auth/', views.obtain_auth_token),
## JWTAuthentication

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('debug',include(debug_toolbar.urls)),
    ]