from django.contrib import admin
from .models import Follow

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'followed', 'created_at')
    list_filter = ('created_at', 'follower', 'followed')
    search_fields = ('follower__username', 'followed__username')
    readonly_fields = ('created_at',)
