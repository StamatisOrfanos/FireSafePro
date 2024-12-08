from django.urls import path
from .views.user.address_views import create_address, address_functionality, get_all_addresses

urlpatterns = [
    path('api/address/', create_address, name='create_address'),
    path('api/address/<int:address_id>/', address_functionality, name='get_address'),
    path('api/addresses/', get_all_addresses, name='get_all_addresses'),
]

