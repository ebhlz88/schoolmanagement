"""schoolmanagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from school import views,teacher,authlogin,sms,calculate
from knox import views as knox_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.studentslist.as_view()),
    path('student/<int:roll>', views.studentByroll),
    path('fees', views.feesget),
    path('feesByroll/<int:roll>', views.feesgetByroll),
    path('feespost/<int:roll>/<str:standardd>',views.feespost),
    path('result/<int:sroll>/<str:standardd>', views.getstudentresult),
    path('resultpost/<int:roll>/<str:standardd>/<str:ssubject>',views.postresult),
    path('standardlist', views.standardlist),
    path('subjectlist', views.subjectlist),
    path('studentsearch/',views.studentsearch.as_view()),
    path('books/<str:stsandardd>',views.allbooks.as_view()),
    path('rbystandard/<str:standardd>/<str:ssubject>',views.getresultBystandard),
    path('enrollments/<int:roll>',views.getenrollments),

    path('resbystandard/<str:standardd>',views.getstudentresultbystandard),
    path('studentstandard/<int:roll>',views.updateStandardInStudent),

    path('calcsubject/<int:roll>/<str:subjectt>', calculate.calcsubject),
    path('nofsubjects/<int:roll>/<str:subjectt>', calculate.nofsubjects),
    

    path('allteachers', teacher.teacheroverall.as_view()),
    path('teacherbyroll/<int:idd>', teacher.teacherbyroll),
    path('teacherpayment/<int:pk>', teacher.teacherpaymentview),
    path('tpaymentpost/<int:pk>', teacher.updateteacherpayments),
    path('teachersearch/',teacher.teachersearch.as_view()),


    path('register', authlogin.RegisterAPI.as_view(), name='register'),
    path('login', authlogin.LoginAPI.as_view(), name='login'),
    path('logout', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('sms', sms.broadcast_sms,name='default'),


    path('calc/<int:year>', calculate.allmoneyfromstudents),
    path('tcalc/<int:year>', calculate.allteacherpayment),
    path('count', calculate.countfunction),
    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
