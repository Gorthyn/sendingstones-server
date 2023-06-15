from rest_framework import permissions, serializers
from rest_framework.viewsets import ViewSet
from sendingstonesapi.models import Invitation, Gamer, PlayerGame, Game
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['id', 'sender', 'receiver', 'status', 'game']
        depth = 2

class InvitationView(ViewSet):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        invitations = Invitation.objects.all()
        receiver = Gamer.objects.get(user=request.auth.user)
        invitation = invitations.filter(receiver=receiver)
        serializer = InvitationSerializer(invitation, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            invitation = Invitation.objects.get(pk=pk)
        except Invitation.DoesNotExist:
            raise Http404

        serializer = InvitationSerializer(invitation)
        return Response(serializer.data)

    def create(self, request):
        serializer = CreateInvitationSerializer(data=request.data)
        sender = Gamer.objects.get(user = request.auth.user)
        game = Game.objects.get(pk=request.data["game"])
        receiver_id = request.data.get('receiver')
        print(f'Sender ID: {sender.id}, Receiver ID: {receiver_id}')
        try:
            receiver = Gamer.objects.get(id=receiver_id)
            print(f'Receiver exists: {receiver is not None}')
        except Gamer.DoesNotExist:
            print('Receiver does not exist')
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=sender, receiver=receiver, game=game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        try:
            invitation = Invitation.objects.get(pk=pk)
        except Invitation.DoesNotExist:
            raise Http404

        serializer = InvitationSerializer(invitation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            if serializer.validated_data.get('status') == 'accepted':
                player_game_data = {
                    'game': invitation.game.id,
                    'gamer': Gamer.objects.get(user=request.auth.user).id,
                    'role': 'player'
                }
                player_game_serializer = PlayerGameSerializer(data=player_game_data)
                if player_game_serializer.is_valid():
                    player_game_serializer.save()
                else:
                    return Response(player_game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            invitation = Invitation.objects.get(pk=pk)
        except Invitation.DoesNotExist:
            raise Http404

        invitation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CreateInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['id', 'receiver_id', 'status', 'game']
        depth = 1

class PlayerGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerGame
        fields = ['game', 'gamer', 'role']
