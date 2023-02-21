from Comments.models import Comments
from django.contrib import admin


# Register your models here.
@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    ...
