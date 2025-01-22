from rest_framework import serializers
from .models import Post, Comment
from cloudinary.utils import cloudinary_url

class CommentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ('id', 'post', 'user', 'user_username', 'content', 'created_at')
        read_only_fields = ('user',)

class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    seller_username = serializers.CharField(source='seller.username', read_only=True)
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'price', 'category', 'condition',
                'image', 'seller', 'seller_username', 'likes_count', 'is_liked',
                'comments', 'created_at')
        read_only_fields = ('seller',)

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

    def get_image(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            try:
                # Get the Cloudinary URL with transformations
                url, options = cloudinary_url(
                    obj.image.public_id,
                    format="jpg",
                    crop="fill",
                    width=800,
                    height=600,
                    quality="auto"
                )
                return url
            except Exception as e:
                print(f"Error getting Cloudinary URL: {e}")
                # Fall back to direct URL if cloudinary_url fails
                return obj.image.url if hasattr(obj.image, 'url') else None
        return None
