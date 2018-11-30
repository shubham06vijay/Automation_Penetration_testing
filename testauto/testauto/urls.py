"""testauto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'testauto'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^enum_vul_services/', views.enum_vul_services, name='enum_vul_services'),
    url(r'^publicdata/$', views.publicdata, name='publicdata'),
    url(r'^week_authentication/', views.weak_authentication, name='weak_authentication'),
    url(r'^main/', views.main, name='main'),
    url(r'^software_update/', views.software_update, name='software_update'),
    url(r'^admin/', admin.site.urls),
    url(r'^metadata/', views.metadata, name='metadata'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
