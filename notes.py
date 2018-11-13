# class 2nd: we will make registration page here now.
#copy User into form.py for registration:
from django import forms  
from employee.models import Employee
from django.contrib.auth.models import User

class userform(forms.ModelForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter UserName'}),required=True,max_length=30)
	email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter email'}),required=True,max_length=30)
	first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter first Name'}),required=True,max_length=30)
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter last Name'}),required=True,max_length=30)
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form--control','placeholder':'Enter Password'}),required=True,max_length=30)
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form--control','placeholder':'Enter confirm Password'}),required=True,max_length=30)

	class Meta():
		model= User
		fields=['username','email','first_name','last_name','password','confirm_password']


class EmployeeForm(forms.ModelForm):  
    class Meta:  
        model = Employee  
        fields = "__all__"  



#create HTML(named registration) in templayes folder:
{% load static %}
<html>
<head>
   <title>Sample</title>
   <link rel="stylesheet" href="{% static 'style.css' %}"/>
   </head>
<body background="{% static 'images/background.jpg' %}">
<h1>User Registration Form</h1>

<form method="POST" action="" class="col-md-5">
    {% csrf_token %}
    {{ frm.as_p }}
    <button type="submit">Submit</button>
</form>
<a href="/display">Click Here to show data</a>
</body>
</html>



#define registration function in views.py:
from django.shortcuts import render, redirect , HttpResponse  #added httpresponse cozused in function regiatration below. 
from employee.forms import *		#we have done it * here from Employeeforms.. as there is une more function mentioned in Forms.py now.. name userform.
from employee.models import Employee
from django.contrib.auth.models import User     
# Create your views here.  
def emp(request):  
    if request.method == "POST":  
        form = EmployeeForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/show')  
            except:  
                pass  
    else:  
        form = EmployeeForm()  
    return render(request,'index.html',{'form':form})  
def show(request):  
    employees = Employee.objects.all()  #here Employee is class the in models.py
    return render(request,"show.html",{'employees':employees})  
def edit(request, id):  
    employee = Employee.objects.get(id=id)  
    return render(request,'edit.html', {'employee':employee})  
def update(request, id):  
    employee = Employee.objects.get(id=id)  
    form = EmployeeForm(request.POST, instance = employee)  #instance sae whi employee entry edit hogi..koi new employee create nii hoga.
    if form.is_valid():  
        form.save()  
        return redirect("/show")  
    return render(request, 'edit.html', {'employee': employee})  
def destroy(request, id):  
    employee = Employee.objects.get(id=id)  
    employee.delete()  
    return redirect("/show")  
def home(request):
	return render(request,'home.html')

def registration(request): #Added this.
    if request.method=='POST':
        form1=userform(request.POST)
        if form1.is_valid():
            username=form1.cleaned_data['username']
            first_name = form1.cleaned_data['first_name']
            last_name = form1.cleaned_data['last_name']
            email = form1.cleaned_data['email']
            password = form1.cleaned_data['password']
            User.objects.create_user(username=username,
            first_name=first_name,last_name=last_name,
            email=email,password=password)
            return HttpResponse('<h1>Thank You</h1>')
    else:
        form1=userform()
    return render(request,'registration.html',{'frm':form1})



#now go to urls.py--> to add registration.
from django.contrib import admin
from django.urls import path
from employee import views
from employee.views import *	#Added This.
urlpatterns = [  
    path('admin/', admin.site.urls),  
    path('emp', views.emp),  
    path('show',views.show),  
    path('edit/<int:id>', views.edit),  
    path('update/<int:id>', views.update),  
    path('delete/<int:id>', views.destroy),  
	path('',views.home),
    path('registration',registration),	#added this.
]  



#add email validation to forms.py:
from django import forms  
from employee.models import Employee
from django.contrib.auth.models import User
from django.core.validators import validate_email 

class userform(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter UserName'}),required=True,max_length=30)
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter email'}),required=True,max_length=30)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter first Name'}),required=True,max_length=30)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter last Name'}),required=True,max_length=30)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form--control','placeholder':'Enter Password'}),required=True,max_length=30)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form--control','placeholder':'Enter confirm Password'}),required=True,max_length=30)

    class Meta():
        model= User
        fields=['username','email','first_name','last_name','password','confirm_password']

    def clean_email(self):
        email=self.cleaned_data['email']
        try:
            ma=validate_email(email)
        except:
            raise forms.ValidationError("Email is not valid")
        return email

    def clean_confirm_password(self):
        p=self.cleaned_data['password']
        cp=self.cleaned_data['confirm_password']
        if(p!=cp):
            raise forms.ValidationError("confirm password and password must be same")
        else:
            if(len(p)<8):
                raise forms.ValidationError("password must be atleast 8 character")
            if(p.isdigit()):
                raise forms.ValidationError("password must contain atleast 8 character")


