from django.contrib import admin

from notifications.models import Template, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    search_fields = ('id', 'email')


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'updated_at')
    search_fields = (
        'id',
        'name',
    )
