from django.db import models
from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.dispatch import receiver
from django_lifecycle import LifecycleModel, hook, AFTER_CREATE, AFTER_UPDATE, AFTER_DELETE, BEFORE_SAVE, BEFORE_UPDATE, BEFORE_DELETE
from django.contrib.auth.models import AbstractUser
from model_utils.models import StatusModel
from model_utils import Choices

# Create your models here.

class User(AbstractUser):
    def __str__(self):
        return self.email


class CommonInfo(StatusModel):
    STATUS = Choices("draft", "published", "error", "banned")
    contents = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(null=True)
    editor =  models.OneToOneField(User, on_delete=models.CASCADE)
    is_trending = models.BooleanField(default=False)

    class Meta:
        abstract = True

class ArticleExample1(LifecycleModel, CommonInfo):
    @hook(AFTER_CREATE)
    def do_after_create(self):
        pass

    @hook(AFTER_DELETE)
    def do_after_deleted_user(self):
        pass

class ArticleExample2(LifecycleModel, CommonInfo):
    """Transitions among specific values
    """
    
    @hook(AFTER_UPDATE, when='status', was='active', is_now='banned')
    def after_banned_user(self):
        pass

class ArticleExample3(LifecycleModel, CommonInfo):
    """Preventing state transitions
    """

    @hook(BEFORE_DELETE, when='is_trending', is_now=True)
    def ensure_trial_not_active(self):
        pass

class ArticleExample4(LifecycleModel, CommonInfo):
    """Any change to a field
    """

    @hook(BEFORE_UPDATE, when='status', has_changed=True)
    def send_email_to_editor(self):
        pass

    
    @hook(BEFORE_SAVE, when='status', was_not="rejected", is_now="published")
    def send_publish_alerts(self):
        # send_mass_email()
        pass

    @hook(BEFORE_SAVE, when='status', changes_to="published")
    def send_publish_alerts(self):
        # send_mass_email()
        pass


class ArticleExample5(LifecycleModel, CommonInfo):
    """Stacking decorators
    """
    
    @hook(AFTER_UPDATE, when="published", has_changed=True)
    @hook(AFTER_CREATE, when="is_trending", has_changed=True)
    def handle_update(self):
        # do something
        pass


class ArticleExample6(LifecycleModel, CommonInfo):
    """Watching multiple fields
    """
    
    @hook(AFTER_UPDATE, when="published", has_changed=True)
    @hook(AFTER_CREATE, when="is_trending", has_changed=True)
    def handle_update(self):
        # do something
        pass

class ArticleExample7(LifecycleModel, CommonInfo):
    
    @hook(AFTER_UPDATE)
    def on_update(self):
        if self.has_changed('updated_at') and not self.has_changed('editor.username'):
            # do the thing here
            if self.initial_value('login_attempts') == 2:
                # do_thing()
                pass
            else:
                # do_other_thing()
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
