from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Contact
from .forms import ContactForm
from accounts.decorators import admin_required, manager_required

import openpyxl
from django.http import HttpResponse


@login_required
def contact_list(request):
    # Sales Rep can only see their assigned contacts
    if request.user.groups.filter(name='Sales Rep').exists():
        contacts = Contact.objects.filter(assigned_to=request.user)
    else:
        contacts = Contact.objects.all()

    search = request.GET.get('search')
    if search:
        contacts = contacts.filter(first_name__icontains=search) | contacts.filter(email__icontains=search)

    return render(request, 'contacts/contact_list.html', {
        'contacts': contacts,
        'total': contacts.count(),
        'is_admin': request.user.groups.filter(name='Admin').exists(),
        'is_manager': request.user.groups.filter(name__in=['Admin', 'Sales Manager']).exists(),
    })


@login_required
def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)

    # Sales Rep can only view their own assigned contacts
    if request.user.groups.filter(name='Sales Rep').exists():
        if contact.assigned_to != request.user:
            raise PermissionDenied("You can only view your assigned contacts.")

    return render(request, 'contacts/contact_detail.html', {'contact': contact})


@login_required
@manager_required
def contact_create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact added successfully!')
            return redirect('contact_list')
    else:
        form = ContactForm()
    return render(request, 'contacts/contact_form.html', {'form': form})


@login_required
@manager_required
def contact_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact updated successfully!')
            return redirect('contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'contacts/contact_form.html', {'form': form})


@login_required
@admin_required
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, 'Contact deleted successfully!')
        return redirect('contact_list')
    return render(request, 'contacts/contact_confirm_delete.html', {'contact': contact})


@login_required
def export_contacts_excel(request):
    # Create workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Contacts"
    
    # Header
    headers = ['ID', 'First Name', 'Last Name', 'Email', 'Phone', 'Company', 'Job Title', 'Status', 'Created Date']
    ws.append(headers)
    
    # Data
    contacts = Contact.objects.all()
    for contact in contacts:
        ws.append([
            contact.id,
            contact.first_name,
            contact.last_name,
            contact.email,
            contact.phone,
            contact.company,
            contact.job_title,
            contact.status,
            contact.created_at.strftime('%Y-%m-%d')
        ])
    
    # Response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=contacts.xlsx'
    wb.save(response)
    return response