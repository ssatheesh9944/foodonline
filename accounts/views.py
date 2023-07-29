from django.shortcuts import render ,redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User
from django.contrib import messages
# Create your views here.

def registeruser(request):
    if request.method == 'POST':
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            # create the user using the form
            
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()
            
            # create the user using create user method
            firstname = form.cleaned_data['first_name']
            lastname = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create(first_name=firstname,last_name=lastname,username=username,email=email,password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request,'User Account Has been Registered Successfully')
            print('user created')
            
            return redirect('registeruser')
        else:
            print("invalid")
            print(form.errors)
    else:
        form = UserForm()
    context = {"form":form}
    return render(request,'accounts/registeruser.html',context)