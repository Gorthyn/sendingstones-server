from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from sendingstonesapi.models import Game, Gamer
from rest_framework.decorators import action

class GameView(ViewSet):
    """Sending Stones games view"""

    queryset = Game.objects.none()

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game"""
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all games"""
        games = Game.objects.filter(game_master=Gamer.objects.get(user=request.auth.user))
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        game = Game()
        game.name = request.data["name"]
        game.description = request.data["description"]
        game.game_master = Gamer.objects.get(user=request.auth.user)
        game.save()

        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        game = Game.objects.get(pk=pk)

        if game.game_master != Gamer.objects.get(user=request.auth.user):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        game.name = request.data["name"]
        game.description = request.data["description"]
        game.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)

        if game.game_master != Gamer.objects.get(user=request.auth.user):
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['post'], detail=True)
    def invite(self, request, pk):
        """Post request for a game_master to invite a gamer to a game"""
        # Get the Gamer object for the user to be invited
        gamer_to_invite = Gamer.objects.get(user__username=request.data['username'])

        # Get the Game object based on the pk provided in the url
        game = Game.objects.get(pk=pk)

        # Make sure the current user is the game_master of the game
        if request.auth.user != game.game_master.user:
            return Response({'message': 'Only the game master can invite players'}, status=status.HTTP_403_FORBIDDEN)

        # Add the gamer to the game's players
        game.players.add(gamer_to_invite)

        return Response({'message': 'Gamer invited'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def remove(self, request, pk):
        """DELETE request for a game_master to remove a gamer from a game"""
        # Get the Gamer object for the user to be removed
        gamer_to_remove = Gamer.objects.get(user__username=request.data['username'])

        # Get the Game object based on the pk provided in the url
        game = Game.objects.get(pk=pk)

        # Make sure the current user is the game_master of the game
        if request.auth.user != game.game_master.user:
            return Response({'message': 'Only the game master can remove players'}, status=status.HTTP_403_FORBIDDEN)

        # Remove the gamer from the game's players
        game.players.remove(gamer_to_remove)

        return Response({'message': 'Gamer removed'}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """DELETE request for a gamer to leave a game"""
        # Get the Gamer object for the current user
        gamer = Gamer.objects.get(user=request.auth.user)

        # Get the Game object based on the pk provided in the url
        game = Game.objects.get(pk=pk)

        # Make sure the current user is a player in the game
        if gamer not in game.players.all():
            return Response({'message': 'You are not a player in this game'}, status=status.HTTP_403_FORBIDDEN)

        # Remove the gamer from the game's players
        game.players.remove(gamer)

        return Response({'message': 'You have left the game'}, status=status.HTTP_204_NO_CONTENT)


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    class Meta:
        model = Game
        fields = ('id', 'name', 'description', 'game_master')
        depth = 1