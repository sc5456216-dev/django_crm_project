from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.db.models import Q

import openpyxl

from .models import Contact
from .forms import ContactForm

from accounts.decorators import admin_required, manager_required
from activities.utils import create_activity
from notifications.utils import create_notification


@login_required
def contact_list(request):
    # Sales Rep can only see assigned contacts
    if request.user.groups.filter(name="Sales Rep").exists():
        contacts = Contact.objects.filter(
            assigned_to=request.user
        )
    else:
        contacts = Contact.objects.all()

    search = request.GET.get("search")

    if search:
        contacts = contacts.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )

    context = {
        "contacts": contacts,
        "total": contacts.count(),
        "is_admin": request.user.groups.filter(
            name="Admin"
        ).exists(),
        "is_manager": request.user.groups.filter(
            name__in=["Admin", "Sales Manager"]
        ).exists(),
    }

    return render(
        request,
        "contacts/contact_list.html",
        context
    )


@login_required
def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)

    if request.user.groups.filter(name="Sales Rep").exists():
        if contact.assigned_to != request.user:
            raise PermissionDenied(
                "You can only view your assigned contacts."
            )

    return render(
        request,
        "contacts/contact_detail.html",
        {
            "contact": contact
        }
    )


@login_required
@manager_required
def contact_create(request):

    if request.method == "POST":

        form = ContactForm(request.POST)

        if form.is_valid():

            contact = form.save()

            # Activity Log
            create_activity(
                user=request.user,
                module="Contact",
                action="CREATE",
                object_name=f"{contact.first_name} {contact.last_name}",
                description=f"Created contact '{contact.first_name} {contact.last_name}'"
            )

            # Notification
            if contact.assigned_to:
                create_notification(
                    user=contact.assigned_to,
                    title="New Contact Assigned",
                    message=(
                        f"{contact.first_name} "
                        f"{contact.last_name} has been assigned to you."
                    )
                )

            messages.success(
                request,
                "Contact added successfully!"
            )

            return redirect("contact_list")

    else:
        form = ContactForm()

    return render(
        request,
        "contacts/contact_form.html",
        {
            "form": form
        }
    )


@login_required
@manager_required
def contact_update(request, pk):

    contact = get_object_or_404(Contact, pk=pk)

    if request.method == "POST":

        form = ContactForm(
            request.POST,
            instance=contact
        )

        if form.is_valid():

            contact = form.save()

            # Activity Log
            create_activity(
                user=request.user,
                module="Contact",
                action="UPDATE",
                object_name=f"{contact.first_name} {contact.last_name}",
                description=f"Updated contact '{contact.first_name} {contact.last_name}'"
            )

            # Notification
            if contact.assigned_to:
                create_notification(
                    user=contact.assigned_to,
                    title="Contact Updated",
                    message=(
                        f"{contact.first_name} "
                        f"{contact.last_name} was updated."
                    )
                )

            messages.success(
                request,
                "Contact updated successfully!"
            )

            return redirect("contact_list")

    else:
        form = ContactForm(instance=contact)

    return render(
        request,
        "contacts/contact_form.html",
        {
            "form": form
        }
    )


@login_required
@admin_required
def contact_delete(request, pk):

    contact = get_object_or_404(Contact, pk=pk)

    if request.method == "POST":

        # Activity Log
        create_activity(
            user=request.user,
            module="Contact",
            action="DELETE",
            object_name=f"{contact.first_name} {contact.last_name}",
            description=f"Deleted contact '{contact.first_name} {contact.last_name}'"
        )

        # Notification
        if contact.assigned_to:
            create_notification(
                user=contact.assigned_to,
                title="Contact Deleted",
                message=(
                    f"{contact.first_name} "
                    f"{contact.last_name} has been removed."
                )
            )

        contact.delete()

        messages.success(
            request,
            "Contact deleted successfully!"
        )

        return redirect("contact_list")

    return render(
        request,
        "contacts/contact_confirm_delete.html",
        {
            "contact": contact
        }
    )


@login_required
def export_contacts_excel(request):

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Contacts"

    headers = [
        "ID",
        "First Name",
        "Last Name",
        "Email",
        "Phone",
        "Company",
        "Job Title",
        "Status",
        "Assigned To",
        "Created Date",
    ]

    ws.append(headers)

    if request.user.groups.filter(name="Sales Rep").exists():
        contacts = Contact.objects.filter(
            assigned_to=request.user
        )
    else:
        contacts = Contact.objects.all()

    for contact in contacts:

        ws.append([
            contact.id,
            contact.first_name,
            contact.last_name,
            contact.email,
            contact.phone,
            str(contact.company),
            contact.job_title,
            contact.status,
            contact.assigned_to.username if contact.assigned_to else "",
            contact.created_at.strftime("%Y-%m-%d"),
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response[
        "Content-Disposition"
    ] = 'attachment; filename="contacts.xlsx"'

    wb.save(response)

    return response