class EmployeeForm(forms.ModelForm):  
    class Meta:  
        model = Employee  
        fields = "__all__"  



#homework:
#add these all to your CRUD.. homework.
first name
last name
gender:choices button
phone
email
address
marital status
langues known: check box
age: date fill.



#CLASS 3: login banayenge aaj.
#make login.html in templates:
<div style="width:300px;height:150px;margin-left:350px">
    <h2 style="width:300px;height:40px;background-color:gray;font-family:stencil;font-size:25px;padding-top:15px"><center>Login</center></h2>
    <form method="POST" action="/check">{% csrf_token %}
        <table>
            <tr height=50px><th>Username</th>
            <td><input type="text" name="username" Value="" id="username"></td>
            </tr>


            <tr height=50px><th>Password:</th>
            <td><input type="Password" name="password" value="" id="password"></td>
            </tr>
        </table><br>
        <input type="submit" name="Login"/>
    </form>
<a href="/registration">Register</a>
    
</div


#make login function in views.py:
from django.shortcuts import render, redirect , HttpResponse   
from employee.forms import *
from employee.models import Employee
from django.contrib.auth.models import User     




# Create your login function in views.py here.  
def emp(request):  
    if request.method == "POST":  
        form = EmployeeForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/show')  
            except:  
                pass  
    else:  
        form = EmployeeForm()  
    return render(request,'index.html',{'form':form})  
def show(request):  
    employees = Employee.objects.all()  #here Employee is class the in models.py
    return render(request,"show.html",{'employees':employees})  
def edit(request, id):  
    employee = Employee.objects.get(id=id)  
    return render(request,'edit.html', {'employee':employee})  
def update(request, id):  
    employee = Employee.objects.get(id=id)  
    form = EmployeeForm(request.POST, instance = employee)  #instance sae whi employee entry edit hogi..koi new employee create nii hoga.
    if form.is_valid():  
        form.save()  
        return redirect("/show")  
    return render(request, 'edit.html', {'employee': employee})  
def destroy(request, id):  
    employee = Employee.objects.get(id=id)  
    employee.delete()  
    return redirect("/show")  
def home(request):
    return render(request,'home.html')

def registration(request): 
    if request.method=='POST':
        form1=userform(request.POST)
        if form1.is_valid():
            username=form1.cleaned_data['username']
            first_name = form1.cleaned_data['first_name']
            last_name = form1.cleaned_data['last_name']
            email = form1.cleaned_data['email']
            password = form1.cleaned_data['password']
            User.objects.create_user(username=username,
            first_name=first_name,last_name=last_name,
            email=email,password=password)
            return HttpResponse('<h1>Thank You</h1>')
    else:
        form1=userform()
    return render(request,'registration.html',{'frm':form1})


def log_in(request):     #this one.
    return render (request,'login.html')



#define login path in urls.py:
from django.contrib import admin
from django.urls import path
from employee import views
from employee.views import *
urlpatterns = [  
    path('admin/', admin.site.urls),  
    path('emp', views.emp),  
    path('show',views.show),  
    path('edit/<int:id>', views.edit),  
    path('update/<int:id>', views.update),  
    path('delete/<int:id>', views.destroy),  
    path('',views.home),
    path('registration',registration),
    path('login',log_in)     #this one.
]  




#now make check funtion in views.py:
from django.shortcuts import render, redirect , HttpResponse   
from employee.forms import *
from employee.models import Employee
from django.contrib.auth.models import User     
from django.contrib.auth import authenticate, Login  #Updated this.




# Create check function in views.py:  
def emp(request):  
    if request.method == "POST":  
        form = EmployeeForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/show')  
            except:  
                pass  
    else:  
        form = EmployeeForm()  
    return render(request,'index.html',{'form':form})  
def show(request):  
    employees = Employee.objects.all()  #here Employee is class the in models.py
    return render(request,"show.html",{'employees':employees})  
def edit(request, id):  
    employee = Employee.objects.get(id=id)  
    return render(request,'edit.html', {'employee':employee})  
def update(request, id):  
    employee = Employee.objects.get(id=id)  
    form = EmployeeForm(request.POST, instance = employee)  #instance sae whi employee entry edit hogi..koi new employee create nii hoga.
    if form.is_valid():  
        form.save()  
        return redirect("/show")  
    return render(request, 'edit.html', {'employee': employee})  
