from functools import wraps
import json
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from ...models import User


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

    try:
        data = json.loads(request.body)
        
        if User.objects.filter(username=data["username"]).exists():
            return JsonResponse({"error": "User already exists with this username"}, status=400)
        
        company = "ACME"  # company = request.user.company
        user = User.objects.create(
            username=data["username"],
            password=make_password(data["password"]),
            role="Company User",
            company=company,
        )
        return JsonResponse({"id": user.id, "message": "User created successfully!"}, status=201)
    except KeyError as e:
        return JsonResponse({"error": f"Missing field: {str(e)}"}, status=400)
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
                "company": "ACME",
                "created_at": user.created_at,
                "updated_at": user.updated_at
            }, status=200)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            user = User.objects.get(id=user_id)

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
            user = User.objects.get(id=user_id)
            user.delete()
            return JsonResponse({"message": f"User with username {user_id} deleted successfully!"}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"error": f"User with username {user_id} not found"}, status=404)
        
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)



@csrf_exempt
def change_password(request, username):
    if request.method != "PUT":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        current_password = data.get("current_password")
        new_password = data.get("new_password")

        if not current_password or not new_password:
            return JsonResponse({"error": "Both current_password and new_password are required"}, status=400)

        user = User.objects.get(username=username)

        if not check_password(current_password, user.password):
            return JsonResponse({"error": "Current password is incorrect"}, status=403)

        user.password = make_password(new_password)
        user.save()

        return JsonResponse({"message": "Password updated successfully!"}, status=200)
    except User.DoesNotExist:
        return JsonResponse({"error": f"User with username {username} not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)



@csrf_exempt
def get_company_users(request):
    if request.method == "GET":
        company = "ACME"
        users = User.objects.filter(company=company).order_by("username")
        users_list = [
            {
                "username": user.username,
                "role": user.role,
                "company": company,
                "created_at": user.created_at,
                "updated_at": user.updated_at
            }
            for user in users
        ]
        return JsonResponse({"users": users_list}, status=200)

