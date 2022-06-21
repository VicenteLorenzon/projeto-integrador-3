from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#CUSTOMIZAÇÕES DO ADMIN PADRÃO
admin.site.site_header = 'Administração do pet shop'
admin.site.index_title = 'Administração do pet shop'
admin.site.site_title = 'Administração do pet shop'
