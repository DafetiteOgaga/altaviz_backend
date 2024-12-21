from django.db import models
from app_users.models import User
# from django.core.files.uploadedfile import InMemoryUploadedFile
# from django.utils import timezone
# import os, uuid, io
from PIL import Image
# from django.db.models import F

# def process_avatar(self, image_path):
# 	"""Resize and convert image to a standard avatar format."""
# 	print(f'Processing avatar: {image_path}')
# 	with Image.open(image_path) as img:
# 		# Convert to RGB mode if not already
# 		if img.mode != 'RGB':
# 			print('Converting image to RGB mode')
# 			img = img.convert('RGB')

# 		# Resize the image to 128x128
# 		img = img.resize((128, 128), Image.Resampling.LANCZOS)
# 		print('Resized image to 128x128')

# 		# Save the processed image back to the same path
# 		img.save(image_path)
# 		print('Saved processed avatar')

# Create your models here.
class Chat(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats', db_index=True, null=True, blank=True)
	contact = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts', db_index=True, null=True, blank=True)
	# youAvatar = models.ImageField(upload_to='avatars', default='avatars/placeholder.png')
	# contaAvatar = models.ImageField(upload_to='avatars', default='avatars/placeholder.png')
	message = models.TextField(null=True, blank=True)
	# youMessage = models.TextField(null=True, blank=True)
	# contactMessage = models.TextField(null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	class Meta:
		ordering = ['timestamp']
		indexes = [
			models.Index(fields=['user', 'contact'], name='user_contact_idx'),
			models.Index(fields=['contact', 'user'], name='contact_user_idx'),
		]

	# def save(self, *args, **kwargs):
	# 	print('Saving chat message')

	# 	# Call the parent class save method to handle the initial saving
	# 	super().save(*args, **kwargs)

	# 	# Process avatars
	# 	if self.youAvatar and self.youAvatar.path:
	# 		self.process_avatar(self.youAvatar.path)

	# 	if self.contaAvatar and self.contaAvatar.path:
	# 		self.process_avatar(self.contaAvatar.path)
