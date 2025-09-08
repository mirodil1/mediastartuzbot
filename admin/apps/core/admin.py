from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import District, Region, Mahalla


class DistrictInline(admin.StackedInline):
    model = District
    extra = 1


class MahallaModelAdmin(ImportExportModelAdmin):
    list_display = ['name', 'is_active', 'id']
    list_filter = ["name", "is_active",]
    list_editable = ['is_active']
    search_fields = ['name', "id"]


class DistrictModelAdmin(ImportExportModelAdmin):
    list_display = ['name', 'region', "is_active", 'id']
    list_filter = ["name", "is_active", 'region']
    list_editable = ['is_active']
    search_fields = ['name', "id"]


class RegionModelAdmin(ImportExportModelAdmin):
    list_display = ['name', "is_active", 'id']
    list_filter = ["name", "is_active"]
    list_editable = ['is_active']
    search_fields = ['name', "id"]

    inlines = [DistrictInline]


admin.site.register(Region, RegionModelAdmin)
admin.site.register(District, DistrictModelAdmin)
admin.site.register(Mahalla, MahallaModelAdmin)
