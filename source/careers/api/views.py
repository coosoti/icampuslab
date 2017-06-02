from careers.models import Career 
from django.db.models import Q
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

from .pagination import CareerLimitOffsetPagination, CareerPageNumberPagination
from rest_framework.permissions import (
		AllowAny,
		IsAuthenticated,
		IsAdminUser,
		IsAuthenticatedOrReadOnly,

	)

from rest_framework.filters import (
	SearchFilter,
	OrderingFilter,
	)
from .permissions import IsOwnerOrReadOnly

from .serializers import (CareerCreateSerializer, 
	CareerListSerializer, 
	CareerDetailSerializer,
	)



class CareerCreateAPIView(CreateAPIView):
	queryset = Career.objects.all()
	serializer_class = CareerCreateSerializer
	# permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)


class CareerDetailAPIView(RetrieveAPIView):
	queryset = Career.objects.all()
	serializer_class = CareerDetailSerializer
	permission_classes = [AllowAny]
	lookup_field = 'slug'


class CareerUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Career.objects.all()
	serializer_class = CareerDetailSerializer
	lookup_field = 'slug'
	permission_classes = [IsOwnerOrReadOnly]

	def perform_update(self, serializer):
		serializer.save(user=self.request.user)


class CareerDeleteAPIView(DestroyAPIView):
	queryset = Career.objects.all()
	serializer_class = CareerDetailSerializer
	lookup_field = 'slug'
	permission_classes = [IsOwnerOrReadOnly]

class CareerListAPIView(ListAPIView):
	serializer_class = CareerListSerializer
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['title', 'description']
	permission_classes = [AllowAny]

	pagination_class = CareerPageNumberPagination #PageNumberPagination

	def get_queryset(self, *args, **kwargs):
		#queryset_list= super(CareerListAPIView, self).get_queryset(*args, **kwargs)
		queryset_list = Career.objects.all()
		query = self.request.GET.get("q")
		if query:
			queryset_list = queryset_list.filter(
				Q(title__icontains=query) |
				Q(description__icontains=query) 
				).distinct()
		return queryset_list


