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
            
            # Create the company
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
            updated_company = update_company(request=request, company=company)
            return JsonResponse({
                "id": updated_company.id,
                "name": updated_company.name,
                "email": updated_company.email,
                "location": {
                    "id": updated_company.location.id,
                    "street": updated_company.location.street,
                    "city": updated_company.location.city,
                    "state": updated_company.location.state,
                    "country": updated_company.location.country,
                    "postal_code": updated_company.location.postal_code,
                } if updated_company.location else None,
                "image_url": updated_company.image.url if updated_company.image else None,
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



def update_company(request, company):
    # Update basic fields
    # --------------------------------------------------------------------------------------------------------------------------------------------    
    # We need to have a separate update for image and the rest data for each company
    # --------------------------------------------------------------------------------------------------------------------------------------------
    
    print("Request POST data:", request.POST)  # Add this
    print("Request FILES data:", request.FILES) 
    
    name = request.POST.get("name")
    if name:
        company.name = name

    email = request.POST.get("email")
    if email:
        company.email = email
        
    print("The new name is: {} and the new email is: {}".format(company.name, company.email))

    # Update or reuse the address
    if any([request.POST.get("street"), request.POST.get("city"), request.POST.get("state"), request.POST.get("country"), request.POST.get("postal_code"),]):
        # Get the new address details or use the current values
        street = request.POST.get("street") or company.location.street
        city = request.POST.get("city") or company.location.city
        state = request.POST.get("state") or company.location.state
        country = request.POST.get("country") or company.location.country
        postal_code = request.POST.get("postal_code") or company.location.postal_code
        print("Here with new address data")

        # Check if the updated address already exists
        location = Address.objects.filter(street=street, city=city, state=state, country=country, postal_code=postal_code).first()

        if not location:
            location = Address.objects.create(street=street, city=city, state=state, country=country, postal_code=postal_code)
            print("New location created")

        # Assign the new or existing location to the company
        company.location = location

    # Update the image
    if request.FILES.get("image"):
        company.image = request.FILES.get("image")

    # Save the updated company instance
    company.save()
    

    return company


    


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
    if not all(address_data.get(field) for field in required_fields) and call=="create":
        return JsonResponse({"error": "Missing address fields"}, status=400)

    address = Address.objects.filter(street=street, city=city, state=state, country=country, postal_code=postal_code).first()
        
    if not address:
        address = Address.objects.create(street=street, city=city, state=state, country=country, postal_code=postal_code)
        
    return address
    
    