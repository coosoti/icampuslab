from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.generics import (
	CreateAPIView,
	DestroyAPIView,
	ListAPIView, 
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	UpdateAPIView,
	)
from rest_framework.pagination import (
	LimitOffsetPagination,
	PageNumberPagination,
	)

from careers.api.pagination import CareerLimitOffsetPagination, CareerPageNumberPagination
from careers.api.permissions import IsOwnerOrReadOnly

from rest_framework.permissions import (
		AllowAny,
		IsAuthenticated,
		IsAdminUser,
		IsAuthenticatedOrReadOnly,

	)

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView 

from rest_framework.filters import (
	SearchFilter,
	OrderingFilter,
	)

User = get_user_model()

from .serializers import ( 
	UserCreateSerializer,
	UserLoginSerializer,
	)



class UserCreateAPIView(CreateAPIView):
	serializer_class = UserCreateSerializer
	queryset = User.objects.all()
	permission_classes = [AllowAny]


class UserLoginAPIView(APIView):
	permission_class = [AllowAny]
	serializer_class = UserLoginSerializer

	def post(self, request, *args, **kwargs):
		data = request.data
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			new_data = serializer.data 
			return Response(new_data, status=HTTP_200_OK)
		return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

		
