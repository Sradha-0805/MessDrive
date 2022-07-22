from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView
from django.forms.models import model_to_dict
from .models import User, Inmate, Staff
from .forms import InmateSignUpForm, StaffSignUpForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from attendance.models import attendance
from login.models import User

# Create your views here.
def index(request):
    return render(request, 'index.html')
def signin(request):
    return render(request, 'signin.html') 
def about(request):
    return render(request, 'about.html') 
def notification(request):
    return render(request, 'notification.html')
def contact(request):
    return render(request, 'contact.html')
def profile(request):
    return render(request, 'profile.html')
def official(request):
    return render(request, 'starter.html')
def attendance_one(request):
    users = User.objects.filter(is_inmate = True)
    staff = User.objects.filter(is_staff = True).filter(is_superuser = False).filter(is_official = False)
    get_response = request.POST
    absentees_name = dict(get_response).get('absenteeslist')
    print(type(absentees_name))
    for i in absentees_name:
        absentees = User.objects.exclude(id = i).values('id')
        print(absentees)
        b = [d['id'] for d in absentees]
        print(b)
        attendance_mark = attendance()
        for j in b:
                attendance_mark.date = '2022-06-06'
                attendance.userid = j
                attendance_mark.save()
     return render(request, 'attendance.html', {"User" : users, "Staff" : staff})  
    


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if(request.method == 'POST'):
        if(form.is_valid()):
            username = form.cleaned_data.get('username')
            password= form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None and user.is_inmate:
                login(request, user)
                return redirect('profile')
            if user.is_staff and user.is_official:
                login(request, user)
                return redirect('official')    
            elif user is not None and user.is_staff:
                login(request, user)
                return redirect('profile')   
            else:
                msg = "invalid credentials"  
        else:
            msg = "error on validating form"
    return render(request, 'signin.html', {'form': form, 'msg' : msg})                      
        

class inmate_register(CreateView):
    model = User
    form_class = InmateSignUpForm
    template_name = 'inmate.html'
    success_url = 'login_view' 


class staff_register(CreateView):
    model = User
    form_class = StaffSignUpForm
    template_name = 'staff.html'
    success_url = 'login_view' 

