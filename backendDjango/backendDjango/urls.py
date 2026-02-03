from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/user/', include('main.routes.user.urls')),
    
    path('api/article/', include('main.routes.articles.urls'))]