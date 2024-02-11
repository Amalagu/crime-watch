from django.urls import path
from .views import login_view, logout_view
from investigator.views import (
    dashboard, 
    home_view, 
    report_view, 
    view_report_details, 
    create_case_view, 
    case_list_view,
    dismiss_report_view,
    view_case_details
    )

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/',  dashboard, name='dashboard'),
    path('report/<int:pk>', view_report_details, name='view_report_details'),
    path('report/',  report_view, name='report'),
    path('report/dismiss/<int:pk>/', dismiss_report_view, name='dismiss_report_view'),

    path('case/', case_list_view, name='case_list_view'),
    path('case/<int:pk>/', create_case_view, name='create_case_view'),
    path('case/details/<int:pk>', view_case_details, name='view_case_details'),
    path('',  home_view, name='home')
]