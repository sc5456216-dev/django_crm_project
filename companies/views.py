from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from .models import Company
from .forms import CompanyForm

from accounts.decorators import admin_required, manager_required
from activities.utils import create_activity
from notifications.utils import create_notification


@login_required
def company_list(request):

    # Sales Rep can only view assigned companies
    if request.user.groups.filter(name="Sales Rep").exists():
        companies = Company.objects.filter(
            assigned_to=request.user
        )
    else:
        companies = Company.objects.all()

    search = request.GET.get("search")

    if search:
        companies = companies.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search) |
            Q(address__icontains=search)
        )

    context = {
        "companies": companies,
        "total": companies.count(),
        "is_admin": request.user.groups.filter(
            name="Admin"
        ).exists(),
        "is_manager": request.user.groups.filter(
            name__in=["Admin", "Sales Manager"]
        ).exists(),
    }

    return render(
        request,
        "companies/company_list.html",
        context,
    )


@login_required
def company_detail(request, pk):

    company = get_object_or_404(
        Company,
        pk=pk
    )

    if request.user.groups.filter(name="Sales Rep").exists():
        if company.assigned_to != request.user:
            raise PermissionDenied(
                "You can only view your assigned companies."
            )

    return render(
        request,
        "companies/company_detail.html",
        {
            "company": company,
        },
    )


@login_required
@manager_required
def company_create(request):

    if request.method == "POST":

        form = CompanyForm(request.POST)

        if form.is_valid():

            company = form.save()

            # Activity Log
            create_activity(
                user=request.user,
                module="Company",
                action="CREATE",
                object_name=company.name,
                description=f"Created company '{company.name}'",
            )

            # Notification
            if company.assigned_to:
                create_notification(
                    user=company.assigned_to,
                    title="New Company Assigned",
                    message=(
                        f"Company '{company.name}' "
                        "has been assigned to you."
                    ),
                )

            messages.success(
                request,
                "Company added successfully!"
            )

            return redirect("company_list")

    else:
        form = CompanyForm()

    return render(
        request,
        "companies/company_form.html",
        {
            "form": form,
        },
    )


@login_required
@manager_required
def company_update(request, pk):

    company = get_object_or_404(
        Company,
        pk=pk
    )

    old_assigned_to = company.assigned_to

    if request.method == "POST":

        form = CompanyForm(
            request.POST,
            instance=company,
        )

        if form.is_valid():

            company = form.save()

            # Activity Log
            create_activity(
                user=request.user,
                module="Company",
                action="UPDATE",
                object_name=company.name,
                description=f"Updated company '{company.name}'",
            )

            # Notify assigned user
            if company.assigned_to:
                create_notification(
                    user=company.assigned_to,
                    title="Company Updated",
                    message=(
                        f"Company '{company.name}' "
                        "has been updated."
                    ),
                )

            # Notify if assignment changed
            if (
                old_assigned_to != company.assigned_to
                and company.assigned_to
            ):
                create_notification(
                    user=company.assigned_to,
                    title="Company Assigned",
                    message=(
                        f"You have been assigned "
                        f"company '{company.name}'."
                    ),
                )

            messages.success(
                request,
                "Company updated successfully!"
            )

            return redirect("company_list")

    else:
        form = CompanyForm(instance=company)

    return render(
        request,
        "companies/company_form.html",
        {
            "form": form,
        },
    )


@login_required
@admin_required
def company_delete(request, pk):

    company = get_object_or_404(
        Company,
        pk=pk
    )

    if request.method == "POST":

        # Activity Log
        create_activity(
            user=request.user,
            module="Company",
            action="DELETE",
            object_name=company.name,
            description=f"Deleted company '{company.name}'",
        )

        # Notification
        if company.assigned_to:
            create_notification(
                user=company.assigned_to,
                title="Company Deleted",
                message=(
                    f"Company '{company.name}' "
                    "has been deleted."
                ),
            )

        company.delete()

        messages.success(
            request,
            "Company deleted successfully!"
        )

        return redirect("company_list")

    return render(
        request,
        "companies/company_confirm_delete.html",
        {
            "company": company,
        },
    )