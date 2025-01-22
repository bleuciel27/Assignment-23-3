from rest_framework import serializers
from .models import Post, Comment
from cloudinary.utils import cloudinary_url
import logging

logger = logging.getLogger(__name__)

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
    image = serializers.ImageField(required=True)
    
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
        try:
            if not obj.image:
                logger.info(f"No image for post {obj.id}")
                return None
                
            if not hasattr(obj.image, 'public_id'):
                logger.info(f"No public_id for image in post {obj.id}")
                return obj.image.url if hasattr(obj.image, 'url') else None

            logger.info(f"Processing image for post {obj.id}")
            logger.info(f"Public ID: {obj.image.public_id}")
            
            url, _ = cloudinary_url(
                obj.image.public_id,
                format="jpg",
                crop="fill",
                width=800,
                height=600,
                quality="auto"
            )
            
            logger.info(f"Generated Cloudinary URL: {url}")
            return url
            
        except Exception as e:
            logger.error(f"Error processing image for post {obj.id}: {str(e)}")
            if hasattr(obj.image, 'url'):
                logger.info(f"Falling back to direct URL for post {obj.id}")
                return obj.image.url
            return None

    def create(self, validated_data):
        logger.info("Creating new post with data: %s", validated_data)
        try:
            instance = super().create(validated_data)
            logger.info("Successfully created post with ID: %s", instance.id)
            return instance
        except Exception as e:
            logger.error("Error creating post: %s", str(e))
            raise
