from django.db import models
from autoslug import AutoSlugField
from django.utils.text import slugify
from django.utils import timezone
# Create your models here.


class Category(models.Model):

    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="name", unique=True, null=True, default=None)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
 
            self.slug = f"{base_slug}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name 


class Blog(models.Model):

    STATUS={
        ('0',"Draft"),
        ('1','Publish')
    }

    SECTION = {
        ('Popular', 'Popular'),
        ('Recent', 'Recent'),
        ('Trending', 'Trending')
    }

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    author_email = models.EmailField(max_length=255, null=True, blank=True)
    author_image = models.ImageField(upload_to="author_images/", null=True, blank=True)
    image = models.ImageField(upload_to="images")
    content = models.TextField()
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    blog_slug  = AutoSlugField(populate_from = 'title', unique=True,null=True, default=None)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(choices=STATUS, max_length=1, default=0)
    section = models.CharField(choices=SECTION, max_length=100)
    Main_post = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.category})"
    


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    blog_id =  models.IntegerField(blank=True,null=True)
    name = models.CharField(max_length=100)
    comment = models.TextField()
    date = models.DateField(default=timezone.now)
    parent = models.ForeignKey('self',null=True, blank=True, on_delete=models.CASCADE,related_name='replies')

    def save(self, *args, **kwargs):
        # Automatically set the blog_id when saving a comment
        if self.post:
            self.blog_id = self.post.id
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Comment ID {self.id} on Blog Post ID {self.blog_id} by {self.name}: {self.comment[:20]}'
