from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model ,logout ,login
from django.contrib.auth.decorators import  login_required

User = get_user_model()

# Create your views here.

@login_required
def home(request):
  title = 'Home Page'
  context = {
    'title':title,
  }
  return render(request, 'home.html', context)

def register_view(request):
  title = 'Register Page'
  if request.method == 'POST':
    username = request.POST['username'].lower()
    email = request.POST['email'].lower()
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    password = request.POST['password']
    password_2 = request.POST['password_2']
    check_email = User.objects.filter(email=email)
    check_username = User.objects.filter(username=username)
    if check_email.count():
      raise ValidationError('This Email Is Already Taken')
    elif check_username.count():
      raise ValidationError('This Username Is Already Taken')
    elif not password:
      raise ValidationError('no password')
    elif password != password_2:
      raise ValidationError('passwords don\'t match')
    else:
      new_user = User.objects.create_user(
        username = username,
        email = email,
        first_name = first_name,
        last_name = last_name,
        password = password,
      )
      new_user.save()
      new = User.objects.get(email=email)
      new2 = new.id
      send_mail(
        'Test Email',
        f'''
        Hello {first_name}\n
        This Is Testing  Email Send\n
        Activate Your Account Here: http://127.0.0.1:8000/user/activate/{new2}
        ''',
        'quadracode4@gmail.com',
        [email, 'fomr777@gmail.com'],
        fail_silently=False )
      return redirect('login_url')
  context = {
    'title' : title,
  }
  return render(request, 'register.html', context)

def activate_view(request, id):
  title = 'Activate Account'
  activate = User.objects.get(id=id)
  name = f'{activate.first_name} {activate.last_name}'
  activate.activated = True
  activate.save()
  context = {
    'title':title,
    'name':name,
  }
  return render(request, 'activate.html', context)

def login_view(request):
  title = 'Login Page'
  next = request.GET.get('next')
  if request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']
    if email and password:
      check_email = User.objects.filter(email = email)
      if check_email:
        user  = authenticate(email = email, password = password)
      else:
        raise ValidationError('Wrong email')
      if not user:
        raise ValidationError('Wrong password')
      elif not user.is_active:
        raise ValidationError('This User Is Not  Active')
      else:
        login(request, user)
        if next:
          return redirect(next)
        else:
          return  redirect('home_url')
  context={
    'title':title,
    'next':next,
  }
  return render(request,'login.html',context)

def logout_view(request):
    logout(request)
    return redirect('login_url')