def destroy(request, id):  
    employee = Employee.objects.get(id=id)  
    employee.delete()  
    return redirect("/show")  
def home(request):
    return render(request,'home.html')

def registration(request): 
    if request.method=='POST':
        form1=userform(request.POST)
        if form1.is_valid():
            username=form1.cleaned_data['username']
            first_name = form1.cleaned_data['first_name']
            last_name = form1.cleaned_data['last_name']
            email = form1.cleaned_data['email']
            password = form1.cleaned_data['password']
            User.objects.create_user(username=username,
            first_name=first_name,last_name=last_name,
            email=email,password=password)
            return redirect('/login')       #changed it to redirect instead of tahnk you msg now.
    else:
        form1=userform()
    return render(request,'registration.html',{'frm':form1})


def log_in(request):
    return render (request,'login.html')


def check(request):     #Added this.
    username=request.POST['username']
    password=request.POST['password']
    user = authenticate(username=username , password=password)  #authenticate is imported above.
    if user is not None:
        login(request)      # this is imprted above
        return redirect('/emp')
    else:
        return HttpResponse('<h1> invalid </h1>')



#set path for check function on urls.py:
from django.contrib import admin
from django.urls import path
from employee import views
from employee.views import *
urlpatterns = [  
    path('admin/', admin.site.urls),  
    path('emp', views.emp),  
    path('show',views.show),  
    path('edit/<int:id>', views.edit),  
    path('update/<int:id>', views.update),  
    path('delete/<int:id>', views.destroy),  
    path('',views.home),
    path('registration',registration),
    path('login',login),
    path('check',check),        #Added this.
]  

#now make logout button in index.html:
<html>
<head>  
    <title>Index</title>  
    {% load staticfiles %}  
    <link rel="stylesheet" href="{% static 'style.css' %}"/>  
</head>  
<body>  
<form method="POST" class="post-form" action="/emp">  #--After submit.. it will take us to "/emp" -->
        {% csrf_token %}  
    <div class="container">  
<br>  
    <div class="form-group row">  
    <label class="col-sm-1 col-form-label"></label>  
    <div class="col-sm-4">  
    <h3>Enter Details</h3>  
    </div>  
  </div>  
    <div class="form-group row">  
    <label class="col-sm-2 col-form-label">Employee Id:</label>  
    <div class="col-sm-4">  
      {{ form.eid }}    <!--it gives us a text box.. without even usung text box -->
    </div>  
  </div>  
  <div class="form-group row">  
    <label class="col-sm-2 col-form-label">Employee Name:</label>  
    <div class="col-sm-4">  
      {{ form.ename }}  
    </div>  
  </div>  
    <div class="form-group row">  
    <label class="col-sm-2 col-form-label">Employee Email:</label>  
    <div class="col-sm-4">  
      {{ form.eemail }}  
    </div>  
  </div>  
    <div class="form-group row">  
    <label class="col-sm-2 col-form-label">Employee Contact:</label>  
    <div class="col-sm-4">  
      {{ form.econtact }}  
    </div>  
  </div>  
    <div class="form-group row">  
    <label class="col-sm-1 col-form-label"></label>  
    <div class="col-sm-4">  
    <button type="submit" class="btn btn-primary">Submit</button>  
    </div>  
  </div>  
    </div>  
</form>  
    <div class="form-group row">  
    <label class="col-sm-1 col-form-label"></label>  
    <div class="col-sm-4">
    <button type="submit" class="btn btn-primary">Log Out</button>  #Added logout.
    </div> 
  </form>
</body>  
</html>  


#define logout function in views.py:
from django.shortcuts import render, redirect , HttpResponse   
from employee.forms import *
from employee.models import Employee
from django.contrib.auth.models import User     
from django.contrib.auth import authenticate, login, logout     #logout imported.


# Create logout function in views.py here.  
def emp(request):  
    if request.method == "POST":  
        form = EmployeeForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/show')  
            except:  
                pass  
    else:  
        form = EmployeeForm()  
    return render(request,'index.html',{'form':form})  
def show(request):  
    employees = Employee.objects.all()  #here Employee is class the in models.py
    return render(request,"show.html",{'employees':employees})  
def edit(request, id):  
    employee = Employee.objects.get(id=id)  
    return render(request,'edit.html', {'employee':employee})  
def update(request, id):  
    employee = Employee.objects.get(id=id)  
    form = EmployeeForm(request.POST, instance = employee)  #instance sae whi employee entry edit hogi..koi new employee create nii hoga.
    if form.is_valid():  
        form.save()  
        return redirect("/show")  
    return render(request, 'edit.html', {'employee': employee})  
