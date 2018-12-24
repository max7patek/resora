from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from booker.models import Bookable
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUserManager(UserManager):
    pass

class CustomUser(AbstractUser):
    objects = CustomUserManager()


class User(models.Model):
    booking = models.OneToOneField(Bookable, related_name='booker', null=True, default=None, on_delete=models.SET_NULL)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def book(self, bookable):
        self.booking = bookable
        self.save()

    def release_booking(self):
        self.booking = None
        self.save()

    @classmethod
    def make(cls, user):
        self = cls()
        self.user = user
        self.save()
        return self



@receiver(post_save, sender=CustomUser)
def my_handler(sender, **kwargs):
    if (kwargs['created']):
        User.make(kwargs['instance'])
