from functools import partial
import json
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from .models import studentsdetail,fees,enroll_student,schoolclasses,marks,subjects,books
from .serializers import studentsdetailSerializer,feesSerializer,studentsresultSerializer,standardSerializer,subjectsSerializer,BooksSerializer,ResultlistSerializer,enrollSerializer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework import generics
# from rest_framework.filters import SearchFilter
from rest_framework.filters import SearchFilter
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser,FormParser,MultiPartParser




class studentslist(APIView):
    def get(self,request,format=None):
        allstudents = studentsdetail.objects.all()
        
        
        allstudents_serializer = studentsdetailSerializer(allstudents, many=True)
        return Response(allstudents_serializer.data)
        # 'safe=False' for objects serialization

    parser_classes = [FormParser,MultiPartParser]
    def post(self, request, format=None):
        allstudents_serializer = studentsdetailSerializer(data=request.data)
        if allstudents_serializer.is_valid():
            allstudents_serializer.save()
            return Response(allstudents_serializer.data, status=status.HTTP_201_CREATED)
        return Response(allstudents_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, format=None):   
        
        studentsdetail.objects.all().delete()  
        return Response({'message':'all students data deleted'},status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST','DELETE'])    
def studentByroll(request, roll) :    
        try:
            student=studentsdetail.objects.filter(rollnbr=roll)
            if request.method == 'DELETE':
                student.delete()
                return JsonResponse({'message':'this row is deleted successfully'},status=status.HTTP_204_NO_CONTENT)
            elif request.method == 'GET':
                student=studentsdetail.objects.get(rollnbr=roll)
                student_serializer=studentsdetailSerializer(student)
            return JsonResponse(student_serializer.data)
        except studentsdetail.DoesNotExist: 
            return JsonResponse({'message': 'The Student does not exist'}, status=status.HTTP_404_NOT_FOUND)
     


@api_view(['GET'])
def standardlist(request):
    if request.method == 'GET':
        standard = schoolclasses.objects.all()
        years_serializer = standardSerializer(standard, many=True)
        return JsonResponse(years_serializer.data, safe=False)
    

@api_view(['GET'])
def subjectlist(request):
    if request.method == 'GET':
        standard = subjects.objects.all()
        years_serializer = subjectsSerializer(standard, many=True)
        return JsonResponse(years_serializer.data, safe=False)

@api_view(['GET', 'POST', 'DELETE'])
def feesget(request):
    if request.method == 'GET':
        allfees = fees.objects.all()
        allfees_serialized = feesSerializer(allfees, many=True)
        return JsonResponse(allfees_serialized.data, safe=False)

@api_view(['GET'])
def feesgetByroll(request,roll):
    if request.method == 'GET':
        student_fee = fees.objects.filter(enrollstudent__student__rollnbr=roll)
        fee_serialized = feesSerializer(student_fee, many=True)
        return JsonResponse(fee_serialized.data, safe=False)

@api_view(['POST'])
def feespost(request,roll,standardd):
    if request.method == 'POST':
        data_month = JSONParser().parse(request)
        inststudent = studentsdetail.objects.get(rollnbr=roll)
        insstandard = schoolclasses.objects.get(standardname=standardd)
        #try:
        try:
            insenroll = enroll_student.objects.get(student__rollnbr=roll,standard__standardname=standardd)
        except enroll_student.DoesNotExist:
            insenroll = enroll_student(student=inststudent,standard=insstandard)
            insenroll.save()
            
        insfees = fees(enrollstudent=insenroll)
        fees_serialized = feesSerializer(insfees,data=data_month, partial=True)
        if fees_serialized.is_valid():
            fees_serialized.save()
            return JsonResponse(fees_serialized.data,status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(fees_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getstudentresult(request,sroll,standardd):
    if request.method == 'GET':
        student = marks.objects.filter(enrollstudent__student__rollnbr=sroll,enrollstudent__standard__standardname=standardd)
        # print(student.standard)
        studentresultSerializer = studentsresultSerializer(student,many = True)
        return JsonResponse(studentresultSerializer.data,safe= False)

@api_view(['POST'])
def postresult(request,roll,ssubject,standardd):
    if request.method == 'POST':
        result_data = JSONParser().parse(request)
        inssubject = subjects.objects.get(subjectname=ssubject)
        inststudent = studentsdetail.objects.get(rollnbr=roll)
        insstandard = schoolclasses.objects.get(classid=standardd)
        try:
            #check if student is enrolled if not it is automatically enrolled
            try:
                insenroll = enroll_student.objects.get(student=roll,standard__classid=standardd)
            except enroll_student.DoesNotExist:
                insenroll = enroll_student(student=inststudent,standard=insstandard)
                insenroll.save()

            markstest = marks.objects.get(enrollstudent__student__rollnbr=roll,subjectname__subjectname=ssubject,enrollstudent__standard__classid=standardd)
            studentresultSerializer = studentsresultSerializer(markstest,data=result_data,partial=True)
            if studentresultSerializer.is_valid():
                studentresultSerializer.save()
                return JsonResponse(studentresultSerializer.data,status=status.HTTP_201_CREATED)
            else:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST)
        except marks.DoesNotExist:
            insmarks = marks(enrollstudent=insenroll,subjectname=inssubject)
            insmarks.save()
            studentresultSerializer = studentsresultSerializer(insmarks,data=result_data,partial=True)
            if studentresultSerializer.is_valid():
                studentresultSerializer.save()
                return JsonResponse(studentresultSerializer.data,status=status.HTTP_201_CREATED)
            else:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST)

class studentsearch(ListAPIView):
        queryset=studentsdetail.objects.all()
        serializer_class=studentsdetailSerializer
        filter_backends=[SearchFilter]
        search_fields=['s_name','s_fname','sex','c_position','rollnbr']

class searchresult(ListAPIView):
        queryset=marks.objects.all()
        serializer_class=studentsresultSerializer
        filter_backends=[SearchFilter]
        search_fields=['subjectname__subjectname','enrollstudent__student__s_name','enrollstudent__student__rollnbr']

class allbooks(APIView):
    def get(self,*args, **kwargs):
        allbooks = books.objects.filter(standard__standardname=kwargs.get('stsandardd', 'ninth'))
        bookSerialized = BooksSerializer(allbooks, many=True)
        return Response(bookSerialized.data)

    parser_classes = [FormParser,MultiPartParser]
    def post(self, request, format=None):
        bookSerialized = BooksSerializer(data= request.data)
        if bookSerialized.is_valid():
            bookSerialized.save()
            return Response(bookSerialized.data, status=status.HTTP_201_CREATED)
        return Response(bookSerialized.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getresultBystandard(request,standardd,ssubject):
    if request.method == 'GET':
        student = marks.objects.filter(enrollstudent__standard__pk=standardd,subjectname__subjectname=ssubject)
        # print(student.standard)
        studentresultSerializer = studentsresultSerializer(student,many = True)
        return JsonResponse(studentresultSerializer.data,safe= False)


@api_view(['GET'])
def getenrollments(request,roll):
    if request.method == 'GET':
        enrollments = enroll_student.objects.filter(student__rollnbr=21).order_by('-date_enrollinstandard')
        enrollments_Serialized = enrollSerializer(enrollments, many= True)
        return JsonResponse(enrollments_Serialized.data,safe=False)

@api_view(['GET'])
def getstudentresultbystandard(request,standardd):
    if request.method == 'GET':
        markdata = marks.objects.filter(enrollstudent__standard__classid=standardd)
        
        studentresultSerializer = studentsresultSerializer(markdata,many = True)
        return JsonResponse(studentresultSerializer.data,safe= False)
from django.core import serializers
@api_view(['GET'])
def updateStandardInStudent(request,roll):
    if request.method == 'GET':
        getstudent = studentsdetail.objects.filter(rollnbr=roll).values("currentStandard")
        queryset = studentsdetail.objects.get(rollnbr=roll)
        #studentserialized = studentsdetailSerializer(getstudent)
        for dd in getstudent:
            currentStan = { "currentStandard": dd['currentStandard']+1 }
        print(currentStan)
        serialized = studentsdetailSerializer(queryset,data=currentStan,partial=True)
        if serialized.is_valid():
            serialized.save()
            return JsonResponse(serialized.data,status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
