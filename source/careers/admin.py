from django.contrib import admin

# Register your models here.
from .models import Category, Career

class CategoryModelAdmin(admin.ModelAdmin):
	list_display = ["title", "updated", "timestamp", "updated"]
	list_display_links = ["title", "updated"]
	list_filter = ["title", "timestamp"]
	search_fields = ["title"]
	prepopulated_fields = {'slug': ('title',)}


	class Meta:
		model = Category

admin.site.register(Category, CategoryModelAdmin)


class CareerModelAdmin(admin.ModelAdmin):
	list_display = ["title", "category", "timestamp", "updated"]
	list_display_links = ["title", "updated"]
	list_filter = ["category","title", "timestamp"]
	search_fields = ["category", "title"]
	prepopulated_fields = {'slug': ('title',)}
	class Meta:
		model = Career

admin.site.register(Career, CareerModelAdmin)