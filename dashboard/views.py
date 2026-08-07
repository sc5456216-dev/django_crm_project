from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from contacts.models import Contact
from deals.models import Deal
from tasks.models import Task
from activities.models import ActivityLog
from notes.models import Note
from notes.forms import NoteForm
from portfolio.models import Project   


@login_required
def dashboard(request):

    # Count stats
    total_contacts = Contact.objects.count()
    total_deals = Deal.objects.count()
    won_deals = Deal.objects.filter(stage='won').count()
    lost_deals = Deal.objects.filter(stage='lost').count()
    pending_tasks = Task.objects.filter(assigned_to=request.user, status='pending').count()

    # Total revenue
    total_revenue = Deal.objects.filter(stage='won').aggregate(total=Sum('value'))['total'] or 0

    # Recent contacts
    recent_contacts = Contact.objects.order_by('-created_at')[:5]

    # Recent notes
    recent_notes = Note.objects.order_by('-created_at')[:5]

    # Total notes
    total_notes = Note.objects.count()

    # Recent projects 
    recent_projects = Project.objects.order_by('-created_at')[:5]

    # Deals by stage
    deals_by_stage = {
        'Lead': Deal.objects.filter(stage='lead').count(),
        'Qualified': Deal.objects.filter(stage='qualified').count(),
        'Proposal': Deal.objects.filter(stage='proposal').count(),
        'Negotiation': Deal.objects.filter(stage='negotiation').count(),
        'Won': Deal.objects.filter(stage='won').count(),
        'Lost': Deal.objects.filter(stage='lost').count(),
    }

    # Monthly revenue
    monthly_revenue = list(
        Deal.objects.filter(stage='won')
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum('value'))
        .order_by('month')[:6]
    )

    # Contact status
    contact_status = {
        'Lead': Contact.objects.filter(status='lead').count(),
        'Customer': Contact.objects.filter(status='customer').count(),
        'Partner': Contact.objects.filter(status='partner').count(),
    }

    # Recent Activity Log
    if request.user.groups.filter(name='Sales Rep').exists():
        recent_activities = ActivityLog.objects.filter(user=request.user).order_by('-created_at')[:10]
    else:
        recent_activities = ActivityLog.objects.select_related('user').order_by('-created_at')[:10]

    # Instantiate the note form
    form = NoteForm()

    context = {
        'total_contacts': total_contacts,
        'total_deals': total_deals,
        'won_deals': won_deals,
        'lost_deals': lost_deals,
        'pending_tasks': pending_tasks,
        'total_revenue': total_revenue,
        'recent_contacts': recent_contacts,
        'recent_notes': recent_notes,
        'total_notes': total_notes,
        'recent_projects': recent_projects,   
        'deals_by_stage': deals_by_stage,
        'monthly_revenue': monthly_revenue,
        'contact_status': contact_status,
        'recent_activities': recent_activities,
        'form': form,
    }

    return render(request, 'dashboard/dashboard.html', context)