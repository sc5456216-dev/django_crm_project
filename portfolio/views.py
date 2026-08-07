from django.shortcuts import render, get_object_or_404
from .models import Project, Skill, Category

def portfolio_list(request):
    projects = Project.objects.all()
    skills = Skill.objects.all()
    categories = Category.objects.all()
    featured = Project.objects.filter(featured=True)
    context = {
        'projects': projects,
        'skills': skills,
        'categories': categories,
        'featured': featured,
    }
    return render(request, 'portfolio/list.html', context)

def portfolio_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'portfolio/detail.html', {'project': project})
