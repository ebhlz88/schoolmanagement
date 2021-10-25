from rest_framework import serializers
from django.contrib.auth.models import User
from .models import studentsdetail,teacherdetail,teachpaymonths,marks,subjects,schoolclasses,enroll_student,fees,books

class studentsdetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = studentsdetail
        #fields=['s_name',]
        fields = '__all__'


class enrollSerializer(serializers.ModelSerializer):

    class Meta:
        model = enroll_student
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['student'] = studentsdetailSerializer(instance.student).data
        rep['standard'] = standardSerializer(instance.standard).data
        return rep

class feesSerializer(serializers.ModelSerializer):

    class Meta:
        model = fees
        fields = '__all__'
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['enrollstudent'] = enrollSerializer(instance.enrollstudent).data
        return rep


class teacherdetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = teacherdetail
        fields = '__all__'

class t_paymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = teachpaymonths
        fields = '__all__'
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['teacher'] = teacherdetailSerializer(instance.teacher).data
        return rep

class studentsresultSerializer(serializers.ModelSerializer):

    class Meta: 
        model = marks
        fields = '__all__'
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['enrollstudent'] = enrollSerializer(instance.enrollstudent).data
        rep['subjectname'] = subjectsSerializer(instance.subjectname).data
        return rep
    

class subjectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = subjects
        fields = '__all__'

class standardSerializer(serializers.ModelSerializer):
    class Meta:
        model = schoolclasses
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user

class BooksSerializer(serializers.ModelSerializer):

    class Meta:
        model = books
        fields = '__all__'
