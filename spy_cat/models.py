from django.db import models
from rest_framework.exceptions import ValidationError

from spy_cat.validator import validate_cat_breed


class SpyCat(models.Model):
    name = models.CharField(max_length=255)
    years_of_experience = models.PositiveIntegerField()
    breed = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=7, decimal_places=2)

    def clean(self):
        validate_cat_breed(self.breed)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Mission(models.Model):
    is_complete = models.BooleanField(default=False)
    cat = models.OneToOneField(
        SpyCat,
        on_delete=models.SET_NULL,
        related_name="mission",
        null=True,
        blank=True,
    )

    def clean(self):
        if not (1 <= self.targets.count() <= 3):
            raise ValidationError("A mission must have " "between 1 and 3 targets.")

    def __str__(self) -> str:
        return f"Mission for '{self.cat.name}', id: {self.id}"


class Target(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    is_complete = models.BooleanField(default=False)
    mission = models.ForeignKey(
        Mission, on_delete=models.CASCADE, related_name="targets"
    )

    def __str__(self) -> str:
        return self.name
