from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size=12
    ordering ='id'
    page_size_query_param='page_size'
    max_page_size = 1000


class JobPagination(PageNumberPagination):
    page_size=10
    ordering ='id'
    page_size_query_param='page_size'
    max_page_size = 1000


class NotificationPagination(PageNumberPagination):
    page_size=10
    ordering ='id'
    page_size_query_param='page_size'
    max_page_size = 1000