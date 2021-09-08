from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from .models import studentsdetail,fees,enroll_student,schoolclasses,marks,subjects
from .serializers import studentsdetailSerializer,feesSerializer,studentsresultSerializer,standardSerializer,subjectsSerializer
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
        # 'safe=False' for objects serialization
 
    # elif request.method == 'POST':
    #     year_data = JSONParser().parse(request)
    #     years_serializer = yearsSerializer(data=year_data)
    #     if years_serializer.is_valid():
    #         years_serializer.save()
    #         return JsonResponse(years_serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return JsonResponse(years_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    # elif request.method == 'DELETE':      
    #             yearclass.objects.all().delete()  
            
    # return JsonResponse({'message':'all years cleared'},status=status.HTTP_204_NO_CONTENT)
    

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
            insenroll = enroll_student.objects.get(student__s_name=roll,standard__standardname=standardd)
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
        insstandard = schoolclasses.objects.get(standardname=standardd)
        try:
            #check if student is enrolled if not it is automatically enrolled
            try:
                insenroll = enroll_student.objects.get(student=roll,standard__standardname=standardd)
            except enroll_student.DoesNotExist:
                insenroll = enroll_student(student=inststudent,standard=insstandard)
                insenroll.save()

            markstest = marks.objects.get(enrollstudent__student__rollnbr=roll,subjectname__subjectname=ssubject,enrollstudent__standard__standardname=standardd)
            
            #get subject object
            # inssubject = subjects.objects.get(subjectname=ssubject)
            # insmarks = marks(enrollstudent=insenroll,subjectname=inssubject)

            
            studentresultSerializer = studentsresultSerializer(markstest,data=result_data,partial=True)
            if studentresultSerializer.is_valid():
                studentresultSerializer.save()
                return JsonResponse(studentresultSerializer.data,status=status.HTTP_201_CREATED)
            else:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST)

            return JsonResponse({'message':'Result already exists do you want to overide'},status=status.HTTP_400_BAD_REQUEST)
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
            


