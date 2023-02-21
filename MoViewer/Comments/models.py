from django.db import models

# Create your models here.


class Comments(models.Model):
    user = models.ForeignKey("authentication.CustomUser", on_delete=models.CASCADE)
    movie = models.ForeignKey("Movie.Movie", on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
