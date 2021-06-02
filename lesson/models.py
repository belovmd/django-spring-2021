from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

from django.conf import settings
from django.urls import reverse

# Create your models here.


class Material(models.Model):
    MATERIAL_TYPE = (
        ('theory', 'Theoretical Material'),
        ('practice', 'Practical Marterial'),
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique_for_date='publish')
    body = models.TextField()

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    publish = models.DateTimeField(default=timezone.now)

    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='user_materials')
    material_type = models.CharField(max_length=20,
                                     choices=MATERIAL_TYPE,
                                     default='theory')


    # def __str__(self):
    #     return self.title

    def get_absolute_url(self):
        return reverse('lesson:material_details',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


class Comment(models.Model):
    material = models.ForeignKey(Material,
                                 on_delete=models.CASCADE,
                                 related_name='comment')
    name = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    birthday = models.DateTimeField(null=True, blank=True)
    photo = models.ImageField(upload_to="user/%Y/%m/%d/", blank=True)
