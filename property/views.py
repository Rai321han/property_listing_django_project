from django.shortcuts import render

# Create your views here.
"""
Views for Property app
"""
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q, Count
from .models import Property, Location


def home(request):
    """
    Home page with search input and recent properties
    """
    recent_properties = (
        Property.objects.filter(status="available")
        .select_related("location")
        .prefetch_related("images")[:6]
    )

    context = {
        "recent_properties": recent_properties,
    }
    return render(request, "property/home.html", context)


def autocomplete_location(request):
    """
    API endpoint for location autocomplete
    Returns JSON with up to 5 location suggestions
    """
    query = request.GET.get("q", "").strip()

    if len(query) < 1:
        return JsonResponse({"suggestions": []})

    # Search in location name and city
    locations = (
        Location.objects.filter(
            Q(name__icontains=query)
            | Q(city__icontains=query)
            | Q(country__icontains=query)
        )
        .annotate(property_count=Count("properties"))
        .filter(property_count__gt=0)
        .order_by("-property_count")[:5]
    )
    suggestions = [
        {
            "id": loc.id,
            "name": loc.name,
            "city": loc.city,
            "country": loc.country,
            "full_address": loc.full_address,
            "property_count": loc.property_count,
        }
        for loc in locations
    ]

    return JsonResponse({"suggestions": suggestions})


def property_list(request):
    """
    Display list of properties filtered by location
    """
    location_param = request.GET.get("location", "").strip()

    properties = (
        # Property.objects.filter(status="available")
        Property.objects.select_related("location").prefetch_related("images")
    )

    selected_location = None

    if location_param:
        # Case 1: location is an ID (from autocomplete)
        if location_param.isdigit():
            print("herer")
            selected_location = get_object_or_404(Location, id=location_param)
            properties = properties.filter(location=selected_location)

        # Case 2: location is free text
        else:
            properties = properties.filter(
                Q(location__name__icontains=location_param)
                | Q(location__city__icontains=location_param)
                | Q(location__country__icontains=location_param)
            )

    # # Additional filters
    # property_type = request.GET.get("type")
    # if property_type:
    #     properties = properties.filter(property_type=property_type)

    # min_price = request.GET.get("min_price")
    # if min_price:
    #     properties = properties.filter(price__gte=float(min_price))

    # max_price = request.GET.get("max_price")
    # if max_price:
    #     properties = properties.filter(price__lte=float(max_price))

    # bedrooms = request.GET.get("bedrooms")
    # if bedrooms:
    #     properties = properties.filter(bedrooms__gte=int(bedrooms))

    properties = properties.order_by("-created_at")

    context = {
        "properties": properties,
        "selected_location": selected_location,
        "property_types": Property.PROPERTY_TYPES,
        "search_query": location_param,
    }

    return render(request, "property/property_list.html", context)


def property_detail(request, pk):
    """
    Display detailed information about a single property
    """
    property_obj = get_object_or_404(
        Property.objects.select_related("location").prefetch_related("images"), pk=pk
    )

    # Get similar properties in the same location
    similar_properties = (
        Property.objects.filter(location=property_obj.location, status="available")
        .exclude(pk=property_obj.pk)
        .select_related("location")
        .prefetch_related("images")[:3]
    )

    context = {
        "property": property_obj,
        "similar_properties": similar_properties,
    }
    return render(request, "property/property_detail.html", context)
