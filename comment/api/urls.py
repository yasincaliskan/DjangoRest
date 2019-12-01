from django.urls import path
from comment.api.views import (CommentCreateAPIView,)

app_name = "comment"

urlpatterns = [
    path('create', CommentCreateAPIView.as_view(), name='create'),

]
