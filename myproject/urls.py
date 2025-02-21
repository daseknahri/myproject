from django.contrib import admin
from django.urls import include, path
from rent.admin import admin_site
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin_site.urls),  # Keep admin outside of i18n_patterns
    path('i18n/', include('django.conf.urls.i18n')),  # Language switcher
]

# Only wrap translatable user-facing URLs inside i18n_patterns
urlpatterns += i18n_patterns(
    path('', include('rent.urls')),  # Only wrap rent.urls inside i18n_patterns
)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)