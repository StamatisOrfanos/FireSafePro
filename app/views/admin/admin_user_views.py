from functools import wraps
import json
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from ...models import User, Company


def check_user_permission(required_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if not hasattr(request, 'user') or request.user.role not in required_roles:
                return JsonResponse({"error": "Unauthorized action"}, status=403)
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


@csrf_exempt
def create_user(request):
    if request.method == "POST":
        try:
            username = request.POST.get("username")
            
            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "User already exists with this username"}, status=400)
            
            password = make_password(request.POST.get("password"))
            role = "Company Admin"
            company_name = request.POST.get("company_name")
            company_query = Company.objects.filter(name__exact=company_name)
            if not company_query.exists():
                return JsonResponse({"error": f"Company with name: {company_name} does not exist"}, status=400)
            
            company = company_query.first()

            image = request.FILES.get("image")
            signature = request.FILES.get("signature")
            
            user = User.objects.create(username=username, password=password, role=role, company=company, image=image, signature=signature)
            return JsonResponse({"id": user.id, "message": "User created successfully!"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)



@csrf_exempt
def user_functionality(request, user_id):
    
    if request.method == "GET":
        try:
            user = User.objects.get(id=user_id)
            return JsonResponse({
                "username": user.username,
                "role": user.role,
                "company": user.company.name,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
                "image": user.image.url if user.image else None,
                "signature": user.signature.url if user.signature else None
            }, status=200)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            user = User.objects.get(id=user_id)
            user.username = data.get("username", user.username)
            user.role = data["role"] if "role" in data else user.role
            user.save()
            return JsonResponse({"id": user.id, "message": "User updated successfully!"}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
    elif request.method == "DELETE":
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return JsonResponse({"message": f"User with ID {user_id} deleted successfully!"}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"error": f"User with ID {user_id} not found"}, status=404)
        
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def get_users(request, request_type):
    if request.method == "GET":
        
        if request_type == "admins":
            users = User.objects.filter(role="Company Admin").order_by("company")
        elif request_type == "users":
            users = User.objects.filter(role="Company User").order_by("company")
        elif request_type == "all":
            users = User.objects.all().order_by("company", "username")
        else:
            return JsonResponse({"error": f"Request type can be one of the [admins, users, all]"}, status=404)
        
        users_list = [
            {
                "username": user.username,
                "role": user.role,
                "company": user.company.name,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
                "image": user.image.url if user.image else None,
                "signature": user.signature.url if user.signature else None
            }
            for user in users
        ]
        return JsonResponse({"users": users_list}, status=200)