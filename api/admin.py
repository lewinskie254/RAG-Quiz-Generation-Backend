from django.contrib import admin
from .models import * 
# Register your models here.
admin.site.register(School)
admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Unit)
admin.site.register(StudentUnitScore)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)