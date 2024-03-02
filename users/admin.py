from django.contrib import admin
from .models import Parcel, UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone_number')

    def first_name(self, obj):
        return obj.user.first_name
    first_name.short_description = 'First Name'  # Sets column name in admin interface

    def last_name(self, obj):
        return obj.user.last_name
    last_name.short_description = 'Last Name'  # Sets column name in admin interface

class ParcelAdmin(admin.ModelAdmin):
    change_form_template = 'admin/parcel_change_form.html'
    list_display = ('user', 'track_code','description', 'in_archive')
    search_fields = ('user__username',)  
    list_filter = ('in_archive', 'status')
    
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Parcel, ParcelAdmin)