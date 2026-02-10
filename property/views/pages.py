from django.shortcuts import render

# Create your views here.
"""
Views for Property app
"""
from django.shortcuts import render, get_object_or_404
from ..models import Property, Location
from django.core.paginator import Paginator
from ..models import Location
from django.db.models import Q


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


def property_list(request):
    """
    Display list of properties filtered by location
    """
    location_id = request.GET.get("location", "").strip()
    location_text = request.GET.get("location_text", "").strip()

    properties = Property.objects.select_related("location").prefetch_related("images")
    selected_location = None

    if location_id:
        if location_id.isdigit():
            selected_location = get_object_or_404(Location, id=location_id)
            properties = properties.filter(location=selected_location)
        else:
            # Free text search if not digit
            properties = properties.filter(
                Q(location__name__icontains=location_id)
                | Q(location__city__icontains=location_id)
                | Q(location__country__icontains=location_id)
            )

    properties = properties.order_by("-created_at")
    paginator = Paginator(properties, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "properties": page_obj,
        "page_obj": page_obj,
        "selected_location": selected_location,
        "property_types": Property.PROPERTY_TYPES,
        "search_query": location_text or location_id,
        "count": properties.count,
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
