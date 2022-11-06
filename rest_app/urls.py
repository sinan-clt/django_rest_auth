from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('register', views.Register.as_view()),
    path('login', views.UserLogin.as_view()),
    path('user_details', views.UserDetails.as_view()),
    path('registerAndLogin', views.RegisterandLogin.as_view()),
    
    path('addProducts', views.addProducts.as_view()),
    path('editProducts/<int:id>', views.editProducts.as_view()),
    path('deleteProducts/<int:id>', views.deleteProducts.as_view()),

    path('addToCart', views.addTocart.as_view()),
    path('fetchCart', views.fetchCart.as_view()),

]