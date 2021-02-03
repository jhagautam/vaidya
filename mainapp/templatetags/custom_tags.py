from django import template
register = template.Library()
from datetime import date
from mainapp.models import *
from django.db.models import Count, Sum , Avg, Max, Min
from django.http import HttpResponse
from django.template.defaulttags import register
import dateutil
from dateutil import parser
import datetime
from django.utils import timezone

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_date(x, key):
    return x+datetime.timedelta(days=key)

@register.filter
def check_slot(q,t):
	p=q.filter(time=t)
	if not p:
		return False
	else:
		return True

@register.filter
def compare(today, aptdate):
	if today >= aptdate:
		return False
	else:
		return True
@register.filter
def doctor_name(dictionary, did):
	q=dictionary.values('name').get(id=did)
	return q.get('name')


