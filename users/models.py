from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10, unique=True)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.userprofile.save()
    
class Parcel(models.Model):
    TRACKING_STATUSES = (
        ('CREATED', 'Создано'),
        ('SHIPPED', 'Отправлено'),
        ('IN_TRANSIT', 'В пути'),
        ('DELIVERED', 'Доставлено'),
        ('RECEIVED', 'Получено клиентом'),
        ('DONE', 'Принято клиентом')
    )
    

    ARCHIVE_CHOICES = (
        (False, 'Не в архиве'),
        (True, 'В архиве'),
    )

    track_code = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=TRACKING_STATUSES, default='PENDING')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parcels')
    in_archive = models.BooleanField(choices=ARCHIVE_CHOICES, default=False)

    def __str__(self):
        return self.track_code