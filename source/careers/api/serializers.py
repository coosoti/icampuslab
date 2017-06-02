from rest_framework.serializers import (
	HyperlinkedIdentityField,
	ModelSerializer, 
	SerializerMethodField,
	)
from accounts.api.serializers import UserDetailSerializer
from comments.api.serializers import CommentSerializer
from comments.models import Comment 
from careers.models import Career 




career_detail_url = HyperlinkedIdentityField(
		view_name = "careers-api:detail",
		lookup_field = "slug",
		)

class CareerCreateSerializer(ModelSerializer):
	class Meta:
		model = Career
		fields = [
			"title",
			"category",
			"description",
			"entry",
			"experience",
			"education",
			"publish",
		]


class CareerDetailSerializer(ModelSerializer):
	url = career_detail_url
	user = UserDetailSerializer(read_only=True)
	image = SerializerMethodField()
	comments = SerializerMethodField()
	class Meta:
		model = Career
		fields = [
			"url",
			"user",
			"title",
			"category",
			"description",
			"entry",
			"experience",
			"education",
			"publish",
			"image",
			"comments",
		]

	def get_image(self, obj):
		try:
			image = obj.image.url
		except:
			image = None
		return image 

	def get_comments(self, obj):
		c_qs = Comment.objects.filter_by_instance(obj) 
		comments = CommentSerializer(c_qs, many=True).data
		return comments


class CareerListSerializer(ModelSerializer):
	url = career_detail_url
	user = UserDetailSerializer(read_only=True)
	image = SerializerMethodField()
	class Meta:
		model = Career
		fields = [
			"url",
			"user",
			"title",
			"category",
			"image",
			"description",
			"entry",
			"experience",
			"education",
		]

	def get_image(self, obj):
		try:
			image = obj.image.url
		except:
			image = None
		return image 

