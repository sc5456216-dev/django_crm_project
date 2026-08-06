from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Deal
from .forms import DealForm
from accounts.decorators import admin_required, manager_required


@login_required
def deal_list(request):
    if request.user.groups.filter(name='Sales Rep').exists():
        deals = Deal.objects.filter(assigned_to=request.user)
    else:
        deals = Deal.objects.all()

    stage = request.GET.get('stage')
    if stage:
        deals = deals.filter(stage=stage)

    return render(request, 'deals/deal_list.html', {
        'deals': deals,
        'total': deals.count(),
        'is_admin': request.user.groups.filter(name='Admin').exists(),
        'is_manager': request.user.groups.filter(name__in=['Admin', 'Sales Manager']).exists(),
    })


@login_required
def deal_detail(request, pk):
    deal = get_object_or_404(Deal, pk=pk)

    if request.user.groups.filter(name='Sales Rep').exists():
        if deal.assigned_to != request.user:
            raise PermissionDenied("You can only view your assigned deals.")

    return render(request, 'deals/deal_detail.html', {'deal': deal})


@login_required
@manager_required
def deal_create(request):
    if request.method == 'POST':
        form = DealForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Deal created successfully!')
            return redirect('deal_list')
    else:
        form = DealForm()
    return render(request, 'deals/deal_form.html', {'form': form})


@login_required
@manager_required
def deal_update(request, pk):
    deal = get_object_or_404(Deal, pk=pk)
    if request.method == 'POST':
        form = DealForm(request.POST, instance=deal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Deal updated successfully!')
            return redirect('deal_list')
    else:
        form = DealForm(instance=deal)
    return render(request, 'deals/deal_form.html', {'form': form})


@login_required
@admin_required
def deal_delete(request, pk):
    deal = get_object_or_404(Deal, pk=pk)
    if request.method == 'POST':
        deal.delete()
        messages.success(request, 'Deal deleted successfully!')
        return redirect('deal_list')
    return render(request, 'deals/deal_confirm_delete.html', {'deal': deal})


@login_required
def deal_pipeline(request):
    if request.user.groups.filter(name='Sales Rep').exists():
        base_deals = Deal.objects.filter(assigned_to=request.user)
    else:
        base_deals = Deal.objects.all()

    pipeline_stages = [
        {'key': 'lead', 'label': 'Lead', 'color': 'secondary', 'deals': base_deals.filter(stage='lead')},
        {'key': 'qualified', 'label': 'Qualified', 'color': 'info', 'deals': base_deals.filter(stage='qualified')},
        {'key': 'proposal', 'label': 'Proposal', 'color': 'primary', 'deals': base_deals.filter(stage='proposal')},
        {'key': 'negotiation', 'label': 'Negotiation', 'color': 'warning', 'deals': base_deals.filter(stage='negotiation')},
        {'key': 'won', 'label': 'Won', 'color': 'success', 'deals': base_deals.filter(stage='won')},
        {'key': 'lost', 'label': 'Lost', 'color': 'danger', 'deals': base_deals.filter(stage='lost')},
    ]

    return render(request, 'deals/deal_pipeline.html', {
        'pipeline_stages': pipeline_stages,
        'is_manager': request.user.groups.filter(name__in=['Admin', 'Sales Manager']).exists(),
    })


@login_required
def deal_change_stage(request, pk):
    deal = get_object_or_404(Deal, pk=pk)

    if request.user.groups.filter(name='Sales Rep').exists():
        if deal.assigned_to != request.user:
            raise PermissionDenied("You can only change your own deals.")

    if request.method == 'POST':
        new_stage = request.POST.get('stage')
        if new_stage in dict(Deal.STAGE_CHOICES):
            deal.stage = new_stage
            deal.save()
            messages.success(request, f'Deal moved to {new_stage}!')
    return redirect('deal_pipeline')