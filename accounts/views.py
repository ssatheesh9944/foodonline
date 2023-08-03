from django.shortcuts import render ,redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages
from django.contrib.auth import authenticate ,login , logout
from vendor.forms import VendorForm
from .utils import detectUser
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied


# Restrict the vendor from accessing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

# Restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

def registeruser(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in')
    elif request.method == 'POST':
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
            user = User.objects.create(first_name=firstname,last_name=lastname,username=username,email=email)
            user.set_password(password)
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

def registervendor(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in')
    elif request.method == 'POST':
        # store the data and create the user
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST,request.FILES)
        if form.is_valid() and v_form.is_valid():
            firstname = form.cleaned_data['first_name']
            lastname = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create(first_name=firstname,last_name=lastname,username=username,email=email)
            user.set_password(password)
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
        v_form = VendorForm()
    context = {
        'form':form,
        'v_form':v_form
    }
    return render(request,'accounts/registervendor.html',context)


def userlogin(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in')
        return redirect('myAccount')
    elif  request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(email=email,password=password)
        
        if user is not None:
            login(request,user)
            messages.success(request,'you are now logged in')
            return redirect('myAccount')
        else:
            messages.error(request,'Invalid login credentials')
            return redirect('login')
                
        
    return render(request,'accounts/login.html')    


def userlogout(request):
    logout(request)
    messages.info(request,'You are logged out')
    return redirect('login')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user) 
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request,'accounts/custDashboard.html') 

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request,'accounts/vendorDashboard.html') 
