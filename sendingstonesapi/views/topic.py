from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.shortcuts import get_object_or_404
from sendingstonesapi.models import Topic, Game, Gamer

class TopicView(ViewSet):
    """Sending Stones topics view"""

    queryset = Topic.objects.none()

    def retrieve(self, request, pk=None):
        """Handle GET requests for single topic"""
        try:
            topic = Topic.objects.get(pk=pk)
            serializer = TopicSerializer(topic)
            return Response(serializer.data)
        except Topic.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all topics for a specific game"""
        # Get the 'game' query parameter, if it exists
        game_pk = request.query_params.get('game', None)

        if game_pk is not None:
            # Try to retrieve the game with the given primary key
            game = get_object_or_404(Game, pk=game_pk)
            # If the game exists, retrieve all topics associated with that game
            topics = Topic.objects.filter(game=game)
        else:
            # If 'game' is not provided, retrieve all topics
            topics = Topic.objects.all()

        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized topic instance
        """
        game = Game.objects.get(pk=request.data["game"])
        if game.game_master != Gamer.objects.get(user=request.auth.user):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        topic = Topic()
        topic.name = request.data["name"]
        topic.description = request.data["description"]
        topic.game = game
        topic.save()

        serializer = TopicSerializer(topic)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        """Handle PUT requests for a topic

        Returns:
            Response -- Empty body with 204 status code
        """
        topic = Topic.objects.get(pk=pk)
        game = Game.objects.get(pk=request.data["game"])
        if game.game_master != Gamer.objects.get(user=request.auth.user):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        topic.name = request.data["name"]
        topic.description = request.data["description"]
        topic.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        topic = Topic.objects.get(pk=pk)
        if topic.game.game_master != Gamer.objects.get(user=request.auth.user):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        topic.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class TopicSerializer(serializers.ModelSerializer):
    """JSON serializer for topics"""
    class Meta:
        model = Topic
        fields = ('id', 'name', 'description', 'game')
        depth = 1
