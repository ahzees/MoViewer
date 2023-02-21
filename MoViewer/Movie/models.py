from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=99)
    slug = models.SlugField(max_length=99, null=True)

    def __str__(self):
        return f"{self.name}"


# def name_valid(str):
#     if 'Movie' not in str:
#         raise ValidationError
#     else:
#         return str
class Movie(models.Model):
    name = models.CharField(max_length=155, null=True)
    slug = models.SlugField(
        unique=True, max_length=255, db_index=True, verbose_name="Url"
    )
    description = models.CharField(max_length=1000, null=True)
    video = models.FileField(null=True)
    images = models.ImageField(null=True)
    like = models.ManyToManyField(
        "authentication.CustomUser", related_name="like", null=True, blank=True
    )
    dislike = models.ManyToManyField(
        "authentication.CustomUser", related_name="dislike", null=True, blank=True
    )
    year = models.DateField(
        null=True,
    )
    category = models.ManyToManyField("Movie.Category", null=True)

    def get_absolute_url(self):
        return reverse("movie", kwargs={"movie_slug": self.slug})

    def __str__(self):
        return f"{self.name} "
