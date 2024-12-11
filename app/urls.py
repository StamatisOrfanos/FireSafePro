from django.urls import path
from .views.address_views import create_address, address_functionality, get_all_addresses
from .views.sign_in_view import sign_in
from .views.user.user_views import create_user, user_functionality, get_company_users
from .views.admin.company_views import create_company, company_functionality, get_all_companies
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/address/', create_address, name='create_address'),
    path('api/address/<int:address_id>/', address_functionality, name='get_address'),
    path('api/addresses/', get_all_addresses, name='get_all_addresses'),
    path('api/sign-in/', sign_in, name='sign_in'),
    path('api/user/', create_user, name='create_user'),
    path('api/user/<int:user_id>/', user_functionality, name='user_functionality'),
    path('api/users/', get_all_addresses, name='get_all_addresses'),
    path('api/company/', create_company, name='create_company'),
    path('api/company/<int:company_id>/', company_functionality, name='company_functionality'),
    path('api/companies/', get_all_companies, name='get_all_companies'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)