from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from sendingstonesapi.models import Comment, Gamer, Post

class CommentView(ViewSet):
    """Sending Stones comments view"""

    queryset = Comment.objects.none()

    def retrieve(self, request, pk=None):
        """Handle GET requests for single comment"""
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all comments"""
        comments = Comment.objects.all()
        gamer = Gamer.objects.get(user=request.auth.user)
        post = request.query_params.get('post', None)
        if post is not None:
            comments = Comment.objects.filter(post_id=post)
        else:
            comments = Comment.objects.all()

        for comment in comments:
            if comment.gamer == gamer:
                comment.can_edit = True
            else:
                comment.can_edit = False

        for comment in comments:
            if comment.gamer == gamer:
                comment.can_delete = True
            else:
                comment.can_delete = False
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized comment instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=request.data["post"])

        comment = Comment()
        comment.content = request.data["content"]
        comment.image_url = request.data["image_url"]
        comment.gamer = gamer
        comment.post = post
        comment.save()

        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        """Handle PUT requests for a comment

        Returns:
            Response -- Empty body with 204 status code
        """
        comment = Comment.objects.get(pk=pk)
        gamer = Gamer.objects.get(user=request.auth.user)

        if comment.gamer != gamer and comment.post.topic.game.game_master != gamer:
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        comment.content = request.data["content"]
        comment.image_url = request.data["image_url"]
        comment.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        """Handle DELETE requests for a comment"""
        comment = Comment.objects.get(pk=pk)
        gamer = Gamer.objects.get(user=request.auth.user)

        if comment.gamer != gamer and comment.post.topic.game.game_master != gamer:
            return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments"""
    class Meta:
        model = Comment
        fields = ('id', 'content', 'gamer', 'post', 'image_url', 'created_on', 'can_edit', 'can_delete')
        depth = 2