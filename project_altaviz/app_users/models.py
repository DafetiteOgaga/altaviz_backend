from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone
import os, uuid, io
from PIL import Image
# from django.conf import settings

# Create your models here.
# renames the profile pictures before being saved to for unique identification
def unique_profile_pic(instance, filename):
	base, ext = os.path.splitext(filename)
	unique_id = uuid.uuid4().hex
	new_filename = f"{base}_{unique_id}_{timezone.now().strftime('%Y%m%d%H%M%S')}{ext}"
	return os.path.join('profile_pictures', new_filename)

class User(AbstractUser):
	middle_name = models.CharField(max_length=100, null=True, blank=True)
	email = models.EmailField(max_length=200, unique=True)
	username = models.CharField(max_length=15, unique=True)
	# username = None
	phone = models.CharField(null=True, blank=True, max_length=15)
	wphone = models.CharField(max_length=15)
	phone3 = models.CharField(null=True, blank=True, max_length=15)
	address = models.CharField(max_length=200)
	department = models.CharField(null=True, blank=True, max_length=50)
	deliveries = models.IntegerField(default=0)
	# website = models.URLField(max_length=200, null=True, blank=True)
	profile_picture = models.ImageField(upload_to=unique_profile_pic, null=True, blank=True, default='profile_pictures/placeholder.png')
	# number_of_articles = models.ForeignKey(null=True, blank=True,)
	# rating = models.ForeignKey(null=True, blank=True)
	aboutme = models.TextField()
	# profile_picture = None

	# groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
	# user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	def __str__(self):
		return self.username

	def save(self, *args, **kwargs):
		print('entering save method ###### 1')
		print(f'isinstance(self.profile_picture, InMemoryUploadedFile: {isinstance(self.profile_picture, InMemoryUploadedFile)}')
		if (self.profile_picture or isinstance(self.profile_picture, InMemoryUploadedFile)) and self.first_name:
			img = Image.open(self.profile_picture)
			if img.mode != 'RGB':
				img = img.convert('RGB')
			min_dim = min(img.width, img.height)
			left = (img.width - min_dim) / 2
			top = (img.height - min_dim) / 2
			right = (img.width + min_dim) / 2
			bottom = (img.height + min_dim) / 2
			img = img.crop((left, top, right, bottom))
			target_size = (200, 200)
			img = img.resize(target_size, Image.LANCZOS)
			output = io.BytesIO()
			img.save(output, format='JPEG', quality=100)
			output.seek(0)
			self.profile_picture = InMemoryUploadedFile(
				output, 'ImageField',
				f"{unique_profile_pic(self, self.profile_picture.name)}",
				'image/jpeg',
				output.getbuffer().nbytes,
				None
			)

		super().save(*args, **kwargs)
