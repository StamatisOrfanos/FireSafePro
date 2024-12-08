import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ...models import Company

@csrf_exempt
def company_detail(request, company_name):
    try:
        company = Company.objects.get(name=company_name)

    except Company.DoesNotExist:
        return JsonResponse({"error": f"Company: {company_name} not found"}, status=404)

    if request.method == "GET":
        return JsonResponse({
            "name": company.name,
            "email": company.email,
            "address": company.location if company.location else None,
            "image_url": company.image.url if company.image else None,
        }, status=200)

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            company.name = data.get("name", company.name)
            company.email = data.get("email", company.email)
            if 
            company.save()
            return JsonResponse({"message": f"Company: {company_name} updated successfully!"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    elif request.method == "DELETE":
        company.delete()
        return JsonResponse({"message": f"Company: {company_name} deleted successfully!"}, status=200)

    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
