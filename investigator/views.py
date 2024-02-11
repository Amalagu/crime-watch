from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import ReportForm, CaseForm
from .models import Report, Evidence, Timeline
from .models import Case as CaseModel
from accounts.models import Investigator
from django import forms
from django.db.models import Case, When, Value, IntegerField, Q
from .decorators import investigator_case_required






################
#   REPORT RELATED VIEWS
###############



def report_view(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your complaint has been logged and will be looked into!')
            return render(request, 'complaint-form.html', {'form': ReportForm()})
        else:
            messages.error(request, 'Failed to log your complaint. Please check the form.')
    else:
        form = ReportForm()
    return render(request, 'complaint-form.html', {'form': form})



@login_required
def view_report_details(request, pk):
    report = Report.objects.get(id=pk)
    context = {
        'report': report
    }
    return render(request, 'investigator-report-details.html', context)

@login_required
def dashboard(request):
    # Get the investigator associated with the current user
    agency = Investigator.objects.get(user=request.user)
    all_reports = Report.objects.filter(category__in=agency.specializations.all().values_list('name'))
    reports_exclude_active = all_reports.exclude(status='ACTIVE')
    if request.method == 'GET':
        # Get the selected status from the search form
        status_to_show = request.GET.get('reportsToShow', 'ALL')
        # Filter reports based on the selected status
        if status_to_show == 'ACTIVE':
            filtered_reports = all_reports.filter(status='ACTIVE').order_by('-timestamp')
        elif status_to_show == 'DISMISSED':
            filtered_reports = all_reports.filter(status='DISMISSED').order_by('-timestamp')
        elif status_to_show == 'VALID':
            filtered_reports = all_reports.filter(status='VALID').order_by('-timestamp')
        else:
            # Custom ordering: valid first, active second, dismissed last
            filtered_reports = all_reports.annotate(
                order=Case(
                    When(status='VALID', then=Value(1)),
                    When(status='ACTIVE', then=Value(2)),
                    When(status='DISMISSED', then=Value(3)),
                    default=Value(4),  # Fallback for other statuses
                    output_field=IntegerField()
                )
            ).order_by('order', '-timestamp')
            
        context = {
        'filtered_reports': filtered_reports,
        'agency': agency,
        'status_to_show': status_to_show,
    }
        return render(request, 'investigator-dashboard.html', context)
        


################
#   CASE RELATED VIEWS
###############

@login_required
def case_list_view(request):
    investigator = Investigator.objects.get(user=request.user)

    cases = CaseModel.objects.filter(investigator= investigator).annotate(
    order=Case(
        # First, cases that are not yet dismissed and not yet resolved
        When(Q(isdismissed=False) & Q(isresolved=False), then=Value(1)),
        # Second, cases that are resolved but not dismissed
        When(Q(isdismissed=False) & Q(isresolved=True), then=Value(2)),
        # Third, cases that are not resolved but are dismissed
        When(Q(isdismissed=True) & Q(isresolved=False), then=Value(3)),
        # Fourth, cases that are dismissed and resolved
        When(Q(isdismissed=True) & Q(isresolved=True), then=Value(4)),
        default=Value(5),  # Fallback for other cases
        output_field=IntegerField()
    )
).order_by('order')

    #cases = CaseModel.objects.filter(investigator= investigator).order_by('-time_opened')
    context = {
        'cases':cases,
        'agency': investigator
    }
    return render(request, 'investigator-cases.html', context)


@login_required
def create_case_view(request, pk):
    report = Report.objects.get(id=pk)
    invesigator = Investigator.objects.get(user=request.user)
    if request.method == 'POST':
        case_data={}
        case_data['authorization_letter'] = request.POST['authorization_letter']
        case_data['report'] = report
        case_data['investigator'] = invesigator
        form = CaseForm(case_data, request.FILES)
        if form.is_valid():
            case = form.save(commit=False)
            case.report = report  
            case.save()
            report.approved = True
            report.status = 'ACTIVE'
            report.save()
            return redirect('case_list_view')  
    else:
        print('BAD FORM INPUT')
        # Pre-populate the form with initial data (report)
        form = CaseForm(initial={'report': report})
    context = {
        'form': form,
        'report': report,
        'agency': invesigator
               }
    return render(request, 'case-creation-form.html', context)



@login_required
@investigator_case_required
def view_case_details(request, pk):
    case = CaseModel.objects.get(id=pk)
    timelines = case.timeline_set.all()
    invesigator = Investigator.objects.get(user=request.user)
    if request.method == 'POST':
        action = request.POST['action']
        if action == 'Dismiss':
            case.isdismissed = True
            case.save()
            return redirect('case_list_view')
        elif action == 'Reopen':
            case.isresolved = False
            case.save()
            return redirect('case_list_view')
        elif action == 'Reverse':
            case.isdismissed = False
            case.save()
            return redirect('case_list_view')
        elif action == 'Resolve':
            case.isresolved = True
            case.save()
            return redirect('case_list_view')
        elif action == 'AddTimeline':
            description = request.POST['description']
            timeline = Timeline(description=description, case=case )
            timeline.save()
    
            return redirect('view_case_details', pk=case.id)
    context = {
        'case': case,
        'timelines':timelines,
        'agency':invesigator
    }
    return render(request, 'investigator-case-details.html', context)



@login_required
def dismiss_report_view(request, pk):
    report = Report.objects.get(pk=pk)
    report.status = 'DISMISSED'
    report.save() 
    return redirect('dashboard')




    context = {
        'filtered_reports': filtered_reports,
        'agency': agency,
        'status_to_show': status_to_show,
    }
    return render(request, 'investigator-dashboard.html', context)




""" @login_required
def dashboard(request):
    if request.method == 'GET':
        #NB: the request.GET returns <QueryDict: {'reportsToShow': ['ACTIVE']}>
    agency = Investigator.objects.get(user=request.user)
    all_reports = Report.objects.filter(category__in=agency.specializations.all().values_list('name'))
    valid_reports = all_reports.filter(status='VALID').order_by('-timestamp')
    dismissed_reports = all_reports.filter(status='DISMISSED').order_by('-timestamp')
    active_reports = all_reports.filter(status='ACTIVE').order_by('-timestamp')
    context = {
        'valid_reports':valid_reports,
        'agency': agency,
        'active_reports':active_reports,
        'dismissed_reports':dismissed_reports
    }
    return render(request, 'investigator-dashboard.html', context) """











def home_view(request):
    return render(request, 'index.html')