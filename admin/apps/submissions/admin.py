from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Submission

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
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

