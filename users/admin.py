from django.contrib import admin

from .models import FollowAuthor


class FollowAuthorAdmin(admin.ModelAdmin):
    list_display = ('user', )
    search_fields = ('user', )


admin.site.register(FollowAuthor, FollowAuthorAdmin)
