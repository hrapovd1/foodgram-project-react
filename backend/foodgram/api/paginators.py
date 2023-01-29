from rest_framework.pagination import PageNumberPagination


class FoodgramPagination(PageNumberPagination):
    """Переопределяю параметры стандартного пагинатора"""
    page_size_query_param = 'limit'