from .models import fees,studentsdetail,teachpaymonths,teacherdetail,marks
from .serializers import studentsresultSerializer
from rest_framework.generics import ListAPIView
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.db.models import Avg, Max, Min,Sum,Count


@api_view(['GET'])
def allmoneyfromstudents(request,year):
    if request.method == 'GET':

        t={'janur': None,'febr': None,'marc': None,'apri': None,'ma': None,'jun': None,'jul': None,'augu': None,'sept': None,'octo': None,'nove': None,'dece': None}
        month = ['january','february','march','april','may','june','july','august','september','october','november','december']
        monthscount= ['janurcount','febrcount','marccount','apricount','macount','juncount','julcount','augucount','septcount','octocount','novecount','dececount']
        
        for i in range(0,12):
            month[i] = fees.objects.filter(date_enroll__year=year,date_enroll__month=(i+1)).annotate(t =Sum('studentamount')) 
            
            monthscount[i] = fees.objects.filter(date_enroll__year=year,date_enroll__month=(i+1)).count()
         

        monthsum=[0,0,0,0,0,0,0,0,0,0,0,0]
        
        for x in range(0,12):
            if(monthscount[x]!=0):
                monthscount[x]+1
            for y in range(0,monthscount[x]):
                monthsum[x] += month[x][y].t
                #print('monthsum[x+1]')
        sumserial = {'jansum': monthsum[0], 'febsum': monthsum[1], 'marsum': monthsum[2], 'aprsum': monthsum[3], 'maysum': monthsum[4], 'junsum': monthsum[5], 'julsum': monthsum[6], 'augsum': monthsum[7], 'sepsum': monthsum[8], 'octsum': monthsum[9], 'novsum': monthsum[10], 'decsum': monthsum[11]}
        return JsonResponse(sumserial)



@api_view(['GET'])
def allteacherpayment(request,year):
    if request.method == 'GET':

        t={'janur': None,'febr': None,'marc': None,'apri': None,'ma': None,'jun': None,'jul': None,'augu': None,'sept': None,'octo': None,'nove': None,'dece': None}
        tmonth = ['january','february','march','april','may','june','july','august','september','october','november','december']
        tmonthscount= ['janurcount','febrcount','marccount','apricount','macount','juncount','julcount','augucount','septcount','octocount','novecount','dececount']
        
        for i in range(0,12):
            tmonth[i] = teachpaymonths.objects.filter(date_payed__year=year,date_payed__month=(i+1)).annotate(t =Sum('teacheramount')) 
            tmonthscount[i] = teachpaymonths.objects.filter(date_payed__year=year,date_payed__month=(i+1)).count()
       
        monthsum=[0,0,0,0,0,0,0,0,0,0,0,0]
       
        for x in range(0,12):
            if(tmonthscount[x]!=0):
                tmonthscount[x]+1
            for y in range(0,tmonthscount[x]):
                monthsum[x] += tmonth[x][y].t
            
        sumserial = {'jansum': monthsum[0], 'febsum': monthsum[1], 'marsum': monthsum[2], 'aprsum': monthsum[3], 'maysum': monthsum[4], 'junsum': monthsum[5], 'julsum': monthsum[6], 'augsum': monthsum[7], 'sepsum': monthsum[8], 'octsum': monthsum[9], 'novsum': monthsum[10], 'decsum': monthsum[11]}
        return JsonResponse(sumserial)

@api_view(['GET'])
def countfunction(request):
    if request.method == 'GET':
        studentscount = studentsdetail.objects.all().count()
        teachercount = teacherdetail.objects.all().count()
        sumserial = {'studentcount': studentscount, 'teachercount': teachercount,}
        return JsonResponse(sumserial)

@api_view(['GET'])
def calcsubject(request,subjectt,roll):
    if request.method == 'GET':
        studentmarks = marks.objects.filter(enrollstudent__student__rollnbr=roll,subjectname__subjectname=subjectt)
        subjectmarks_serialized = studentsresultSerializer(studentmarks,many=True)
        return JsonResponse(subjectmarks_serialized.data,safe=False)

@api_view(['GET'])
def nofsubjects(request,subjectt,roll):
    if request.method == 'GET':
        nosubjects = marks.objects.filter(enrollstudent__student__rollnbr=roll,subjectname__subjectname=subjectt).count()
        return JsonResponse({'nosubjects': nosubjects})

