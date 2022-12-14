from django.db import models
from django.urls import reverse
from users.models import User


class Image(models.Model):
    class Meta:
        db_table = 'image'

    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    image_url = models.CharField(max_length=1000000, null=True)
    before_image = models.ImageField(upload_to="before_image", blank=True, null=True)
    model = models.CharField(max_length=1000, null=True)
    after_image = models.ImageField(upload_to="after_image", blank=True, null=True)

class ImageModel(models.Model):
    class Meta:
        db_table = 'image_model'
        
    model_path = models.CharField(max_length=200)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    title = models.CharField(max_length=50)
    content = models.TextField()
    image = models.OneToOneField(Image, on_delete=models.CASCADE, related_name='images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='like_posts')

    def get_absolute_url(self):
        return reverse('post_detail_view', kwargs={"post_id":self.id})
     
    def __str__(self):
        return str(self.title)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.content)
        