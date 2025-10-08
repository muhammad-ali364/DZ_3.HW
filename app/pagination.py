from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustonPagination(PageNumberPagination):
    poge_size = 3
    page_query_param = "page_size"
    max_page_size = 10 

    def get_poginated_response(self , date):
        return Response({
            "mate":{
                "tatal_items" : self.page.paginator.count,
                "tatal_pogez" : self.poge.paginator.num_poges,
                "current_page" : self.get_page.number,
                "page_size" : self.get_page_size(self.request),
                "next" : self.get_next_link(),
                "previus" : self.get_previous_link(),
            },
            "results" : date 
        })

