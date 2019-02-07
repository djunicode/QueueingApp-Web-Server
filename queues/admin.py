from django.contrib import admin
from .models import Location, Student, Queue, Teacher, Token


admin.site.register(Location)
admin.site.register(Student)
admin.site.register(Queue)
admin.site.register(Teacher)
admin.site.register(Token)
