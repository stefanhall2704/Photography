"""
URL configuration for hallsPhotography project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include, path
from photography import views

urlpatterns = [
    path("admin", admin.site.urls),
    path("o/", include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.sign_up, name='signup'),
    path('accounts/', include('allauth.urls')),
    path('', views.home, name='home'),
    path('download/', views.download, name='download'),
    path('upload/', views.upload, name='upload'),
]
    # path("admin", admin.site.urls),
    # path("o/", include('oauth2_provider.urls', namespace='oauth2_provider')),
    # path('download_view/', views.download, name='download'),