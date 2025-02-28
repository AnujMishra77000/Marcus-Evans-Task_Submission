from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from User_app.api.views import registration_view, logout_view


urlpatterns = [
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
]