from django.db import models


class Location(models.Model):
    """
    Represents a geographic location where properties can be situated.
    """

    name = models.CharField(max_length=255, unique=True, db_index=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default="USA")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self):
        return f"{self.name}, {self.city}"

    @property
    def full_address(self):
        """Return full formatted address"""
        parts = [self.name, self.city]
        if self.state:
            parts.append(self.state)
        if self.zipcode:
            parts.append(self.zipcode)
        parts.append(self.country)
        return ", ".join(parts)


class Property(models.Model):
    """
    Represents a real estate property listing.
    """

    PROPERTY_TYPES = [
        ("house", "House"),
        ("apartment", "Apartment"),
        ("condo", "Condo"),
        ("townhouse", "Townhouse"),
        ("land", "Land"),
        ("commercial", "Commercial"),
    ]

    STATUS_CHOICES = [
        ("available", "Available"),
        ("sold", "Sold"),
        ("pending", "Pending"),
        ("rented", "Rented"),
    ]

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
    area_sqft = models.PositiveIntegerField(help_text="Area in square feet")
    year_built = models.PositiveIntegerField(null=True, blank=True)

    # Metadata
    featured = models.BooleanField(default=False)
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


class Image(models.Model):
    """
    Represents an image associated with a property.
    """

    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="properties/")
    caption = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-uploaded_at"]
        verbose_name = "Property Image"
        verbose_name_plural = "Property Images"

    def __str__(self):
        return f"Image for {self.property.title}"

    def save(self, *args, **kwargs):
        """
        Auto-set first image as primary if no primary exists
        """
        if self.is_primary:
            # Ensure only one primary image per property
            Image.objects.filter(property=self.property, is_primary=True).update(
                is_primary=False
            )
        super().save(*args, **kwargs)

    @property
    def thumbnail_url(self):
        """Return image URL (can be extended with thumbnail generation)"""
        if self.image:
            return self.image.url
        return None
