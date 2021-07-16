from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import MyForm, SignIn
from .models import User, ToDo
from random import randint
from django.core.mail import send_mail
from django.conf import settings

default_data = {
    'app_name': 'My ToDo',
    'msgs': {'show': False, 'title': '', 'text': '', 'type': 'primary'}
}

# default page
def index(request):
    return render(request, 'index.html', default_data)

# register page
def register_page(request):
    return render(request, 'register.html', default_data)

# otp page
def otp_page(request):
    return render(request, 'otp_page.html', default_data)

# profile update page
def profile_update_page(request):
    profile_data(request)
    return render(request, 'update_profile.html', default_data)

# otp
def create_otp(request):
    email_to_list = [request.session['reg_data']['email'],]
    
    subject = 'OTP for Todo Registration'

    otp = randint(1000,9999)

    print('OTP is: ', otp)

    request.session['otp'] = otp

    message = f"Your One Time Password for verification is: {otp}"
    
    email_from = settings.EMAIL_HOST_USER
    

    send_mail(subject, message, email_from, email_to_list)

# verify otp
def verify_otp(request):
    if request.method == 'POST':
        otp = int(request.POST['otp'])

        if otp == request.session['otp']:
            User.objects.create(
                Email = request.session['reg_data']['email'],
                Password = request.session['reg_data']['password']
            )

            del request.session['reg_data']
            del request.session['otp']

            default_data['msgs']['text'] = 'Your account has created successfully.'
            default_data['msgs']['title'] = 'Success'
        else:
            default_data['msgs'] = 'Wrong OTP input. Please input correct OTP.'
            default_data['msgs']['title'] = 'Error'
            return redirect(otp_page)

        default_data['msgs']['show'] = True

        return redirect(register_page)
    else:
        pass

# create new user and save to model
def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.all()
        
        for u in user:
            if u.Email == email:
                default_data['msgs'] = f'{email} is exists already. please signin or use different email.'
                default_data['msgs']['show']  = True
                default_data['msgs']['title'] = 'Success'
                
                #break
                return redirect(register_page)
        else:
            request.session['reg_data'] = request.POST
            create_otp(request)
        
            return redirect(otp_page)
    else:
        return HttpResponse('Invalid method')

# load todo
def load_todo(request):
    user = User.objects.get(Email=request.session['email'])
    todo = ToDo.objects.filter(User = user)

    print('todo: ', len(todo))
    default_data['my_todo'] = todo[::-1]
    
    default_data['total_todo'] = len(todo)
    print(default_data['my_todo'])

def profile_data(request, user_obj = None):
    if user_obj:
        default_data['profile_data'] = user_obj
    else:
        user_obj = User.objects.get(Email=request.session['email'])
        default_data['profile_data'] = user_obj
    
    load_todo(request)

# profile page
def profile_page(request):
    profile_data(request)
    return render(request, 'profile.html', default_data)

# change password
def change_password(request):
    if request.method == 'POST':
        user = User.objects.get(Email=request.session['email'])

        if user.Password == request.POST["current_password"]:
            user.Password = request.POST['new_password']

            user.save()
        
            default_data['msgs']['title'] = 'Success'
            default_data['msgs']['text'] = 'Your password has updated.'
            default_data['msgs']['type'] = 'primary'
        else:
            default_data['msgs']['title'] = 'Warning'
            default_data['msgs']['text'] = 'Please enter your current password correctly.'
            default_data['msgs']['type'] = 'warning'
        
        default_data['msgs']['show'] = True
        
        return redirect(profile_update_page)

# create new user and save to model
def profile_update(request):
    if request.method == 'POST':
        user = User.objects.get(Email=request.session['email'])
        
        user.Name = request.POST['name']
        user.Address = request.POST['address']

        if 'profile_photo' in request.FILES:
            user.ProfilePhoto = request.FILES['profile_photo']

        user.save()

        default_data['msgs']['text'] = 'Your profile is updated successfully.'
        default_data['msgs']['show'] = True
        default_data['msgs']['title'] = 'Success'

        return redirect(profile_update_page)
    else:
        return HttpResponse('Invalid method')

# sign in page
def signin_page(request):
    return render(request, 'signin.html', default_data)

# sign in
def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        pwd = request.POST['password']

        try:
            user = User.objects.get(Email=email)
            if user.Password == pwd:
                request.session['email'] = email
                return redirect(profile_page)
            else:
                default_data['msgs'] = 'Your password is incorrect!'
                return redirect(signin_page)

        except User.DoesNotExist as err:
            print('Error: ', err)
            default_data['msgs'] = f'{email} doesn\'t exist. please signup first.'
            return redirect(signin_page)
    else:
        pass

# create new todo
def create_todo(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']

        user = User.objects.get(Email=request.session['email'])

        ToDo.objects.create(
            User=user,
            Title=title,
            Content=content,
        )

        return redirect(profile_page)
    else:
        pass

# update selected todo from user side
def update_todo(request, pk):
    if request.method == 'POST':
        user = User.objects.get(Email=request.session['email'])

        todo = ToDo.objects.get(id = pk, User = user)
        todo.Title = request.POST['title']
        todo.Content = request.POST['content']

        todo.save()

        return redirect(profile_page)
    else:
        return redirect(profile_page)


# delete a todo from user side
def delete_todo(request, pk):
    user = User.objects.get(Email=request.session['email'])

    ToDo.objects.get(id = pk, User = user).delete()

    return redirect(profile_page)

# logout function
def logout(request):
    if 'email' in request.session:
        del request.session['email']
        default_data['msgs']['text'] = 'Logged out successfully!'
        

    return redirect(index)