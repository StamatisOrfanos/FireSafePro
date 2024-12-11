import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ...models import Company, Address


@csrf_exempt
def create_company(request):
    if request.method == "POST":
        try:
            # Parse form-data for image and JSON fields
            name = request.POST.get("name")
            email = request.POST.get("email")
            address = define_address(request=request)
            image = request.FILES.get("image")
            
            print("Image:", request.FILES.get("image"))

            
            # Create the company
            company = Company.objects.create(
                name=name,
                email=email,
                location=address,
                image=image)

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
            "address": company.location if company.location else None,
            "image_url": company.image.url if company.image else None,
        }, status=200)

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            company.name = data.get("name", company.name)
            company.email = data.get("email", company.email)
            company.save()
            return JsonResponse({"message": f"Company: {company.name} updated successfully!"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    elif request.method == "DELETE":
        company.delete()
        return JsonResponse({"message": f"Company: {company.name} deleted successfully!"}, status=200)

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



def define_address(request):
    street=request.POST.get("street")
    city=request.POST.get("city")
    state=request.POST.get("state")
    country=request.POST.get("country")
    postal_code=request.POST.get("postal_code")
    
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

    address = Address.objects.filter(street=street, city=city, state=state, country=country, postal_code=postal_code).first()
        
    if not address:
        address = Address.objects.create(street=street, city=city, state=state, country=country, postal_code=postal_code)
        
    return address
    
    