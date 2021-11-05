from django.http import HttpResponse
from rest_framework import status
from .models import teacherdetail,teachpaymonths
from .serializers import teacherdetailSerializer,t_paymentSerializer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework import generics
from rest_framework.filters import SearchFilter

@api_view(['GET','POST','DELETE'])
def teacheroverall(request):
    if request.method == 'GET':
        allstudents = teacherdetail.objects.all()
        allstudents_serializer = teacherdetailSerializer(allstudents, many=True)
        return JsonResponse(allstudents_serializer.data,safe = False)
    elif request.method == 'POST':
        teacherpostdata = JSONParser().parse(request)
        postserializer = teacherdetailSerializer(data=teacherpostdata)
        if postserializer.is_valid():
            postserializer.save()
            return JsonResponse(postserializer.data,status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(postserializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':      
                teacherdetail.objects.all().delete()  
            
    return JsonResponse({'message':'all students data deleted'},status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def teacherbyroll(request,idd):
    if request.method == 'GET':
        teacher = teacherdetail.objects.get(id=idd)
        allstudents_serializer = teacherdetailSerializer(teacher)
        return JsonResponse(allstudents_serializer.data,safe = False)



@api_view(['DELETE'])
def teacherdelete(request,pk):
    if request.method == 'DELETE':
        teacherdetail.objects.get(pk=pk).delete()
        return JsonResponse({'message':'student data deleted'})


@api_view(['GET'])
def teacherpaymentview(request,pk):
    if request.method == 'GET':
        monthss = teachpaymonths.objects.filter(teacher__pk=pk)
    
        month_serializer = t_paymentSerializer(monthss ,many=True)
        return JsonResponse(month_serializer.data, safe=False)

@api_view(['POST'])
def updateteacherpayments(request,pk):
    if request.method == 'POST':
        tmonthss = teacherdetail.objects.get(pk=pk)
        data_month = JSONParser().parse(request)
        # try:
        #     monthss = teachpaymonths.objects.get(teacher__pk=pk)
        #     tmonth_serializer = t_paymentSerializer(data=data_month, partial=True)
        #     if tmonth_serializer.is_valid():
        #         tmonth_serializer.save()
        #         return JsonResponse(tmonth_serializer.data,status=status.HTTP_201_CREATED)
        #     else:
        #         return JsonResponse(month_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # except teachpaymonths.DoesNotExist:
        ins = teachpaymonths(teacher=tmonthss)
        print(ins)
        # monthss = teachpaymonths.objects.get(teacher__pk=pk)
        tmonth_serializer = t_paymentSerializer(ins,data=data_month, partial=True)
        if tmonth_serializer.is_valid():
            tmonth_serializer.save()
            return JsonResponse(tmonth_serializer.data,status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(tmonth_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class teachersearch(ListAPIView):
        queryset=teacherdetail.objects.all()
        serializer_class=teacherdetailSerializer
        filter_backends=[SearchFilter]
        search_fields=['t_name','t_fname','sex','c_position','id']