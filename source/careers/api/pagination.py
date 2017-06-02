from rest_framework.pagination import (
	LimitOffsetPagination,
	PageNumberPagination,
	)

class CareerLimitOffsetPagination(LimitOffsetPagination):
	default_limit = 2
	max_limit = 10


class CareerPageNumberPagination(PageNumberPagination):
	page_size = 10