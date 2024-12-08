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

    try:
        data = json.loads(request.body)
        company = Company.objects.get(name=data["company"])
        user = User.objects.create(
            username=data["username"],
            password=make_password(data["password"]),
            role="Company Admin",
            company=company,
        )
        return JsonResponse({"id": user.id, "message": "User created successfully!"}, status=201)

    except KeyError as e:
        return JsonResponse({"error": f"Missing field: {str(e)}"}, status=400)
    except Company.DoesNotExist:
        return JsonResponse({"error": "Company not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)



@csrf_exempt
def user_functionality(request, user_id):
    
    if request.method == "GET":
        try:
            user = User.objects.get(id=user_id)
            return JsonResponse({
                "username": user.username,
                "role": "Company Admin",
                "company": user.company,
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
            if "role" in data: 
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
            return JsonResponse({"message": f"User with ID {user_id} deleted successfully!"}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"error": f"User with ID {user_id} not found"}, status=404)
        
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def get_all_users(request):
    if request.method == "GET":
        users = User.objects.all().order_by("company", "username")
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