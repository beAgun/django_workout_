from django.db import models
from django.contrib.auth.models import AbstractUser


def get_photo_path(instance, filename):
    return f'users/{instance.username}/{filename}'


class User(AbstractUser):
    photo = models.ImageField(upload_to=get_photo_path, blank=True,
                              null=True, verbose_name='Photo')
    date_birth = models.DateField(blank=True, null=True,
                                      verbose_name='Birth date', )

    def __str__(self):
        return f'{self.username}'


    # def _check_upload_to(self):
    #     self.photo.upload_to = f'users/{self.username}/'
    #     self.photo.
