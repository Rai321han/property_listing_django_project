"""
Admin configuration for Property app models
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Location, Property, Image


class ImageInline(admin.TabularInline):
    """
    Inline admin for managing property images
    """

    model = Image
    extra = 1
    fields = ["image", "caption", "is_primary", "order", "image_preview"]
    readonly_fields = ["image_preview"]

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 150px;" />',
                obj.image.url,
            )
        return "No image"

    image_preview.short_description = "Preview"


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """
    Admin interface for Location model
    """

    list_display = ["id", "name", "city", "state", "country", "property_count"]
    list_filter = ["city", "state", "country"]
    search_fields = ["name", "city", "state"]
    ordering = ["name"]

    def property_count(self, obj):
        return obj.properties.count()

    property_count.short_description = "Properties"


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    """
    Admin interface for Property model with image upload
    """

    list_display = [
        "id",
        "title",
        "location",
        "property_type",
        "status",
        "formatted_price",
        "bedrooms",
        "bathrooms",
        "image_count",
        "created_at",
        "updated_at",
    ]
    list_filter = ["property_type", "status", "location__city"]
    search_fields = ["title", "description", "location__name"]
    list_editable = ["status"]
    readonly_fields = ["created_at", "updated_at", "primary_image_preview"]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("title", "description", "property_type", "status", "location")},
        ),
        (
            "Property Details",
            {"fields": ("price", "bedrooms", "bathrooms")},
        ),
        ("Primary Image", {"fields": ("primary_image_preview",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    inlines = [ImageInline]

    def image_count(self, obj):
        return obj.images.count()

    image_count.short_description = "Images"

    def primary_image_preview(self, obj):
        primary = obj.primary_image
        if primary:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 300px;" />',
                primary.image.url,
            )
        return "No images uploaded"

    primary_image_preview.short_description = "Primary Image"


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """
    Admin interface for Image model
    """

    list_display = [
        "property",
        "caption",
        "is_primary",
        "order",
        "image_preview",
        "uploaded_at",
    ]
    list_filter = ["is_primary", "uploaded_at"]
    search_fields = ["property__title", "caption"]
    list_editable = ["is_primary", "order"]

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 80px; max-width: 120px;" />',
                obj.image.url,
            )
        return "No image"

    image_preview.short_description = "Preview"
