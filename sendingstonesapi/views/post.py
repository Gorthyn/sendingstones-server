from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from sendingstonesapi.models import Post, Gamer, Topic, Game

class PostView(ViewSet):
    """Sending Stones posts view"""

    def get_queryset(self):
        queryset = Post.objects.all().select_related('gamer__user')
        return queryset

    def retrieve(self, request, pk=None):
        """Handle GET requests for single post"""
        try:
            post = Post.objects.select_related('gamer__user', 'topic__game__game_master').get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all posts for a specific topic"""
        topic_pk = request.query_params.get('topic', None)
        if topic_pk is not None:
            topic = get_object_or_404(Topic, pk=topic_pk)
            posts = Post.objects.filter(topic=topic)
        else:
            posts = Post.objects.all()
            
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized post instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        topic = Topic.objects.get(pk=request.data["topic"])

        post = Post()
        post.name = request.data["name"]
        post.content = request.data["content"]
        post.gamer = gamer
        post.topic = topic
        post.image_url = request.data["image_url"]
        post.save()

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        """Handle PUT requests for a post

        Returns:
            Response -- Empty body with 204 status code
        """
        post = Post.objects.get(pk=pk)
        gamer = Gamer.objects.get(user=request.auth.user)

        if post.gamer != gamer and post.topic.game.game_master != gamer:
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        post.name = request.data["name"]
        post.content = request.data["content"]
        post.image_url = request.data["image_url"]
        post.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        gamer = Gamer.objects.get(user=request.auth.user)

        if post.gamer != gamer and post.topic.game.game_master != gamer:
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for user"""
    class Meta:
        model = User
        fields = ('id', 'username')

class GamerSerializer(serializers.ModelSerializer):
    """JSON serializer for gamer"""
    user = UserSerializer(many=False)

    class Meta:
        model = Gamer
        fields = ('id', 'bio', 'user', 'games_moderated')
        depth = 1

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game"""
    game_master = GamerSerializer(many=False)

    class Meta:
        model = Game
        fields = ('id', 'name', 'description', 'game_master')
        depth = 1

class TopicSerializer(serializers.ModelSerializer):
    """JSON serializer for topic"""
    game = GameSerializer(many=False)

    class Meta:
        model = Topic
        fields = ('id', 'name', 'description', 'game')
        depth = 1

class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts"""
    gamer = GamerSerializer(many=False)
    topic = TopicSerializer(many=False)

    class Meta:
        model = Post
        fields = ('id', 'name', 'content', 'gamer', 'topic', 'image_url', 'created_on')
        depth = 2