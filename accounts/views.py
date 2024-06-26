from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages

# Create your views here.
def login(request):
    if request.method=='POST':
        username=request.POST["username"]
        password=request.POST["password"]

        user =auth.authenticate(username=username,password=password)        
        if user is not None:
            request.session['user_id'] = user.id
            auth.login(request,user)
            return redirect('success')
        else:
            messages.info(request,'Invalid Credentials.')
            return redirect('login') 
    else:       
        return render(request,'login.html')

def register(request):
    if request.method =='POST':
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        username=request.POST["username"]
        email=request.POST["email"]
        password1=request.POST["password1"]
        password2=request.POST["password2"]

        if password1==password2:
            # if User.objects.filter(username=username).exists():
            #     messages.info(request,'User already exists')
            #     return redirect('register')
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email already exists')
                return redirect('register')
            else:
                user= User.objects.create_user(username=username,password=password1,email=email,
                first_name=first_name,last_name=last_name)
                user.save()
                messages.info(request,'User created')
                return redirect('login') 
        else:
            messages.info(request,'password is not matching')
            return redirect('register')
             
    else:        
        return render(request,'register.html')
    



def success(request):
    users=User.objects.all()

    return render(request,'success.html',{"users":users})

def logout(request):
    auth.logout(request)
    return redirect("login")

def delete(request,user_id):    
    try:
        
        u = User.objects.get(id = user_id)
        u.delete()
        messages.success(request, "The user is deleted")            

    except User.DoesNotExist:
        messages.error(request, "User doesnot exist")    
        return redirect('success') 

    except Exception as e: 
       return redirect('success',{'err':e.message})

    return redirect('success') 

def edit(request,user_id):  
    print("*******",user_id) 
    user = User.objects.get(id = user_id)  
    if request.method =='POST': 
        user.first_name=request.POST["first_name"]
        user.last_name=request.POST["last_name"]
        # user.username=request.POST["username"]
        user.email=request.POST["email"]
        user.password=request.POST["password1"]
        user.save()
        return redirect('success')
        print(user.id)
        print(user.username)
        print(user.first_name)
        print(user.last_login)
        print(user.email)
    else:
     return render(request,'edit_user.html',{'edit_user':user})
