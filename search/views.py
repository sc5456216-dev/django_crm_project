from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from contacts.models import Contact
from companies.models import Company
from deals.models import Deal
from tasks.models import Task


@login_required
def global_search(request):
    query = request.GET.get("q", "").strip()

    contacts = Contact.objects.none()
    companies = Company.objects.none()
    deals = Deal.objects.none()
    tasks = Task.objects.none()

    if query:

        contacts = Contact.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )

        companies = Company.objects.filter(
            Q(name__icontains=query)
        )

        deals = Deal.objects.filter(
            Q(title__icontains=query)
        )

        tasks = Task.objects.filter(
            Q(title__icontains=query)
        )

        # Sales Rep can only search their own records
        if request.user.groups.filter(name="Sales Rep").exists():
            contacts = contacts.filter(assigned_to=request.user)
            companies = companies.filter(assigned_to=request.user)
            deals = deals.filter(assigned_to=request.user)
            tasks = tasks.filter(assigned_to=request.user)

    context = {
        "query": query,
        "contacts": contacts,
        "companies": companies,
        "deals": deals,
        "tasks": tasks,
    }

    return render(request, "search/search.html", context)