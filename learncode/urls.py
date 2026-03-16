from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('courses.urls')),
]
if getattr(settings, 'DEBUG', False):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'courses.views.page_not_found_view'
handler500 = 'courses.views.server_error_view'
