from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
	pass

class Note(models.Model):
	creator = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "creator")
	note = models.CharField(max_length = 50000)
	title = models.CharField(max_length = 100)
	timestamp = models.DateTimeField(auto_now_add=True)
	def serialize(self):
		return {
			"timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
		}