from django.contrib import admin

from Comments.models import Comments


# Register your models here.
@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    ...