from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User, UserManager, MessagePost, MessageManager, Comment

def home_reroute(request):
    return redirect('/login')

def login(request):
    return render(request, "login.html")

def  sucess(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    context = {
        'all_messages':MessagePost.objects.all()
    }
    return render(request, "sucess.html", context)

def logout(request):
    request.session.clear()
    return redirect('/login')

def register(request):
    if request.method=='POST':
        errors=User.objects.validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/login')

        user_pw=request.POST['pw']
        hash_pw=bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
        print(hash_pw)
        new_user = User.objects.create(first_name=request.POST['f_n'], last_name=request.POST['l_n'], email=request.POST['email'], password=hash_pw)
        print(new_user)
        request.session['user_id']=new_user.id
        request.session['user_name']=f"{new_user.first_name} {new_user.last_name}"
        return redirect('/sucess')
    return redirect('/login')

def log_in(request):
    if request.method=='POST':
        logged_user=User.objects.filter(email=request.POST['email'])
        if logged_user:
            logged_user=logged_user[0]
            if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.password.encode()):
                request.session['user_id']=logged_user.id
                request.session['user_name']=f"{logged_user.first_name} {logged_user.last_name}"
                return redirect('/sucess')
    return redirect('/login')

def create_mess(request):
    if request.method=='POST':
        error=MessagePost.objects.empty_validator(request.POST)
        if error:
            messages.error(request, error)
            return redirect('/sucess')
        MessagePost.objects.create(content=request.POST['content'], poster=User.objects.get(id=request.session['user_id']))
        return redirect('/sucess')
    return redirect('/login')


