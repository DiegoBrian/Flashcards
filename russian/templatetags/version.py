from django import template
from language.views_common import str_time, get_time_step, set_time_step
from language.views import revert_delta

register = template.Library()

#times = ["5s","25s","2m","10m","1h","5h","1d","5d","25d","4m","2y"]

@register.filter()
def to_int(value):
    value = value[:-1]
    return int(value)


@register.filter()
def time(current_box, user):
	if current_box > 10:
		pos = 10
	elif current_box <0:
		pos = 0
	else:
		pos = current_box
	
	time_step = revert_delta(user)

	return time_step[pos]

