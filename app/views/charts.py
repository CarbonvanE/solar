""" Handles all chart related views """

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def chart_day_view(request):
    """ Returns the chart of the last 24 hours """
    context = {
        'tab': 'chart_day'
    }
    return render(request, 'app/chart.html', context)


@login_required
def chart_week_view(request):
    """ Returns the chart of the last 7 days """
    context = {
        'tab': 'chart_week'
    }
    return render(request, 'app/chart.html', context)


@login_required
def chart_year_view(request):
    """ Returns the chart of the last 365 days """
    context = {
        'tab': 'chart_year'
    }
    return render(request, 'app/chart.html', context)
