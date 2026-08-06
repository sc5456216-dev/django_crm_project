from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from contacts.models import Contact
from deals.models import Deal
from tasks.models import Task

@login_required
def dashboard(request):
    # Count stats
    total_contacts = Contact.objects.count()
    total_deals = Deal.objects.count()
    won_deals = Deal.objects.filter(stage='won').count()
    lost_deals = Deal.objects.filter(stage='lost').count()
    pending_tasks = Task.objects.filter(assigned_to=request.user, status='pending').count()
    
    # Total revenue from won deals
    total_revenue = Deal.objects.filter(stage='won').aggregate(total=Sum('value'))['total'] or 0
    
    # Recent contacts
    recent_contacts = Contact.objects.all().order_by('-created_at')[:5]
    
    # Deals by stage (for chart)
    deals_by_stage = {
        'Lead': Deal.objects.filter(stage='lead').count(),
        'Qualified': Deal.objects.filter(stage='qualified').count(),
        'Proposal': Deal.objects.filter(stage='proposal').count(),
        'Negotiation': Deal.objects.filter(stage='negotiation').count(),
        'Won': Deal.objects.filter(stage='won').count(),
        'Lost': Deal.objects.filter(stage='lost').count(),
    }
    
    # Monthly revenue data (last 6 months) - simplified
    from django.db.models.functions import TruncMonth
    monthly_revenue = list(Deal.objects.filter(stage='won').annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(total=Sum('value')).order_by('month')[:6])
    
    # Contact status distribution
    contact_status = {
        'Lead': Contact.objects.filter(status='lead').count(),
        'Customer': Contact.objects.filter(status='customer').count(),
        'Partner': Contact.objects.filter(status='partner').count(),
    }
    
    context = {
        'total_contacts': total_contacts,
        'total_deals': total_deals,
        'won_deals': won_deals,
        'lost_deals': lost_deals,
        'pending_tasks': pending_tasks,
        'total_revenue': total_revenue,
        'recent_contacts': recent_contacts,
        'deals_by_stage': deals_by_stage,
        'monthly_revenue': monthly_revenue,
        'contact_status': contact_status,
    }
    return render(request, 'dashboard/dashboard.html', context)