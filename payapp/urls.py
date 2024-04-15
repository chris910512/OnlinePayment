from django.urls import path
from . import views

urlpatterns = [
    path('make_payment/', views.make_payment, name='make_payment'),
    path('request_payment/', views.request_payment, name='request_payment'),
    path('notifications/', views.notifications, name='notifications'),
    path('accept_payment_request/<int:request_id>/', views.accept_payment_request, name='accept_payment_request'),
    path('decline_payment_request/<int:request_id>/', views.decline_payment_request, name='decline_payment_request'),
]