def destroy(request, id):  
    employee = Employee.objects.get(id=id)  
    employee.delete()  
    return redirect("/show")  
def home(request):
    return render(request,'home.html')

def registration(request): 
    if request.method=='POST':
        form1=userform(request.POST)
        if form1.is_valid():
            username=form1.cleaned_data['username']
            first_name = form1.cleaned_data['first_name']
            last_name = form1.cleaned_data['last_name']
            email = form1.cleaned_data['email']
            password = form1.cleaned_data['password']
            User.objects.create_user(username=username,
            first_name=first_name,last_name=last_name,
            email=email,password=password)
            return redirect('/login')
    else:
        form1=userform()
    return render(request,'registration.html',{'frm':form1})


def log_in(request):
    return render (request,'login.html')


def check(request):
    username=request.POST['username']
    password=request.POST['password']
    user = authenticate(username=username , password=password)
    if user is not None:
        login(request)
        return redirect('/emp')
    else:
        return HttpResponse('<h1> invalid </h1>')


def log_out(request):       #Added this. choose log_out coz logout is predefined.
    logout(request) #this is imported above.
    return render(request,'login.html')


#add log_out path to urls.py file: 
from django.contrib import admin
from django.urls import path
from employee import views
from employee.views import *
urlpatterns = [  
    path('admin/', admin.site.urls),  
    path('emp', views.emp),  
    path('show',views.show),  
    path('edit/<int:id>', views.edit),  
    path('update/<int:id>', views.update),  
    path('delete/<int:id>', views.destroy),  
    path('',views.home),
    path('registration',registration),
    path('login',login),
    path('check',check),
    path('logout',log_out), #Added This.
]  



#now Add Decorators to show function(url) so that it is not visible without login:
#(we can do it to oter functions(urls) too.. lie edit.. update..emp...)
from django.shortcuts import render, redirect , HttpResponse   
from employee.forms import *
from employee.models import Employee
from django.contrib.auth.models import User     
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required   #decorators imported
# Create your views here.  
def emp(request):  
    if request.method == "POST":  
        form = EmployeeForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/show')  
            except:  
                pass  
    else:  
        form = EmployeeForm()  
    return render(request,'index.html',{'form':form})  
@login_required(login_url= '/login')        #decoratorused for show url. 
def show(request):  
    employees = Employee.objects.all()  #here Employee is class the in models.py
    return render(request,"show.html",{'employees':employees})  
def edit(request, id):  
    employee = Employee.objects.get(id=id)  
    return render(request,'edit.html', {'employee':employee})  
def update(request, id):  
    employee = Employee.objects.get(id=id)  
    form = EmployeeForm(request.POST, instance = employee)  #instance sae whi employee entry edit hogi..koi new employee create nii hoga.
    if form.is_valid():  
        form.save()  
        return redirect("/show")  
    return render(request, 'edit.html', {'employee': employee})  
def destroy(request, id):  
    employee = Employee.objects.get(id=id)  
    employee.delete()  
    return redirect("/show")  
def home(request):
    return render(request,'home.html')

def registration(request): 
    if request.method=='POST':
        form1=userform(request.POST)
        if form1.is_valid():
            username=form1.cleaned_data['username']
            first_name = form1.cleaned_data['first_name']
            last_name = form1.cleaned_data['last_name']
            email = form1.cleaned_data['email']
            password = form1.cleaned_data['password']
            User.objects.create_user(username=username,
            first_name=first_name,last_name=last_name,
            email=email,password=password)
            return redirect('/login')
    else:
        form1=userform()
    return render(request,'registration.html',{'frm':form1})


def log_in(request):
    return render (request,'login.html')


def check(request):
    username=request.POST['username']
    password=request.POST['password']
    user = authenticate(username=username , password=password)
    if user is not None:
        login(request)
        return redirect('/emp')
    else:
        return HttpResponse('<h1> invalid </h1>')


def log_out(request):
    logout(request)
    return render(request,'login.html')



#class 4th on CRUD.. CONTINUE... :


email through django:

#setting up TLS server in settings.py(at the bottom). 

STATIC_URL = '/static/'


EMAIL_USE_TLS=True      #Added from here
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_HOST_USER='hbaghelducat@gmail.com'        #this is host id..email bhejne waale ki
EMAIL_HOST_PASSWORD='root@123'      #host id password.


