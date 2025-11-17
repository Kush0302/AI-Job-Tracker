"""
URL configuration for config project.

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
from django.urls import path, include # include lets you import URLs from another app(tracker)
from tracker import views # import your job_list view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from tracker.views import register_user
from rest_framework_simplejwt.views import(TokenObtainPairView, TokenRefreshView,)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.job_list, name='home'), # show job list at root URL
    path('jobs/', include('tracker.urls')), #'' means "for the root URL and everything under it"
    path('', include('tracker.urls')), 
    path("api/", include("tracker.urls")), 
    path("accounts/login/", auth_views.LoginView.as_view(template_name="login.html")), 
    path('accounts/logout/', auth_views.LogoutView.as_view()),
    path('accounts/signup/', register_user, name="signup"),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)