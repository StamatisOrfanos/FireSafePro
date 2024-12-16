from django.urls import path
from .views.address_views import create_address, address_functionality, get_all_addresses
from .views.sign_in_view import sign_in
from .views.admin.admin_user_views import create_user, user_functionality, get_users
from .views.admin.company_views import create_company, company_functionality, update_company_image ,get_all_companies
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/admin/company_admin/', create_user, name='create_user'),
    path('api/admin/company_admin/<int:user_id>/', user_functionality, name='user_functionality'),
    path('api/admin/all_users/<str:request_type>/', get_users, name='get_users'),
    
    
    path('api/address/', create_address, name='create_address'),
    path('api/address/<int:address_id>/', address_functionality, name='get_address'),
    path('api/addresses/', get_all_addresses, name='get_all_addresses'),
    

    
    
    path('api/sign-in/', sign_in, name='sign_in'),

    path('api/company/', create_company, name='create_company'),
    path('api/company/<int:company_id>/', company_functionality, name='company_functionality'),
    path('api/company/<int:company_id>/image', update_company_image, name='update_company_image'),
    path('api/companies/', get_all_companies, name='get_all_companies'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)