#importing email in views.py and adding email settings to registration page in views.py:
from django.shortcuts import render, redirect , HttpResponse   
from employee.forms import *
from employee.models import Employee
from django.contrib.auth.models import User     
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail  #Added
from crud import settings   #Added
# Create your views here.  
def emp(request):  
    if request.method == "POST":  
        form = EmployeeForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/show')  
            except:  
                pass  
    else:  
        form = EmployeeForm()  
    return render(request,'index.html',{'form':form})  
@login_required(login_url= '/login')
def show(request):  
    employees = Employee.objects.all()  #here Employee is class the in models.py
    return render(request,"show.html",{'employees':employees})  
def edit(request, id):  
    employee = Employee.objects.get(id=id)  
    return render(request,'edit.html', {'employee':employee})  
def update(request, id):  
    employee = Employee.objects.get(id=id)  
    form = EmployeeForm(request.POST, instance = employee)  #instance sae whi employee entry edit hogi..koi new employee create nii hoga.
    if form.is_valid():  
        form.save()  
        return redirect("/show")  
    return render(request, 'edit.html', {'employee': employee})  
def destroy(request, id):  
    employee = Employee.objects.get(id=id)  
    employee.delete()  
    return redirect("/show")  
def home(request):
    return render(request,'home.html')

def registration(request): 
    if request.method=='POST':
        form1=userform(request.POST)
        if form1.is_valid():
            username=form1.cleaned_data['username']
            first_name = form1.cleaned_data['first_name']
            last_name = form1.cleaned_data['last_name']
            email = form1.cleaned_data['email']
            password = form1.cleaned_data['password']
            subject="Confirmation mail" #added
            msg="Dear sir/Ma'am,thanx For your details contact visit:"  #added
            send_mail(subject,msg,settings.EMAIL_HOST_USER,[email]) #Added.
            User.objects.create_user(username=username,
            first_name=first_name,last_name=last_name,
            email=email,password=password)
            return redirect('/login')
    else:
        form1=userform()
    return render(request,'registration.html',{'frm':form1})


def log_in(request):
    return render (request,'login.html')


def check(request):
    username=request.POST['username']
    password=request.POST['password']
    user = authenticate(username=username , password=password)
    if user is not None:
        login(request,user)
        return redirect('/emp')
    else:
        return HttpResponse('<h1> invalid </h1>')


def log_out(request):
    logout(request)
    return render(request, 'login.html')


# CLASS 5 CRUD.... continues...:
#adding search to our CRUD.

#add search function in views.py.
from django.shortcuts import render, redirect , HttpResponse   
from employee.forms import *
from employee.models import Employee
from django.contrib.auth.models import User     
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from crud import settings
# Create your views here.  
def emp(request):  
    if request.method == "POST":  
        form = EmployeeForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/show')  
            except:  
                pass  
    else:  
        form = EmployeeForm()  
    return render(request,'index.html',{'form':form})  
@login_required(login_url= '/login')
def show(request):  
    employees = Employee.objects.all()  #here Employee is class the in models.py
    return render(request,"show.html",{'employees':employees})  
def edit(request, id):  
    employee = Employee.objects.get(id=id)  
    return render(request,'edit.html', {'employee':employee})  
def update(request, id):  
    employee = Employee.objects.get(id=id)  
    form = EmployeeForm(request.POST, instance = employee)  #instance sae whi employee entry edit hogi..koi new employee create nii hoga.
    if form.is_valid():  
        form.save()  
        return redirect("/show")  
    return render(request, 'edit.html', {'employee': employee})  
def destroy(request, id):  
    employee = Employee.objects.get(id=id)  
    employee.delete()  
    return redirect("/show")  
def home(request):
    return render(request,'home.html')

def registration(request): 
    if request.method=='POST':
        form1=userform(request.POST)
        if form1.is_valid():
            username=form1.cleaned_data['username']
            first_name = form1.cleaned_data['first_name']
            last_name = form1.cleaned_data['last_name']
            email = form1.cleaned_data['email']
            password = form1.cleaned_data['password']
            subject="Confirmation mail"
            msg="Dear sir/Ma'am,thanx For your details contact visit:"
            send_mail(subject,msg,settings.EMAIL_HOST_USER,[email])
            User.objects.create_user(username=username,
            first_name=first_name,last_name=last_name,
            email=email,password=password)
            return redirect('/login')
    else:
        form1=userform()
    return render(request,'registration.html',{'frm':form1})


def log_in(request):
    return render (request,'login.html')


def check(request):
    username=request.POST['username']
    password=request.POST['password']
    user = authenticate(username=username , password=password)
    if user is not None:
        login(request,user)
        return redirect('/emp')
    else:
        return HttpResponse('<h1> invalid </h1>')


