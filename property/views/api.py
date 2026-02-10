from rest_framework.generics import GenericAPIView
from django.db.models import Q, Count
from ..models import Location
from rest_framework.response import Response
from ..serializers import LocationAutocompleteSerializer


class LocationAutocompleteAPIView(GenericAPIView):
    serializer_class = LocationAutocompleteSerializer

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()

        if not query:
            return Location.objects.none()

        return (
            Location.objects.filter(
                Q(name__icontains=query)
                | Q(city__icontains=query)
                | Q(country__icontains=query)
            )
            .annotate(property_count=Count("properties"))
            .filter(property_count__gt=0)
            .order_by("-property_count")[:5]
        )

    def get(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({"suggestions": serializer.data})
