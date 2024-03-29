from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ibc_financeiro.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

# Executa o método quando ocorre erro
handler404 = 'ibc_financeiro.views.errors'      # 404