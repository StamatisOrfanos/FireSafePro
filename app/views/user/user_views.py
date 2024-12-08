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
    
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    if User.objects.filter(username=data["username"]).exists():
        return JsonResponse({"error": "User already exists with this username"}, status=400)

    try:
        data = json.loads(request.body)
        company = request.user.company

        user = User.objects.create(
            username=data["username"],
            password=make_password(data["password"]),
            role=User.TYPE_CHOICES["Company User"],
            company=company,
        )
        return JsonResponse({"id": user.id, "message": "User created successfully!"}, status=201)

    except KeyError as e:
        return JsonResponse({"error": f"Missing field: {str(e)}"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)



@csrf_exempt
def user_functionality(request, username):
    
    if request.method == "GET":
        try:
            user = User.objects.get(username=username)
            return JsonResponse({
                "username": user.username,
                "role": user.role,
                "company": user.company,
                "created_at": user.created_at,
                "updated_at": user.updated_at
            }, status=200)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            user = User.objects.get(id=username)

            if request.user.role == "Company Admin" and user.company != request.user.company:
                return JsonResponse({"error": "Unauthorized to update users outside your company"}, status=403)

            user.username = data.get("username", user.username)
            if "password" in data: 
                user.password = make_password(data["password"])
            if "role" in data and request.user.role == "System Admin":
                user.role = data["role"]

            user.save()
            return JsonResponse({"id": user.id, "message": "User updated successfully!"}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
    elif request.method == "DELETE":
        try:
            user = User.objects.get(id=username)
            user.delete()
            return JsonResponse({"message": f"User with username {username} deleted successfully!"}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"error": f"User with username {username} not found"}, status=404)
        
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def get_company_users(request):
    if request.method == "GET":
        company = request.user.company
        users = User.objects.filter(company=company).order_by("username")
        users_list = [
            {
                "username": user.username,
                "role": user.role,
                "company": user.company,
                "created_at": user.created_at,
                "updated_at": user.updated_at
            }
            for user in users
        ]
        return JsonResponse({"users": users_list}, status=200)

