from django.contrib import admin

from riddles.models import *

admin.site.register(RiddleType)
admin.site.register(Riddle)
admin.site.register(RiddleState)
