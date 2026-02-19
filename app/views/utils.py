from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'results': data,
            'page': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'current_page': self.page.number,
            'per_page': self.page.paginator.per_page
            
        })