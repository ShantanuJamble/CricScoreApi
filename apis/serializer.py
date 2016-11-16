from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .views import WebScrapper


class GameListView(APIView):
    def get(self, request, *args, **kw):
        # add authenitcation here whenever needed
        scrapper = WebScrapper()
        result = scrapper.get_all_games()
        if result != '-1':
            response = Response(result, status.HTTP_200_OK)
        else:
            response = Response(None, status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response


class GameDetailView(APIView):
    def get(self, request, *args, **kw):
        # add authenitcation here whenever needed
        match_code = request.GET.get('match_code')
        scrapper = WebScrapper()
        result = scrapper.get_match_details(int(match_code))
        if result != '-1':
            response = Response(result, status.HTTP_200_OK)
        else:
            response = Response(None, status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response
