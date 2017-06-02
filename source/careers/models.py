from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify

from ckeditor_uploader.fields import RichTextUploadingField

from comments.models import Comment

# Create your models here.
class CareerManager(models.Manager):
	def active(self, *args,**kwargs):
		return super(CareerManager, self).filter(draft=False).filter(publish__lte=timezone.now())


class Category(models.Model):
	title = models.CharField(max_length = 120)
	slug = models.SlugField(unique= True)
	overview = models.TextField()
	updated = 	models.DateField(auto_now=True, auto_now_add=False, blank=True)
	timestamp = models.DateField(auto_now=False, auto_now_add=True, blank=True)

	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title

def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)

class Career(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default = 1)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, db_index = True)
	title = models.CharField(max_length = 120)
	slug = models.SlugField(unique = True)
	image = models.ImageField(upload_to=upload_location, 
			null=True, 
			blank=True, 
			width_field="width_field", 
			height_field="height_field")
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	description = RichTextUploadingField()
	entry = models.CharField(max_length = 120)
	experience = RichTextUploadingField()
	education = RichTextUploadingField()
	draft = models.BooleanField(default=False)
	publish = models.DateField(auto_now=False, auto_now_add=False)
	updated = 	models.DateField(auto_now=True, auto_now_add=False)
	timestamp = models.DateField(auto_now=False, auto_now_add=True)
	#prof_courses = models.CharField()
	#skills = models.CharField()

	objects = CareerManager()

	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
			super(Career, self).save(*args, **kwargs)


	def get_absolute_url(self):
		return reverse("careers:detail", kwargs = {"slug": self.slug})

	def get_api_url(self):
		return reverse("careers-api:detail", kwargs = {"slug": self.slug})

	@property
	def comments(self):
		instance = self
		qs = Comment.objects.filter_by_instance(instance)
		return qs

	@property
	def get_content_type(self):
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type