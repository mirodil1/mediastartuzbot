from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel, Mahalla
from apps.tgusers.models import TelegramUser


class Submission(TimeStampedModel):

    class EducationLevel(models.TextChoices):
        SCHOOL = 'school', 'School (Secondary Education)'
        COLLEGE = 'college', 'College (Vocational Secondary)'
        BACHELOR = 'bachelor', 'Bachelor (Incomplete Higher Education)'
        MASTERS = 'masters', 'Masters (Higher Education)'

    tg_user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name=_("Telegram User")
    )
    full_name = models.CharField(max_length=255, verbose_name=_("Full Name"))
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    area = models.ForeignKey(
        Mahalla,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name=_("Area")
    )
    photo = models.ImageField(upload_to='photos/', verbose_name=_("Photo"))
    education = models.CharField(max_length=255, verbose_name=_("Education"))
    education_level = models.CharField(
        null=True,
        max_length=20,
        choices=EducationLevel.choices,
        verbose_name=_("Education Level")
    )
    profession = models.CharField(
        max_length=255,
        verbose_name=_("Profession"),
        null=True
    )
    certificate = models.FileField(
        null=True,
        upload_to='certificates/',
        verbose_name=_("Certificate")
    )
    creative_work = models.TextField(
        null=True,
        verbose_name=_("Creative Work")
    )
    phone_number = models.CharField(max_length=20, verbose_name=_("Phone Number"))
    is_accepted = models.BooleanField(default=False, verbose_name=_("Accepted"))

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "submissions"
        verbose_name = _("Submission")
        verbose_name_plural = _("Submissions")
        ordering = ["-created_at"]

    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
