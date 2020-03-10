from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from PIL import Image


class Author(models.Model):  # one-to-one to user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_moderator = models.BooleanField(default=False)
    location = models.CharField(blank=True, max_length=50)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)


class Tag(models.Model):
    name = models.CharField(max_length=50)
    domain = models.CharField(max_length=50)  # TODO: change to enum?
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} | {self.domain}"


class Cmux(models.Model):
    text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField(Tag)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('text', 'is_active')

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('cmuxovik-home')


class Vote(models.Model):
    cmux = models.ForeignKey(Cmux, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)
    vote = models.IntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author.user.username} -> {self.cmux}: {self.vote}"

    class Meta:
        unique_together = ('cmux', 'author')
