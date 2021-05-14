from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

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
