""" Handles all chart related views """

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def chart_day_view(request):
    """ Returns the chart of the last 24 hours """
    context = {
        'tab': 'chart_day',

        'chart_url': '/json/power',
        'chart_y_axis_title': 'Power [W]',
        'chart_tooltip_suffix': ' W',
        'chart_raw_data_as_column': False,
        'color_raw_data': 'grey',
        'color_small_avg': 'darkgrey',
        'color_large_avg': 'lightgrey'
    }
    return render(request, 'app/chart.html', context)


@login_required
def chart_month_view(request):
    """ Returns the chart of the last 30 days """
    context = {
        'tab': 'chart_month'
    }
    return render(request, 'app/chart.html', context)


@login_required
def chart_year_view(request):
    """ Returns the chart of the last 365 days """
    context = {
        'tab': 'chart_year',

        'chart_url': '/json/energy',
        'chart_y_axis_title': 'Energy generated per day [kWh]',
        'chart_tooltip_suffix': ' kWh',
        'chart_raw_data_as_column': True,
        'color_raw_data': 'lightgrey',
        'color_small_avg': 'darkgrey',
        'color_large_avg': 'grey'
    }
    return render(request, 'app/chart.html', context)
