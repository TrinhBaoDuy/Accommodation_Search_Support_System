from rest_framework.pagination import PageNumberPagination


class ASSSPaginator(PageNumberPagination):
    page_size = 5

