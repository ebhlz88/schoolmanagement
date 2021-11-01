from django.db import models
from django.db.models.fields.related import ForeignKey

# Create your models here.
class studentsdetail(models.Model):
    rollnbr = models.BigAutoField(primary_key=True)
    student_pic = models.ImageField(upload_to='studentpic',blank=True)
    s_name = models.CharField(max_length=50)
    s_fname = models.CharField(max_length=50)
    dob = models.DateField()
    date_join = models.DateField()
    c_position = models.BooleanField(default=True)
    sex = models.CharField(max_length=7)
    address = models.CharField(max_length=200)
    fm_number = models.CharField(max_length=15)
    bloodgroup = models.CharField(max_length=4)

    def __str__(self):
        return self.s_name



class schoolclasses(models.Model):
    standardname = models.CharField(max_length=100)
    date_started = models.DateField(default=0,null=True)
    date_ended = models.DateField(default=0,null=True)
    def __str__(self):
        return self.standardname

class enroll_student(models.Model):
    standard = models.ForeignKey(schoolclasses,on_delete=models.CASCADE)
    student = models.ForeignKey(studentsdetail,on_delete=models.CASCADE)
    
    

class fees(models.Model):
    enrollstudent = models.ForeignKey(enroll_student,on_delete=models.CASCADE)
    studentamount = models.IntegerField(default=0,null=True)
    date_enroll = models.DateField(auto_now_add=True)

class subjects(models.Model):
    subjectname = models.CharField(max_length=100)
    def __str__(self):
        return self.subjectname


class marks(models.Model):
    subjectname = models.ForeignKey(subjects,on_delete=models.DO_NOTHING)
    enrollstudent = models.ForeignKey(enroll_student,on_delete=models.CASCADE)
    subjectmarks = models.PositiveSmallIntegerField(default=0,null=True)
    
    
class teacherdetail(models.Model):
    t_name = models.CharField(max_length=50)
    t_fname = models.CharField(max_length=50)
    teacher_pic = models.ImageField(upload_to='teacherpic',blank=True)
    dob = models.DateField()
    m_number = models.CharField(max_length=20)
    t_email = models.CharField(max_length=50)
    date_hiring = models.DateField()
    c_position = models.BooleanField(default=True)
    sex = models.CharField(max_length=7)
    address = models.CharField(max_length=200)
    salary = models.IntegerField()
    speciality = models.CharField(max_length=200)
    bloodgroup = models.CharField(max_length=4)

    def __str__(self):
        return str(self.t_name)

class teachpaymonths(models.Model):
    teacher = models.ForeignKey(teacherdetail,on_delete=models.CASCADE)
    teacheramount = models.IntegerField(default=0,null=True)
    date_payed = models.DateField(auto_now_add=True)

class books(models.Model):
    bookthumbnail = models.ImageField(upload_to='books',blank=True)
    bookname =  models.CharField(max_length=200)
    book = models.FileField(upload_to='books')
    standard = models.ForeignKey(schoolclasses,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.bookname)




   
