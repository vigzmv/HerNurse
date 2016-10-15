from django.contrib import admin

from .models import *

admin.site.register(ModelUser)
admin.site.register(ModelDiscuss)
admin.site.register(ModelTag)
admin.site.register(ModelQuestion)
admin.site.register(ModelAnswer)
