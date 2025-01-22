# posts/management/commands/create_test_data.py
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from users.models import User
from posts.models import Post, Comment
from decimal import Decimal
import base64

class Command(BaseCommand):
    help = 'Creates initial test data for Sparta Store'

    def handle(self, *args, **kwargs):
        # Create test users
        self.stdout.write('Creating test users...')
        
        # Create main test user
        main_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            bio='A test user who loves shopping'
        )
        
        # Create seller
        seller = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='seller123',
            bio='Experienced seller with great items'
        )

        # Sample product data
        products = [
            {
                'title': 'Harry Potter Complete Collection',
                'description': 'All 7 books in excellent condition. Perfect for Potter fans!',
                'price': Decimal('79.99'),
                'category': 'BOOKS',
                'condition': 'Excellent',
                'seller': seller
            },
            {
                'title': 'Lululemon Yoga Pants',
                'description': 'Size M, Black color, worn only twice',
                'price': Decimal('45.00'),
                'category': 'CLOTHING',
                'condition': 'Like New',
                'seller': seller
            },
            {
                'title': 'New Balance Running Shoes',
                'description': 'Men\'s size 10, perfect for running or casual wear',
                'price': Decimal('55.00'),
                'category': 'CLOTHING',
                'condition': 'Good',
                'seller': main_user
            }
        ]

        # Create posts
        self.stdout.write('Creating posts...')
        for product in products:
            # Create a simple base64 image for testing
            image_data = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=')
            
            post = Post.objects.create(
                title=product['title'],
                description=product['description'],
                price=product['price'],
                category=product['category'],
                condition=product['condition'],
                seller=product['seller']
            )
            
            # Add test image
            post.image.save('test_image.png', ContentFile(image_data), save=True)
            
            # Add some likes
            post.likes.add(main_user)
            
            # Add a comment
            Comment.objects.create(
                post=post,
                user=main_user,
                content=f'Interested in this {post.title}! Is it still available?'
            )

        self.stdout.write(self.style.SUCCESS('Successfully created test data'))