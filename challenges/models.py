from django.db import models
from django.utils.translation import gettext_lazy as _
import string
import random
from django.dispatch import receiver
from django.db.models.signals import post_save

from users.models import CyphersUser
# Create your models here.

class Challeng(models.Model):

    class DifficultChoices(models.TextChoices):
        EASY = 'E', _('Easy')
        MEDIUM = 'M', _('Medium')
        HARD = 'H', _('Hard')

    name = models.CharField(max_length=30)
    text = models.CharField(max_length=1000)    
    difficult_level = models.CharField(max_length=1, choices = DifficultChoices.choices, default = DifficultChoices.EASY)


class CyphersUserChalleng(models.Model):

    user = models.ForeignKey(CyphersUser, on_delete=models.CASCADE)
    challeng = models.ForeignKey(Challeng, on_delete=models.CASCADE)
    answer = models.CharField(max_length=10)
    unblock_code = models.CharField(max_length=10)
    is_done = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        code = string.ascii_letters + string.digits
        unblock_code = ''.join(random.sample(code,len(code)))
        answer = ''.join(random.sample(code,len(code)))
        if not self.unblock_code:
            self.unblock_code = unblock_code[:10]
        if not self.answer:
            self.answer = answer[:10]
        super().save(*args, **kwargs)    


@receiver(post_save, sender=CyphersUser)
def create_challenges(sender, instance, created, **kwargs):
    if created:
        for ch in Challeng.objects.all():
            new_challeng = CyphersUserChalleng(user=instance, challeng=ch)
            new_challeng.save()
        user_challenges = CyphersUserChalleng.objects.filter(user=instance)
        for i in range(1,len(user_challenges)):            
            user_challenges[i].unblock_code = user_challenges[i-1].answer
            user_challenges[i].save()

    