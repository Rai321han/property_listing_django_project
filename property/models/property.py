from django.db import models
from .location import Location


class Property(models.Model):
    """
    Represents a real estate property listing.
    """

    PROPERTY_TYPES = [
        ("house", "House"),
        ("apartment", "Apartment"),
        ("commercial", "Commercial"),
    ]

    STATUS_CHOICES = [("available", "Available"), ("rented", "Rented")]

    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(
        max_length=20, choices=PROPERTY_TYPES, default="house"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="available"
    )

    # Location relationship
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="properties"
    )

    # Property details
    price = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Property"
        verbose_name_plural = "Properties"
        indexes = [
            models.Index(fields=["location", "status"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.location.name}"

    @property
    def primary_image(self):
        """Return the first image or None"""
        return self.images.first()

    @property
    def formatted_price(self):
        """Return formatted price with currency"""
        return f"${self.price:,.2f}"
