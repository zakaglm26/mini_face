from django.contrib import admin

# Register your models here.
from django.contrib import admin
from ump_app.models import Faculty,Student,Cursus,Job,Employee,Campus, Message
admin.site.register(Faculty)
admin.site.register(Student)
admin.site.register(Cursus)
admin.site.register(Job)
admin.site.register(Employee)
admin.site.register(Campus)
admin.site.register(Message)
