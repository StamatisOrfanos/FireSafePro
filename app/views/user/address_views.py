import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ...models import Address

@csrf_exempt
def create_address(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            address = Address.objects.create(
                street=data.get("street"),
                city=data.get("city"),
                state=data.get("state"),
                country=data.get("country"),
                postal_code=data.get("postal_code"),
            )
            return JsonResponse({"id": address.id, "message": "Address created successfully!"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def address_functionality(request, address_id):
    # Get
    if request.method == "GET":
        try:
            address = Address.objects.get(id=address_id)
            return JsonResponse({
                "id": address.id,
                "street": address.street,
                "city": address.city,
                "state": address.state,
                "country": address.country,
                "postal_code": address.postal_code,
            }, status=200)
        except Address.DoesNotExist:
            return JsonResponse({"error": "Address not found"}, status=404)
    
    # Update
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            address = Address.objects.get(id=address_id)
            address.street = data.get("street", address.street)
            address.city = data.get("city", address.city)
            address.state = data.get("state", address.state)
            address.country = data.get("country", address.country)
            address.postal_code = data.get("postal_code", address.postal_code)
            address.save()
            return JsonResponse({"message": "Address updated successfully!"}, status=200)
        except Address.DoesNotExist:
            return JsonResponse({"error": "Address not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    # Delete
    elif request.method == "DELETE":
        try:
            address = Address.objects.get(id=address_id)
            address.delete()
            return JsonResponse({"message": f"Address with ID {address_id} deleted successfully!"}, status=200)
        except Address.DoesNotExist:
            return JsonResponse({"error": f"Address with ID {address_id} not found"}, status=404)
    
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)




@csrf_exempt
def get_all_addresses(request):
    if request.method == "GET":
        addresses = Address.objects.all()
        address_list = [
            {
                "id": address.id,
                "street": address.street,
                "city": address.city,
                "state": address.state,
                "country": address.country,
                "postal_code": address.postal_code,
            }
            for address in addresses
        ]
        return JsonResponse({"addresses": address_list}, status=200)
