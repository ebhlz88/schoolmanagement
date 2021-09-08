from django.contrib import admin

from school.models import studentsdetail,teacherdetail,teachpaymonths,subjects,marks,schoolclasses,enroll_student,fees

# Register your models here.
admin.site.register(studentsdetail)
admin.site.register(teacherdetail)
admin.site.register(teachpaymonths)
admin.site.register(schoolclasses)
admin.site.register(subjects)
admin.site.register(marks)
admin.site.register(enroll_student)
admin.site.register(fees)