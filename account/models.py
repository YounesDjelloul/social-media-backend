from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserManager(BaseUserManager):
	
	def create_user(self, username, password1, password2):
		user = User(username=username)
		user.set_password(password1)
		user.save()

		return user

	def create_superuser(self, username, password):
		user = User(username=username, is_staff=True, is_superuser=True)
		user.set_password(password)
		user.save()

		return user

class User(AbstractUser):

	email           = None
	firstname       = None
	lastname        = None

	REQUIRED_FIELDS = []
	objects         = UserManager()

	def __str__(self):
		return self.username

class Profile(models.Model):

	user      = models.OneToOneField(User, on_delete=models.CASCADE)
	fullname  = models.CharField(max_length=120)
	bio       = models.TextField(default='', null=True, blank=True)
	birthdate = models.DateField(null=True, blank=True)

	def __str__(self):
		return self.fullname

@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
	if kwargs['created']:
		Profile.objects.create(user=kwargs['instance'], fullname=kwargs['instance'].username)

class Friend(models.Model):

	first_user  = models.ForeignKey(User, related_name='first_user', on_delete=models.CASCADE)
	second_user = models.ForeignKey(User, related_name='second_user', on_delete=models.CASCADE)
	chat_id     = models.CharField(max_length=1000, default='')

	def __str__(self):
		return str(self.chat_id)

class FriendRequest(models.Model):
	
	sender   = models.ForeignKey(User, related_name='request_sender', on_delete=models.CASCADE)
	receiver = models.ForeignKey(User, related_name='request_receiver', on_delete=models.CASCADE)

	def __str__(self):
		return str(self.sender)

class Message(models.Model):
	sender   = models.ForeignKey(User, related_name='message_sender', on_delete=models.CASCADE)
	receiver = models.ForeignKey(User, related_name='message_receiver', on_delete=models.CASCADE)
	content  = models.TextField(default='')

	def __str__(self):
		return str(self.sender)