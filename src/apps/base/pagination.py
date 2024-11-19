from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_query_param = "page"
    page_size_query_param = "per_page"
    max_page_size = 100
