from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User

admin.site.register(User)


class CustomUserAdmin(DefaultUserAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(pk=request.user.pk)
        return qs


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
