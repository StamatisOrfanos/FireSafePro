from functools import wraps
import json
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from ..models import User, Company


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
@check_user_permission(["System Admin", "Company Admin"])
def create_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        role = "Company Admin" if request.user.role == "System Admin" else "Company User"
        company = (
            Company.objects.get(name=data["company"]) if request.user.role == "System Admin"
            else request.user.company
        )

        # Create the user
        user = User.objects.create(
            username=data["username"],
            password=make_password(data["password"]),
            role=role,
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
@check_user_permission(["System Admin", "Company Admin"])
def update_user(request, user_id):
    if request.method != "PUT":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        user = User.objects.get(id=user_id)

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



