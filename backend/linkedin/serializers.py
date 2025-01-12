from rest_framework import serializers
from .enums import SuggestionItemEnum
from .models import Post
class SuggestionSerializer(serializers.Serializer):
    suggestion_item = serializers.ChoiceField(
        choices=[(item.value, item.name) for item in SuggestionItemEnum]
    )
    content = serializers.CharField(max_length=500)

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty or just spaces.")
        return value


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'