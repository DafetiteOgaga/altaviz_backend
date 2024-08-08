from django.db import models

# Create your models here.
class Product(models.Model):
	product_images = models.ImageField(upload_to='product_images/')
	title = models.CharField(max_length=100)
	# descriptions = models.OneToOneField('Description', on_delete=models.CASCADE, related_name='description', null=True, blank=True)
	def __str__(self) -> str:
		return f'{self.title} - product'

class Description(models.Model):
	product = models.OneToOneField('Product', on_delete=models.CASCADE, related_name='description', null=True, blank=True)
	about = models.TextField()
	feature = models.CharField(max_length=100)
	benefit = models.CharField(max_length=100)
	conclusion = models.CharField(max_length=500)

	def __str__(self) -> str:
		return f'{self.product.title} -- description'
	
class Feature(models.Model):
	description = models.ForeignKey('Description', on_delete=models.CASCADE, related_name='features')
	head = models.CharField(max_length=200)
	body = models.TextField(max_length=500)

	def __str__(self) -> str:
		return f'{self.description.product.title} - features'

class Benefit(models.Model):
	description = models.ForeignKey('Description', on_delete=models.CASCADE, related_name='benefits')
	head = models.CharField(max_length=200)
	body = models.TextField(max_length=500)

	def __str__(self) -> str:
		return f'{self.description.product.title} - benefits'
