from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from cryptography.fernet import Fernet


# Create your views here.
def login(request):    
    if request.method=='POST':              
            try: 
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
            except Exception as e:
                  print(e)
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

            # key = Fernet.generate_key()

            # with open("D:\\encrypt_pwd.key", "wb") as key_file:
            #    key_file.write(key)

            # f = Fernet(key)
            # enc_pwd = f.encrypt(password1.encode())       

            password2=request.POST["password2"]
            if '' not in (username, password1, email, first_name,last_name):

                    if password1==password2:
                        if User.objects.filter(username=username).exists():
                            messages.info(request,'User already exists')
                            return redirect('register')
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
                messages.info(request,'All fields are mandatory')
                return redirect('register')
                
        else:        
            return render(request,'register.html')
    except Exception as e:
        print(e)


def success(request):
    try:
        users=User.objects.all()
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
 try:
    print("*******",user_id) 
    user = User.objects.get(id = user_id)  
    if request.method =='POST': 
     
            user.first_name=request.POST["first_name"]
            user.last_name=request.POST["last_name"]
            # user.username=request.POST["username"]
            user.email=request.POST["email"]
            user.password=request.POST["password1"]
            confirmPassword=request.POST["password2"]
            if '' not in ( user.first_name, user.last_name, user.email, user.password,confirmPassword):
                if user.password==confirmPassword:                   
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