def log_out(request):
    logout(request)
    return render(request, 'login.html')


def search(request):        #Added this
    if request.method=='POST': #post liya.. cz we don't want to show the data on url.
        squery=request.POST['search_box1']   #squery mein data liya yha per.
        if squery is not None:      #ager sqery hui.. tou if loop chalega.
            s=Employee.objects.filter(ename=squery) #ename sae search kar rhe hein.
            if s:
                return render(request,'search.html',{'q':s})    #search page bane kar wha per print kr denge.. agar kuch mila tou.
            else:
                return HttpResponse('<h1> NOT FOUND </h1>')
        else:
            return redirect('/show')
    return redirect('/')


#show.html pae butoon ban denge ek,, search k naam sae.:
<html>
<head>  
    <meta charset="UTF-8">  
    <title>Employee Records</title>  
     {% load staticfiles %}  
    <link rel="stylesheet" href="{% static 'style.css' %}"/>  
</head>  
<body>  
<form action=''>        #Added this.. from here.
    <div class="form-group row">
        <label class="col-sm-2 col-form-label">Enter Name:</label>
        <div class="col-sm-4">
            <input type="text" name="search_box1" placeholder="Enter Employee Name">
        </div>      #name="search_box1" menioned above.. will be same as mentioned in def search in views.py.
    </div>
    <div class="form-group row">
        <label class="col-sm-1 col-form-label"></label>
        <div class="col-sm-4">
            <button type="submit" class="btn btn-primary">Search</button>
        </div>
    </div>
    
</form>     #till here.
<table class="table table-striped table-bordered table-sm">  
    <thead class="thead-dark">  
    <tr>  
        <th>Employee ID</th>  
        <th>Employee Name</th>  
        <th>Employee Email</th>  
        <th>Employee Contact</th>  
        <th>Actions</th>  
    </tr>  
    </thead>  
    <tbody>  
{% for employee in employees %}  
    <tr>  
        <td>{{ employee.eid }}</td>  
        <td>{{ employee.ename }}</td>  
        <td>{{ employee.eemail }}</td>  
        <td>{{ employee.econtact }}</td>  
        <td>  
            <a href="/edit/{{ employee.id }}"><span class="glyphicon glyphicon-pencil" >Edit</span></a>  
            <a href="/delete/{{ employee.id }}">Delete</a>  
        </td>  
    </tr>  
{% endfor %}  
    </tbody>  
</table>  
<br>  
<br>  
<center><a href="/emp" class="btn btn-primary">Add New Record</a></center>  

  <form action="logout">
    <div class="form-group row">  
    <label class="col-sm-1 col-form-label"></label>  
    <div class="col-sm-4">
    <button type="submit" class="btn btn-primary">Log Out</button>
    </div> 
  </form>
</body>  
</html>  


#Add search pathn in urls.py:
from django.contrib import admin
from django.urls import path
from employee import views
from employee.views import *
urlpatterns = [  
    path('admin/', admin.site.urls),  
    path('emp', views.emp),  
    path('show',views.show),  
    path('edit/<int:id>', views.edit),  
    path('update/<int:id>', views.update),  
    path('delete/<int:id>', views.destroy),  
    path('',views.home),
    path('registration',registration),
    path('login',log_in),
    path('check',check),
    path('logout',log_out),
    path('search',search),      #Added this.
]  

#mention search url in html of shoe.html:
<html>
<head>  
    <meta charset="UTF-8">  
    <title>Employee Records</title>  
     {% load staticfiles %}  
    <link rel="stylesheet" href="{% static 'style.css' %}"/>  
</head>  
<body>  
<form action='/search'>     #added this.. this search here is added.
    <div class="form-group row">
        <label class="col-sm-2 col-form-label">Enter Name:</label>
        <div class="col-sm-4">
            <input type="text" name="search_box1" placeholder="Enter Employee Name">
        </div>
    </div>
    <div class="form-group row">
        <label class="col-sm-1 col-form-label"></label>
        <div class="col-sm-4">
            <button type="submit" class="btn btn-primary">Search</button>
        </div>
    </div>
    
