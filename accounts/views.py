from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import auth
from django.contrib import messages
from cryptography.fernet import Fernet
from user_login_reg import settings
from .models import user_data

fernet_key=settings.FERNET_KEY.encode()
key = Fernet(fernet_key)

# Create your views here.
def login(request):    
    if request.method=='POST':              
             
        username=request.POST["username"]
        password=request.POST["password"] 
        try:
            user = user_data.objects.get(username = username) 
            dec_pwd =key.decrypt(user.password.encode()).decode()
            if(password==dec_pwd):
                # user =auth.authenticate(username=username,password=password)  
                
                    user = user_data.objects.get(username=username, password=user.password)      
                    if user is not None:
                            request.session['user_id'] = user.id
                            # auth.login(request,user)
                            return redirect('success')               
        except user_data.DoesNotExist:
                    messages.info(request,'Invalid Credentials.')
                    return redirect('login') 
    else:       
        return render(request,'login.html')
   
def register(request):
    try:
        if request.method =='POST':
            first_name=request.POST["first_name"]
            last_name=request.POST["last_name"]
            username=request.POST["username"]
            email=request.POST["email"]
            password1=request.POST["password1"]
            password2=request.POST["password2"]
            enc_password = key.encrypt(password1.encode()).decode()   
           
            if '' not in (username, password1, email,  first_name,last_name):

                    if password1==password2:
                        if user_data.objects.filter(username=username).exists():
                            messages.info(request,'User already exists')
                            return redirect('register')
                        if user_data.objects.filter(email=email).exists():
                            messages.info(request,'Email already exists')
                            return redirect('register')
                        else:
                            user= user_data.objects.create(username=username,password=enc_password,email=email,
                            first_name=first_name,last_name=last_name)
                            user.save()
                            messages.info(request,'User created')
                            return redirect('login')                      
                            
                    else:
                        messages.info(request,'password is not matching')
                        return redirect('register')
            else:
                messages.info(request,'All fields are mandatory')
                return redirect('register')
                
        else:        
            return render(request,'register.html')
    except Exception as e:
        print(e)


def success(request):
    try:
        users=user_data.objects.all()
        # user_id=request.session.get('user_id')
        # if user_id is not None:     
        return render(request,'success.html',{"users":users})
        # else:
        #     return redirect("login")
    except Exception as e:
        print(e)

def logout(request):
    try:
        auth.logout(request)
        return redirect("login")
    except Exception as e:
        print(e)

def delete(request,user_id):    
    try:
        
        user = user_data.objects.get(id = user_id)
        user.delete()
        messages.success(request, "The user is deleted")            

    except user.DoesNotExist:
        messages.error(request, "User doesnot exist")    
        return redirect('success') 

    except Exception as e: 
       return redirect('success',{'err':e.message})

    return redirect('success') 

def edit(request,user_id):  
 try:
    print("*******",user_id) 
    user = user_data.objects.get(id = user_id)  
    print("^^^^^^^^^^^^^^^^^^^^^",user.password)
    if request.method =='POST': 
     
            user.first_name=request.POST["first_name"]
            user.last_name=request.POST["last_name"]
            user.email=request.POST["email"]
            user.password=request.POST["password1"]
            password2=request.POST["password2"]
            enc_password = key.encrypt(user.password.encode()).decode()   


            if '' not in ( user.first_name, user.last_name, user.email, user.password,password2):
                if user.password==password2:   
                    user.password=enc_password                
                    user.save()
                    return redirect('success')
                else:
                    messages.info(request,'password is not matching')
                    return render(request,'edit_user.html',{'edit_user':user,'pageName':'edit'})
            else:
                messages.info(request,'All fields are mandatory')
                return render(request,'edit_user.html',{'edit_user':user,'pageName':'edit'})
    else:
     return render(request,'edit_user.html',{'edit_user':user,'pageName':'success'})
    
 except Exception as e: 
       print(e)  
