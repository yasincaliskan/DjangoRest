from rest_framework.generics import CreateAPIView
from comment.api.serializers import CommentCreateSerializer
from comment.models import Comment

class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

