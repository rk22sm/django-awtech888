from django.urls import path
from . import views
from .views import CustomLoginView, CustomSignupView



app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', CustomLoginView.as_view(), name='account_login'),
    path('signup/', CustomSignupView.as_view(), name='account_signup'),
    path('logout/', views.Mylogout, name='account_logout'),
    # path('forgot_pass/', views.signup, name='signup'),    
]
