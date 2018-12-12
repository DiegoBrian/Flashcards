from django.contrib import admin

from .models import *

admin.site.register(Sentence)
admin.site.register(User_Sentence)
admin.site.register(User_TimeSettings)