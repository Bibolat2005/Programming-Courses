from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'bio')  
    list_filter = ('role',)  
    search_fields = ('user__username', 'role') 

admin.site.register(Profile, ProfileAdmin)