</form>
<table class="table table-striped table-bordered table-sm">  
    <thead class="thead-dark">  
    <tr>  
        <th>Employee ID</th>  
        <th>Employee Name</th>  
        <th>Employee Email</th>  
        <th>Employee Contact</th>  
        <th>Actions</th>  
    </tr>  
    </thead>  
    <tbody>  
{% for employee in employees %}  
    <tr>  
        <td>{{ employee.eid }}</td>  
        <td>{{ employee.ename }}</td>  
        <td>{{ employee.eemail }}</td>  
        <td>{{ employee.econtact }}</td>  
        <td>  
            <a href="/edit/{{ employee.id }}"><span class="glyphicon glyphicon-pencil" >Edit</span></a>  
            <a href="/delete/{{ employee.id }}">Delete</a>  
        </td>  
    </tr>  
{% endfor %}  
    </tbody>  
</table>  
<br>  
<br>  
<center><a href="/emp" class="btn btn-primary">Add New Record</a></center>  

  <form action="logout">
    <div class="form-group row">  
    <label class="col-sm-1 col-form-label"></label>  
    <div class="col-sm-4">
    <button type="submit" class="btn btn-primary">Log Out</button>
    </div> 
  </form>
</body>  
</html>  


#now make search.html page:
#copy whole show page into it.. with slight modification.

<html>
<head>  
    <meta charset="UTF-8">  
    <title>Employee Records</title>  
     {% load staticfiles %}  
    <link rel="stylesheet" href="{% static 'style.css' %}"/>  
</head>  
<body>  
<form action='/search' method="POST">   #modified this too.. is POST is requird in def search.
    {% csrf_token %}        #add csrf security.
    <div class="form-group row">
        <label class="col-sm-2 col-form-label">Enter Name:</label>
        <div class="col-sm-4">
            <input type="text" name="search_box1" placeholder="Enter Employee Name">
        </div>
    </div>
    <div class="form-group row">
        <label class="col-sm-1 col-form-label"></label>
        <div class="col-sm-4">
            <button type="submit" class="btn btn-primary">Search</button>
        </div>
    </div>
    
</form>
<table class="table table-striped table-bordered table-sm">  
    <thead class="thead-dark">  
    <tr>  
        <th>Employee ID</th>  
        <th>Employee Name</th>  
        <th>Employee Email</th>  
        <th>Employee Contact</th>  
        <th>Actions</th>  
    </tr>  
    </thead>  
    <tbody>  
{% for employee in q %} #tis is modified:(employees is replaced with q.. as "q" is the key value in search function in views.py)  
    <tr>  
        <td>{{ employee.eid }}</td>  
        <td>{{ employee.ename }}</td>  
        <td>{{ employee.eemail }}</td>  
        <td>{{ employee.econtact }}</td>  
        <td>  
            <a href="/edit/{{ employee.id }}"><span class="glyphicon glyphicon-pencil" >Edit</span></a>  
            <a href="/delete/{{ employee.id }}">Delete</a>  
        </td>  
    </tr>  
{% endfor %}  
    </tbody>  
</table>  
<br>  
<br>  
<center><a href="/emp" class="btn btn-primary">Add New Record</a></center>  

  <form action="logout">
    <div class="form-group row">  
    <label class="col-sm-1 col-form-label"></label>  
    <div class="col-sm-4">
    <button type="submit" class="btn btn-primary">Log Out</button>
    </div> 
  </form>
</body>  
</html>  


#add methot="POST" and{% csrf_token %} to show.html too: below form:
<html>
<head>  
    <meta charset="UTF-8">  
    <title>Employee Records</title>  
     {% load staticfiles %}  
    <link rel="stylesheet" href="{% static 'style.css' %}"/>  
</head>  
<body>  
<form action='/search'  method="POST">      #added method="POST" here.
    {% csrf_token %}        #Added here:
    <div class="form-group row">
        <label class="col-sm-2 col-form-label">Enter Name:</label>
        <div class="col-sm-4">
            <input type="text" name="search_box1" placeholder="Enter Employee Name">
        </div>
    </div>
    <div class="form-group row">
        <label class="col-sm-1 col-form-label"></label>
        <div class="col-sm-4">
            <button type="submit" class="btn btn-primary">Search</button>
        </div>
    </div>
    
</form>
<table class="table table-striped table-bordered table-sm">  
    <thead class="thead-dark">  
    <tr>  
        <th>Employee ID</th>  
        <th>Employee Name</th>  
        <th>Employee Email</th>  
        <th>Employee Contact</th>  
        <th>Actions</th>  
    </tr>  
    </thead>  
    <tbody>  
{% for employee in employees %}  
    <tr>  
        <td>{{ employee.eid }}</td>  
        <td>{{ employee.ename }}</td>  
        <td>{{ employee.eemail }}</td>  
        <td>{{ employee.econtact }}</td>  
        <td>  
            <a href="/edit/{{ employee.id }}"><span class="glyphicon glyphicon-pencil" >Edit</span></a>  
            <a href="/delete/{{ employee.id }}">Delete</a>  
        </td>  
    </tr>  
{% endfor %}  
    </tbody>  
