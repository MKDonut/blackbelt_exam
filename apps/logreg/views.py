from django.shortcuts import render, redirect
from .models import User, UserManager, Trip, TripManager
from django.contrib import messages
from django.core.urlresolvers import reverse

def index(request):
	
	return render(request, 'logreg/index.html')

def register_user(request):
	res = User.objects.register_user(request.POST)
	if res["added"]:
		request.session['logged_in']=True
		messages.success(request, "Hello, {}".format(res["new_user"].first_name))
		return redirect(reverse('my_users:success'))
	else:
		request.session['logged_in']=False
		for error in res["errors"]:
			messages.error(request, error)
		return redirect(reverse('my_users:index'))
def login_user(request):
	print("Something")
	reqs = User.objects.Login_user(request.POST)
	if reqs["checked"]:
		request.session['logged_in']=True
		messages.success(request, "Successful Login! Welcome, {}".format(reqs["logger"].first_name))
		return redirect(reverse('my_users:success'))
	else:
		for error in reqs["errors"]:
			request.session['logged_in']=False
			messages.error(request, error)
		return redirect(reverse('my_users:index'))

def success(request):
	context={
		"trips":Trip.objects.all()
	}
	if not request.session['logged_in']:
		return redirect(reverse('my_users:index'))
	return render(request,'logreg/success.html', context)

def logout(request):
	request.session['logged_in']=False
	return redirect(reverse('my_users:index'))
def trip_validation(request):
	valids = Trip.objects.trip_validation(request.POST)
	if valids["valid"]:
		request.session["new_trip"]=True
		return redirect(reverse('my_users:success'))
	else:
		for error in valids["errors"]:
			request.session["new_trip"]=False
			messages.error(request, error)
		return redirect(reverse('my_users:plan'))

def add_plan(request):
	Trip.objects.create(destination=request.POST["destination"], description=request.POST["description"])
	return redirect(reverse('my_users:success'))

def plan(request):
	
	return render(request,'logreg/plan.html')
 
def join(request):
 	user=User.objects.get(id=request.POST['user_id'])
 	trip= Trip.objects.get(id=request.Post['trip_id'])
 	trip.users.add(user)
	return render(request, 'my_users:success', context)

# Create your views here.
