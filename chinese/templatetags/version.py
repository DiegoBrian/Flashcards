from django import template

register = template.Library()

times = ["5s","25s","2m","10m","1h","5h","1d","5d","25d","4m","2y"]

@register.filter()
def to_int(value):
    value = value[:-1]
    return int(value)


@register.filter()
def time(current_box):
	if current_box > 10:
		return times[10]
	elif current_box <0:
		return times[0]
	else:
		return times[current_box]


@register.filter()
def filter_chinese(sentence):
	return sentence.replace('==', ' ')

