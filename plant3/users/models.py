from django.db import models

class AccessLevel(models.Model):
    class Meta:
        permissions = (
            ("admin", "Admin access"),
            ("planter", "All views except setup"),
            ("viewer", "Only index, images, about"),
        )