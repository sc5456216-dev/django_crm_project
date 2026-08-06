from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Company
from .forms import CompanyForm
from accounts.decorators import admin_required, manager_required


@login_required
def company_list(request):
    if request.user.groups.filter(name='Sales Rep').exists():
        companies = Company.objects.filter(assigned_to=request.user)
    else:
        companies = Company.objects.all()

    search = request.GET.get('search')
    if search:
        companies = companies.filter(name__icontains=search)

    return render(request, 'companies/company_list.html', {
        'companies': companies,
        'total': companies.count(),
        'is_admin': request.user.groups.filter(name='Admin').exists(),
        'is_manager': request.user.groups.filter(name__in=['Admin', 'Sales Manager']).exists(),
    })


@login_required
def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)

    if request.user.groups.filter(name='Sales Rep').exists():
        if company.assigned_to != request.user:
            raise PermissionDenied("You can only view your assigned companies.")

    return render(request, 'companies/company_detail.html', {'company': company})


@login_required
@manager_required
def company_create(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company added successfully!')
            return redirect('company_list')
    else:
        form = CompanyForm()
    return render(request, 'companies/company_form.html', {'form': form})


@login_required
@manager_required
def company_update(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company updated successfully!')
            return redirect('company_list')
    else:
        form = CompanyForm(instance=company)
    return render(request, 'companies/company_form.html', {'form': form})


@login_required
@admin_required
def company_delete(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        company.delete()
        messages.success(request, 'Company deleted successfully!')
        return redirect('company_list')
    return render(request, 'companies/company_confirm_delete.html', {'company': company})