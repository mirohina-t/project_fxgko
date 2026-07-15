"""
URL configuration for irina_proj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
import irina_app.views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/news/<int:news_id>/', irina_app.views.news_detail_api, name='news_detail_api'), # API для модалки
   
    path('news/', irina_app.views.news_list, name="news_list"),
    path('news/<int:news_id>/', irina_app.views.news_detail_page, name='news_detail_page'), # Отдельная страница новости
    
    re_path(r'starts/', irina_app.views.starts, name="all_starts"),
    
    path('registration/<int:start_id>/', irina_app.views.registration_view, name='registration'),
    path('get-category-items/<int:category_id>/', irina_app.views.get_category_items, name='get_category_items'),
    path('login/', irina_app.views.user_login, name='user_login'),
    path('admin-panel/', irina_app.views.admin_panel, name='admin_panel'),
    path('logout/', irina_app.views.user_logout, name='user_logout'),
    # path('registration-success/<int:start_id>/', irina_app.views.registration_success, name='registration_success'),
    re_path(r'privacy/', irina_app.views.privacy, name="privacy"),
    re_path(r'info/', irina_app.views.info, name="info"),
    
   
    path(r'', irina_app.views.index, name="index"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
