from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """
    Abstract Timestamp model
    """

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated"))

    class Meta:
        abstract = True


class Region(TimeStampedModel):
    name = models.CharField(max_length=120, verbose_name=_("Name"))
    is_active = models.BooleanField(default=True, verbose_name=_("Status"))

    class Meta:
        db_table = "regions"
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")

    def __str__(self):
        return f"{self.name}"


class District(TimeStampedModel):
    name = models.CharField(max_length=120, verbose_name=_("Name"))
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name='region',
        verbose_name=_("Region")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Status"))

    class Meta:
        db_table = "districts"
        verbose_name = _("District")
        verbose_name_plural = _("Districts")

    def __str__(self):
        return f"{self.name}"


class Mahalla(TimeStampedModel):
    name = models.CharField(max_length=120, verbose_name=_("Name"))
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        related_name='district',
        verbose_name=_("District")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("D]Status"))

    class Meta:
        db_table = "mahalla"
        verbose_name = _("Mahalla")
        verbose_name_plural = _("Mahalla")

    def __str__(self):
        return f"{self.name}"
