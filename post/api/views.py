from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (ListAPIView,
                                     RetrieveAPIView,
                                     DestroyAPIView,
                                     CreateAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin

from post.api.paginations import PostPagination
from post.api.permissions import IsOwner
from post.api.serializers import PostSerializer, PostUpdateCreateSerializer
from post.models import Post
from rest_framework.permissions import (IsAuthenticated,)


class PostListAPIView(ListAPIView, CreateModelMixin):
    serializer_class = PostSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "content"]
    pagination_class = PostPagination

    def get_queryset(self):
        queryset = Post.objects.filter(draft=False)
        return queryset

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):    # postu oluşturan kullanıcının kendisi olmasını kontrol eder
        serializer.save(user = self.request.user)

class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'

class PostUpdateAPIView(RetrieveUpdateAPIView, DestroyModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostUpdateCreateSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwner]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save(modified_by = self.request.user)

class PostCreateAPIView(CreateAPIView, ListModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostUpdateCreateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)  #kullanıcının kendi user id'si için