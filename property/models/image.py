from django.db import models
from .property import Property


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