</table>  
<br>  
<br>  
<center><a href="/emp" class="btn btn-primary">Add New Record</a></center>  

  <form action="logout">
    <div class="form-group row">  
    <label class="col-sm-1 col-form-label"></label>  
    <div class="col-sm-4">
    <button type="submit" class="btn btn-primary">Log Out</button>
    </div> 
  </form>
</body>  
</html>  




#class continue: upload images to our page.
#issey pehle project9 revise krlo.. image upload project.

#add eimage in models.
from django.db import models

class Employee(models.Model):  
    eid = models.CharField(max_length=20)  
    ename = models.CharField(max_length=100)  
    eemail = models.EmailField()  
    econtact = models.CharField(max_length=15)  
    eimage=models.ImageField(upload_to="emp")   #added this
    class Meta:  
        db_table = "employee"


#Add register.FILES in views.py:
def emp(request):  
    if request.method == "POST":  
        form = EmployeeForm(request.POST,request.FILES) #added here  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/show')  
            except:  
                pass  
    else:  
        form = EmployeeForm()  
    return render(request,'index.html',{'form':form})  


def update(request, id):  
    employee = Employee.objects.get(id=id)  
    form = EmployeeForm(request.POST,request.FILES, instance = employee) #added here.. changed this one. 
    if form.is_valid():  
        form.save()  
        return redirect("/show")  
    return render(request, 'edit.html', {'employee': employee})   


#now add enctype and image button in index.html:
<head>  
    <title>Index</title>  
    {% load staticfiles %}  
    <link rel="stylesheet" href="{% static 'style.css' %}"/>  
</head>  
<body>  
<form method="POST" class="post-form" action="/emp" enctype="Multipart/form-data"> #added this
        {% csrf_token %}  
    <div class="form-group row">    #added this.
      <label class="col-sm-2 col-form-label">Employee Image</label>
      <div class="col-sm-4">
        {{ form.eimage }}
        
      </div>
      </div>
    <div class="container">  
<br>  
    <div class="form-group row">  
    <label class="col-sm-1 col-form-label"></label>  
    <div class="col-sm-4">  
    <h3>Enter Details</h3> 


#add media_ROOT and media_URL to settings.py:

STATIC_URL = '/static/'


EMAIL_USE_TLS=True
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_HOST_USER='hbaghelducat@gmail.com'
EMAIL_HOST_PASSWORD='root@123'



MEDIA_ROOT= os.path.join(BASE_DIR,'media')  #added this
MEDIA_URL='/media/' #added this.


#import files and add static url in urls.py:

from django.contrib import admin
from django.urls import path
from employee import views
from employee.views import *
from django.conf import settings    #added this
from django.conf.urls.static import staticfiles#added this
urlpatterns = [  
    path('admin/', admin.site.urls),  
    path('emp', views.emp),  
    path('show',views.show),  
    path('edit/<int:id>', views.edit),  
    path('update/<int:id>', views.update),  
    path('delete/<int:id>', views.destroy),  
    path('',views.home),
    path('registration',registration),
    path('login',log_in),
    path('check',check),
    path('logout',log_out),
    path('search',search),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  #added this.


#now add uploaded image on show.html:
<table class="table table-striped table-bordered table-sm">  
    <thead class="thead-dark">  
    <tr>  
        <th>Employee ID</th>  
        <th>Employee Name</th>  
        <th>Employee Email</th>  
        <th>Employee Contact</th>
        <th>Employee Image</th>     #added this... to add column to the table. 
        <th>Actions</th>  
    </tr>  
    </thead>  
    <tbody>  
{% for employee in employees %}  
    <tr>  
        <td>{{ employee.eid }}</td>  
        <td>{{ employee.ename }}</td>  
        <td>{{ employee.eemail }}</td>  
        <td>{{ employee.econtact }}</td>
        <td><img src="media/{{employee.eimage}}" width=50px></td>#this will upload the file. here we used media in "media/{{employee.eimage}}".. coz in settings.py.. we have mentioned the image_URL default to media folder.
        <td>  
            <a href="/edit/{{ employee.id }}"><span class="glyphicon glyphicon-pencil" >Edit</span></a>  
            <a href="/delete/{{ employee.id }}">Delete</a>  
        </td>  
    </tr>  
{% endfor %}  

    </tbody>  
</table>  


















#gitbub
#python anywhere
#gitbash software.
















































































































































































































































































