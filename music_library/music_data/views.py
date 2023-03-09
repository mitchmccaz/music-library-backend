from django.http import Http404
from .models import Song
from .serializers import SongSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'SongList': 'music/',
        'SongDetail': 'music/<int:pk>'
    }
    return Response(api_urls)


class SongList(APIView):
    """
    This SongList class is used to allow a front-end users to easily identify and manipulate a list of songs in
    my current MySQL database.
    """

    def get(self, request):
        """
        Get all the songs in the current list of songs.
        :param request: Comes from the client.
        :return: The list of songs.
        """
        song = Song.objects.all()
        # Converts all objects into JSON
        serializer = SongSerializer(song, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Creates a song object with input from client.
        :param request: Comes from client.
        :return: Will return a Song object to push into the database.
        """
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SongDetail(APIView):
    """
    This SongDetail class is used to allow a front-end users to easily identify and manipulate specific
     songs in a list of songs contained in my current MySQL database.
    """

    def get_object(self, pk):
        """
        Allows you to search for a Song contained in the current MySQL database containing all the song objects.
        :param pk: Given by the client.
        :return: The specific details of a song in a Song object.
        """
        try:
            return Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        song = self.get_object(pk)
        serializer = SongSerializer(song)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Allows you to update a specific object inside of the current list of Song objects thats contained in the
        MySQL database.
        :param request:Taken in from the client.
        :param pk: The specific Song tht the client wants to manipulate. (It's location.)
        :return: The updated Song object.
        """
        song = self.get_object(pk)
        serializer = SongSerializer(song, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Can be used to isolate any specific attribute inside of Song. In this case, it's being
        used to isolate the number of likes inside of the current Song model being viewed.
        :param request: Taken in from the client.
        :param pk: The specific Song that the client wants to manipulate. (It's location.)
        :return: The updated Song object.
        """
        song = self.get_object(pk)
        song.likes += 1
        serializer = SongSerializer(song, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Deletes the Song that is searched by the client wanting to delete it.
        :param request: Taken in from the client.
        :param pk: The specific Song that the client wants to manipulate (It's location)
        :return: A response to the client stating that there is no content.
        """
        song = self.get_object(pk)
        song.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)