from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Reservation, Question
from django.utils import timezone
from django.http import HttpResponseNotAllowed
from .forms import ReservationForm, QuestionForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import pymysql

con = pymysql.connect(host='localhost', user='root', password='dkagh1.', db='django', charset='utf8')
cur = con.cursor()
 

# Create your views here.
# 응답에 대한 처리 함수를 정의할 땐 무조건 매개변수 한 개 이사이 필요
def index(request):
    page = request.GET.get('page', '1')
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    context = {'question_list':page_obj, 'state' : 'True'}
    return render(request, 'pybo/mainpage.html',context) 

# 공지사항 detail
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question' : question}
    return render(request, 'pybo/Notification.html', context)


@login_required(login_url='common:login')
def question_create(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index') 
    else:
        form = QuestionForm()
    context = {'form' : form}
    return render(request, 'pybo/question_detail.html', context)

def reservation(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        n = "update pybo_reservation set NAME=%s" + "where HOSPITAL=%s" + "AND HOUR=%s"
        b = "update pybo_reservation set BIRTH=%s" + "where HOSPITAL=%s" + "AND HOUR=%s"
        v = "update pybo_reservation set VACCINE=%s" + "where HOSPITAL=%s" + "AND HOUR=%s"
        d = "update pybo_reservation set DATE=%s" + "where HOSPITAL=%s" + "AND HOUR=%s"
        check = "select NAME from pybo_reservation where HOSPITAL=%s and HOUR=%s"
        id = "select id from pybo_reservation where HOSPITAL=%s and HOUR=%s"
        cur.execute(check, [request.POST['HOSPITAL'], request.POST['HOUR']])
        x = cur.fetchone()
        cur.execute(id, [request.POST['HOSPITAL'], request.POST['HOUR']])
        y = cur.fetchone()

        if form.is_valid():
            if x[0] == 'N':
                cur.execute(n, [request.POST['NAME'], request.POST['HOSPITAL'], request.POST['HOUR']])
                cur.execute(b, [request.POST['BIRTH'], request.POST['HOSPITAL'], request.POST['HOUR']])
                cur.execute(v, [request.POST['VACCINE'], request.POST['HOSPITAL'], request.POST['HOUR']])
                cur.execute(d, [request.POST['DATE'], request.POST['HOSPITAL'], request.POST['HOUR']])
                con.commit()
                context = {'state' : y[0]}
                return render(request, 'pybo/mainpage.html', context)
            else:
                context = { 'state' : 'False' }
                return render(request, 'pybo/mainpage.html', context)

    else:
        form = ReservationForm()
        info = Reservation.objects
    context = {'form' : form, 'info' : info}
    return render(request, 'pybo/reservation.html', context)

def reservation_check(request):
    form = ReservationForm()
    info = Reservation.objects
    context = {'form' : form, 'info' : info}
    return render(request, 'pybo/reservation_check.html', context)

def reservation_delete(request):
    if request.method == "POST":
        n = "update pybo_reservation set NAME='N' where id=%s" 
        b = "update pybo_reservation set BIRTH='N' where id=%s"
        v = "update pybo_reservation set VACCINE='N' where id=%s"
        d = "update pybo_reservation set DATE='9999-01-01' where id=%s"
        check = "select NAME from pybo_reservation where id=%s"
        id = request.POST['ID']
        cur.execute(check, [id])
        x = cur.fetchone()
        if x[0] != 'N':
            cur.execute(n, [id])
            cur.execute(b, [id])
            cur.execute(v, [id])
            cur.execute(d, [id])
            con.commit()
            context = {'state' : 'Delete'}
            return render(request, 'pybo/mainpage.html', context)
        else:
            context = { 'state' : 'Error' }
            return render(request, 'pybo/mainpage.html', context)
    else:
        form = ReservationForm()
        info = Reservation.objects
    context = {'form' : form, 'info' : info}
    return render(request, 'pybo/reservation_check.html', context)