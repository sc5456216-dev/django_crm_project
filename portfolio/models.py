from django.db import models
from django.utils import timezone

class Skill(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class, e.g. 'fab fa-python'")
    level = models.PositiveSmallIntegerField(default=1, choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    technologies = models.ManyToManyField(Skill, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='portfolio/', blank=True, null=True)
    link = models.URLField(blank=True, help_text="Live demo or GitHub link")
    github = models.URLField(blank=True, help_text="GitHub repository link")
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
