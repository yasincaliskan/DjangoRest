from rest_framework.serializers import ModelSerializer

from comment.models import Comment


class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['created',] # tüm field 'ları alır. içerisinde 'created' olanı çıkarır.

    def validate(self, attrs):
        if(attrs["parent"]):
            if attrs["parent"].post != attrs["post"]:
                return attrs

