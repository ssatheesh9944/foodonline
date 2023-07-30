from django.shortcuts import render ,redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages
from vendor.forms import VendorForm
# Create your views here.

def registeruser(request):
    if request.method == 'POST':
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            # create the user using the form
            
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()
            
            # create the user using create user method
            # firstname = form.cleaned_data['first_name']
            # lastname = form.cleaned_data['last_name']
            # username = form.cleaned_data['username']
            # email = form.cleaned_data['email']
            # password = form.cleaned_data['password']
            # user = User.objects.create(first_name=firstname,last_name=lastname,username=username,email=email,password=password)
            # user.role = User.CUSTOMER
            # user.save()
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

def registervendor(request):
    if request.method == 'POST':
        # store the data and create the user
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST,request.FILES)
        if form.is_valid() and v_form.is_valid():
            firstname = form.cleaned_data['first_name']
            lastname = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create(first_name=firstname,last_name=lastname,username=username,email=email,password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor.user_profile = UserProfile.objects.get(user=user) 
            vendor.save()
            messages.success(request,'Your Account Has been Registered Successfully please wait for approval')
            return redirect('registervendor')
        else:
            print('form not valid')
            print(form.errors)
                
    else:    
        form = UserForm()
        v_form = VendorForm
    context = {
        'form':form,
        'v_form':v_form
    }
    return render(request,'accounts/registervendor.html',context)
    