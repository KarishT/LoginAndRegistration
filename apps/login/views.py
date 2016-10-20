from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.contrib import messages
# Create your views here
def index(request):
    return render(request, 'login/index.html')

def register(request):
        if request.method == 'POST':
            params ={
                'f_name' : request.POST['f_name'],
                'l_name' : request.POST['l_name'],
                'email' : request.POST['email'],
                'password' : request.POST['password'],
                'cpassword' : request.POST['cpassword']
            }

            result = User.objects.reg_valid(params)
            if result[0] == False:
                print_messages(request, result[1])
                return redirect('/')

            return login_success(request, result[1])

def login(request):
    if request.method == 'POST':
        params ={
        'email' : request.POST['email'],
        'password' : request.POST['password']
        }
        result = User.objects.login_valid(params)
        if result[0] == False:
            print_messages(request, result[1])
            return redirect('/')
        return login_success(request, result[1])
            #load our succesful login page

def login_success(request, user):
    print "session thing starts"
    request.session['user'] = {
        'id' : user.id,
        'first_name' : user.f_name,
        'last_name' : user.l_name,
        'email' : user.email,
    }
    return redirect ('/success')

def print_messages(request, message_list):
    for message in message_list:
        print message
        messages.add_message(request, messages.INFO, message)

def success(request):
    if not 'user' in request.session:
        return redirect('/')
    return render(request, 'login/success.html')

def logout(request):
    request.session.pop('user')
    return redirect('/')
