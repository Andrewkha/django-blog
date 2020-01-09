from django.db import models

# Create your models here.
from datetime import date
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    bio = models.TextField(max_length=2000, help_text='Put your bio here')

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['user', 'bio']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.user.id)])


@receiver(post_save, sender=User)
def create_author(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_author(sender, instance, **kwargs):
    instance.author.save()


class Post(models.Model):
    title = models.CharField(max_length=200, help_text='Post title', verbose_name='Post title')
    description = models.TextField(help_text='The post contents')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateField(default=date.today)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']

    def get_absolute_url(self):
        return reverse('post-details', args=[str(self.id)])


class Comment(models.Model):
    """
    Model representing a comment against a blog post.
    """
    description = models.TextField(max_length=1000, help_text="Enter comment about blog here.")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # Foreign Key used because BlogComment can only have one author/User, but users can have multiple comments
    post_date = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        ordering = ["post_date"]

    def __str__(self):
        """
        String for representing the Model object.
        """
        len_title = 75
        if len(self.description) > len_title:
            titlestring = self.description[:len_title] + '...'
        else:
            titlestring = self.description
        return titlestring
