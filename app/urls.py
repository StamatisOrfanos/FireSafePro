from django.urls import path
from .views.address_views import create_address, address_functionality, get_all_addresses
from .views.sign_in_view import sign_in
from .views.user.user_views import create_user, user_functionality, get_company_users

urlpatterns = [
    path('api/address/', create_address, name='create_address'),
    path('api/address/<int:address_id>/', address_functionality, name='get_address'),
    path('api/addresses/', get_all_addresses, name='get_all_addresses'),
    path('api/sign-in/', sign_in, name='sign_in'),
    path('api/user/', create_user, name='create_user'),
    path('api/user/<int:user_id>/', user_functionality, name='user_functionality'),
    path('api/users/', get_all_addresses, name='get_all_addresses'),
    
]

