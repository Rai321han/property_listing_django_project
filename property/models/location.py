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
        parts = [self.name, self.city, self.country]
        if self.state:
            parts.append(self.state)
        parts.append(self.country)
        return ", ".join(parts)
