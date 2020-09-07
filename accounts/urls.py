from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	path('register/', views.register_page, name='register-url'),
	path('login/', views.login_page, name='login-url'),
	path('logout/', views.logoutUser, name='logout-url'),

    path('', views.dashboard, name='dashboard-url'),
    path('user/', views.user_page, name='user-url'),
    path('products/', views.products, name='products-url'),
    path('customer/<str:pk>/', views.customer, name='customer-url'),
    path('account/', views.accountSettings, name="account-url"),
    
    path('create_order/<str:pk>/', views.create_order, name='create_order-url'),
    path('update_order/<str:pk>/', views.update_order, name='update_order-url'),
    path('delete_order/<str:pk>/', views.delete_order, name="delete_order-url"),
    
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = 'accounts/password_reset.html'), name = "password_reset"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = 'accounts/password_reset_sent.html'), name = "password_reset_done"),
    path('reset<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'accounts/password_reset_form.html'), name = "password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'accounts/password_reset_done.html'), name = "password_reset_complete")
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)