from django.urls import path, include
from . import views
from django.conf import settings
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('signup/', views.handleSignup, name='signup'),
    path('login/', views.handleLogin, name='login'),
    path('logout/', views.handleLogout, name='logout'),
    path('edit/<int:pk>', views.editProfile, name='edituser'),
    path('delete/<int:pk>', views.deleteProfile, name='deleteuser'),
    path('forget/', views.handleforget, name='forget'),
    path('reset/<int:pk>', views.handlereset, name='reset'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)