from django.shortcuts import  render, redirect
from django.http import HttpResponse
from app.models import Employee, Visitor
from .forms import NewUserForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import SessionAuthentication
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer,employeeSerializer,visitorSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
def index(request):
    return render(request,'index.html',{})
def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("home")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})
def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user:
				login(request, user)
				messages.info(request, "You are now logged.")
				return redirect("home.html")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})
def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("home.html")
@login_required(login_url='login.html')
def emp(request):
	if(request.method=='POST'):
		name1=request.POST['name']
		email=request.POST['email']
		department=request.POST['department']
		location=request.POST['location']
		emp1=Employee(name=name1,email=email,dept=department,location=location)
		emp1.save()
	emp_data=Employee.objects.all()
	return render(request,"employee.html",{'employees':emp_data})
def delete_emp(request,emp_id):
	emp=Employee.objects.get(pk=emp_id)
	emp.delete()
	emp_data=Employee.objects.all()
	return render(request,"employee.html",{'employees':emp_data})
def update_emp(request,emp_id):
	emp_update=Employee.objects.get(pk=emp_id)
	emp=Employee.objects.all()
	return render(request,"employee.html",{'update':emp_update,'employees':emp})
def updated_emp(request,emp_id):
	emp_updated=Employee.objects.get(pk=emp_id)
	emp_updated.name=request.POST['name']
	emp_updated.email=request.POST['email']
	emp_updated.dept=request.POST['department']
	emp_updated.location=request.POST['location']
	emp_updated.save()
	emp=Employee.objects.all()
	return render(request,"employee.html",{'employees':emp})
@login_required(login_url='login.html')
def vis(request):
	if(request.method=='POST'):
		name1=request.POST['name']
		email=request.POST['email']
		department=request.POST['department']
		location=request.POST['location']
		employee_name=request.POST['attend_emp']
		status=request.POST['status']
		emp1=Visitor(name=name1,email=email,phone=department,location=location,employee_name=employee_name,status=status)
		emp1.save()
	emp_data=Visitor.objects.all()
	return render(request,"visitor.html",{'employees':emp_data})
def delete_vis(request,vis_id):
	emp=Visitor.objects.get(pk=vis_id)
	emp.delete()
	emp_data=Visitor.objects.all()
	return render(request,"visitor.html",{'employees':emp_data})
def update_vis(request,vis_id):
	emp_update=Visitor.objects.get(pk=vis_id)
	status1=emp_update.status
	emp=Visitor.objects.all()
	return render(request,"visitor.html",{'update':emp_update,'employees':emp,'status1':status1})
def updated_vis(request,vis_id):
	emp_updated=Visitor.objects.get(pk=vis_id)
	emp_updated.name=request.POST['name']
	emp_updated.email=request.POST['email']
	emp_updated.phone=request.POST['department']
	emp_updated.location=request.POST['location']
	emp_updated.employee_name=request.POST['attend_emp']
	emp_updated.status=request.POST['status']
	emp_updated.save()
	emp=Visitor.objects.all()
	return render(request,"visitor.html",{'employees':emp})
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })
class emplist(generics.ListCreateAPIView):
	authentication_classes = (TokenAuthentication,SessionAuthentication)
	permission_classes = (IsAuthenticated,)
	queryset=Employee.objects.all()
	serializer_class=employeeSerializer

class empdetail(generics.RetrieveUpdateDestroyAPIView):
	authentication_classes = (TokenAuthentication,SessionAuthentication)
	permission_classes = (IsAuthenticated,)
	queryset = Employee
	serializer_class=employeeSerializer

class visitorlist(generics.ListCreateAPIView):
	authentication_classes = (TokenAuthentication,SessionAuthentication)
	permission_classes = (IsAuthenticated,)
	queryset=Visitor.objects.all()
	serializer_class=visitorSerializer

class visitordetail(generics.RetrieveUpdateDestroyAPIView):
	authentication_classes = (TokenAuthentication,SessionAuthentication)
	permission_classes = (IsAuthenticated,)
	queryset = Visitor
	serializer_class=visitorSerializer