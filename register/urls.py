from django.urls import path

from . import views
from .views import user_list

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('user-list/', user_list, name='user_list'),
    path('logout/', views.logout_view, name='logout'),
]
