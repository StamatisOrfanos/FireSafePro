import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ...models import Company, Address


@csrf_exempt
def create_company(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            email = request.POST.get("email")
            address = define_address(request=request)
            image = request.FILES.get("image")            
            company = Company.objects.create(name=name, email=email, location=address, image=image)

            return JsonResponse({
                "id": company.id, 
                "name": company.name, 
                "email": company.email,
                "location": {
                    "id": address.id,
                    "street": address.street,
                    "city": address.city,
                    "state": address.state,
                    "country": address.country,
                    "postal_code": address.postal_code,
                },
                "image": company.image.url if company.image else None,
                "message": "Company and address processed successfully!"
            }, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)




@csrf_exempt
def company_functionality(request, company_id):
    try:
        company = Company.objects.get(id=company_id)

    except Company.DoesNotExist:
        return JsonResponse({"error": f"Company: {company.name} not found"}, status=404)

    if request.method == "GET":
        return JsonResponse({
            "name": company.name,
            "email": company.email,
            "location": {
                    "id": company.location.id,
                    "street": company.location.street,
                    "city": company.location.city,
                    "state": company.location.state,
                    "country": company.location.country,
                    "postal_code": company.location.postal_code},
            "image_url": company.image.url if company.image else None,
        }, status=200)

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            company.name = data["name"] if "name" in data else company.name
            company.email = data["email"] if "email" in data else company.email
            company.location = define_address(data=data["location"]) if "location" in data else company.location
            company.save()
            return JsonResponse({
                "id": company.id,
                "name": company.name,
                "email": company.email,
                "location": {
                    "id": company.location.id,
                    "street": company.location.street,
                    "city": company.location.city,
                    "state": company.location.state,
                    "country": company.location.country,
                    "postal_code": company.location.postal_code,
                } if company.location else None,
                "image_url": company.image.url if company.image else None,
                "message": "Company updated successfully!",
            }, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    elif request.method == "DELETE":
        company.delete()
        return JsonResponse({"message": f"Company: {company.name} deleted successfully!"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)




@csrf_exempt
def update_company_image(request, company_id):
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        return JsonResponse({"error": f"Company not found"}, status=404)

    if request.method == "PUT":
        try:
            image = request.FILES.get("image")
            if image:
                company.image = image
                company.save()

            return JsonResponse({
                "id": company.id,
                "name": company.name,
                "email": company.email,
                "location": {
                    "id": company.location.id,
                    "street": company.location.street,
                    "city": company.location.city,
                    "state": company.location.state,
                    "country": company.location.country,
                    "postal_code": company.location.postal_code,
                },
                "image_url": company.image.url if company.image else None,
                "message": "Company image updated successfully!",
            }, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)



@csrf_exempt
def get_all_companies(request):
    if request.method == "GET":
        companies = Company.objects.all()
        companies_list = [
            {
                "id": company.id, 
                "name": company.name, 
                "email": company.email,
                "location": {
                    "id": company.location.id,
                    "street": company.location.street,
                    "city": company.location.city,
                    "state": company.location.state,
                    "country": company.location.country,
                    "postal_code": company.location.postal_code,
                },
                "image": company.image.url if company.image else None,
            }
            for company in companies
        ]
        return JsonResponse({"companies": companies_list}, status=200)


def define_address(data):
    
    street=data["street"]
    city=data["city"]
    state=data["state"]
    country=data["country"]
    postal_code=data["postal_code"]

    
    address_data = {
        "street" : street,
        "city"   : city,
        "state"  : state,
        "country":country,
        "postal_code":postal_code
    }
    
    required_fields = ["street", "city", "state", "country", "postal_code"]
    if not all(address_data.get(field) for field in required_fields):
        return JsonResponse({"error": "Missing address fields"}, status=400)

    address = Address.objects.filter(**address_data).first()
        
    if not address:
        address = Address.objects.create(**address_data)
        
    return address
    
    