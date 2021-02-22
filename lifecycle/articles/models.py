from django.db import models
from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.dispatch import receiver
from django_lifecycle import LifecycleModel, hook, AFTER_CREATE, AFTER_UPDATE, AFTER_DELETE, BEFORE_UPDATE
from django.contrib.auth.models import AbstractUser
from model_utils.models import StatusModel
from model_utils import Choices

# Create your models here.

class User(AbstractUser):
    def __str__(self):
        return self.email


class CommonInfo(StatusModel):
    STATUS = Choices("draft", "published", "error")
    contents = models.TextField()
    updated_at = models.DateTimeField(null=True)
    editor =  models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class ArticleExample1(LifecycleModel, CommonInfo):
    @hook(AFTER_CREATE)
    def do_after_create(self):
        pass

    @hook(AFTER_DELETE)
    def email_deleted_user(self):
        pass

class ArticleExample2(LifecycleModel, CommonInfo):
    pass

class ArticleExample3(LifecycleModel, CommonInfo):
    pass

class ArticleExample4(LifecycleModel, CommonInfo):
    pass

class ArticleExample5(LifecycleModel, CommonInfo):
    pass

class ArticleOverriting(CommonInfo):
    def save(self, *args, **kwargs):
        # something before
        super().save(*args, **kwargs)
        # something after

class ArticleSignal(CommonInfo):
    pass



# Signals


@receiver(pre_save, sender=ArticleSignal)
def call_pre_save(sender, **kwargs):
    pass

@receiver(post_save, sender=ArticleSignal)
def call_post_save(sender, **kwargs):
    pass

@receiver(pre_delete, sender=ArticleSignal)
def call_pre_delete(sender, **kwargs):
    pass

@receiver(post_delete, sender=ArticleSignal)
def call_pre_delete(sender, **kwargs):
    pass
