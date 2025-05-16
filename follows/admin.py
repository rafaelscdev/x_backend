from django.contrib import admin
from .models import Follow

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    list_filter = ('created_at', 'follower', 'following')
    search_fields = ('follower__username', 'following__username')
    readonly_fields = ('created_at',)
