from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ExportMixin

from import_export import resources
from datetime import date

from .models import Submission


class SubmissionResource(resources.ModelResource):
    # Custom field to export full hierarchy
    area = resources.Field()

    def dehydrate_area(self, submission):
        # Access related models and build the full hierarchy
        mahalla = submission.area
        district = mahalla.district
        region = district.region

        # Combine Region, District, and Mahalla names in a readable format
        return f"{region.name} > {district.name} > {mahalla.name}"

    def dehydrate_age(self, submission):
        # Calculate age from date_of_birth
        today = date.today()
        birth_date = submission.date_of_birth
        age = today.year - birth_date.year

        # Adjust age if birthday hasn't occurred yet this year
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1

        return age
    
    class Meta:
        model = Submission
        fields = (
            "full_name",
            "age",
            "area",
            "phone_number",
            "education",
            "photo", 
            "certificate",
            "creative_work",
            "created_at",
        )



@admin.register(Submission)
class SubmissionAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = SubmissionResource
    list_display = (
        "full_name",
        "full_area",
        "phone_number",
        "age",
        "education"
    )
    list_filter = ("is_accepted", "education_level", "area")
    search_fields = ("full_name", "tg_user__username", "phone_number")
    readonly_fields = ("tg_user", "full_name", "date_of_birth", "area", "photo",
                       "education", "certificate", "creative_work",
                       "phone_number", "is_accepted")
    exclude = ("profession", "education_level")
    actions = ["accept_submissions"]

    @admin.action(description=_("Accept selected submissions"))
    def accept_submissions(self, request, queryset):
        updated_count = queryset.update(is_accepted=True)
        self.message_user(request, _("%d submissions were accepted." % updated_count))
    accept_submissions.short_description = _("Accept selected submissions")

    @admin.display(description=_("Area"))
    def full_area(self, obj):
        return f"{obj.area.district.region.name} - {obj.area.district.name} - {obj.area.name}"

