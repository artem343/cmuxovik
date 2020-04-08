from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
# Images
from PIL import Image
import io
from django.conf import settings
from django.core.files.storage import default_storage as storage
# Star ratings
from star_ratings.models import Rating
from django.utils.translation import gettext_lazy as _


class SoftDeleteModel(models.Model):
    class Meta:
        abstract = True

    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self):
        self.deleted_at = timezone.now()
        self.is_active = False
        self.save()

    def undelete(self):
        self.deleted_at = None
        self.is_active = True
        self.save()


class SoftDeleteQuerySet(models.query.QuerySet):
    """
    Prevents objects from being hard-deleted. Instead, sets the
    ``date_deleted``, effectively soft-deleting the object.
    """

    def delete(self):
        for obj in self:
            obj.deleted_at = timezone.now()
            self.is_active = False
            obj.save()

    def undelete(self):
        for obj in self:
            obj.deleted_at = None
            self.is_active = True
            obj.save()


class SoftDeleteManager(models.Manager):
    """
    Only exposes objects that have NOT been soft-deleted.
    """

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(
            deleted_at__isnull=True)


class Author(SoftDeleteModel):  # one-to-one to user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_moderator = models.BooleanField(default=False)
    location = models.CharField(
        blank=True, max_length=50, verbose_name=_('location'))
    avatar = models.ImageField(
        default='default.jpg', upload_to='profile_pics', verbose_name=_('avatar'))
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if settings.DEBUG:  # save to media/ locally
            img = Image.open(self.avatar.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.avatar.path)
        else:  # resize and save to S3
            img_read = storage.open(self.avatar.name, 'rb')
            img = Image.open(img_read)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                in_mem_file = io.BytesIO()
                img.convert('RGB').save(in_mem_file, format='JPEG')
                img_write = storage.open(self.avatar.name, 'w+')
                img_write.write(in_mem_file.getvalue())
                img_write.close()
            img_read.close()


class Tag(SoftDeleteModel):
    name = models.CharField(max_length=50)
    domain = models.CharField(max_length=50)  # TODO: change to enum?
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')


class Cmux(SoftDeleteModel):
    text = models.TextField(verbose_name=_('cmux'))
    author = models.ForeignKey(
        Author, on_delete=models.DO_NOTHING, verbose_name=_('author'))
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_('tags'))
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    ratings = GenericRelation(Rating, related_query_name='cmuxes')

    class Meta:
        unique_together = ('text', 'is_active')

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('cmuxovik-home')


class Vote(SoftDeleteModel):
    cmux = models.ForeignKey(Cmux, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)
    vote = models.IntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author.user.username} -> {self.cmux}: {self.vote}"

    class Meta:
        unique_together = ('cmux', 'author')
