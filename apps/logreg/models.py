from __future__ import unicode_literals
from datetime import datetime, timedelta
from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
import bcrypt

class UserManager(models.Manager):
	def register_user(self, data):
		password = data["password"].encode()
		hashed = bcrypt.hashpw(password, bcrypt.gensalt())
		
		errors = []
		if not data["first_name"]:
			errors.append("Please enter your first name")
		elif len(data["first_name"]) < 3:
			errors.append("Please enter more that 2 characters")
		if not data["last_name"]:
			errors.append("Please enter your last name")
		elif len(data["last_name"]) < 3:
			errors.append("Please enter more that 2 characters")
		if not data["email"]:
			errors.append("Please enter your email")
		elif not EMAIL_REGEX.match(data["email"]):
			errors.append("Invalid email")
		if not data["password"]:
			errors.append("Enter Password")
		elif not len(data["password"]) >= 8:
			errors.append("Need more characters!")
		if not data["confirm_password"]:
			errors.append("Confirm Password")
		elif data["confirm_password"] != data["password"]:
			errors.append("Passwords do not match")

		response = {}
		if not errors:
			new_user=self.create(first_name=data["first_name"],last_name=data["last_name"], email=data["email"], password=hashed, confirm_password=data["confirm_password"])
			response ["added"]=True
			response ["new_user"]= new_user
		else:
			response["added"]=False
			response["errors"]=errors
		return response

	def Login_user(self, data):
		user= self.filter(email=data["email"])
		print user
		errors=[]
		reqs={}
		if not user:
			errors.append("Please register or check spelling")
		else: 
			user=user[0]
			if bcrypt.hashpw(data['password'].encode(), user.password.encode()) ==user.password.encode():
				reqs["checked"]=True
				reqs["logger"]=user
			else: 
				errors.append("Email and Password do not match")
		
		if errors:
			reqs["checked"]=False
			reqs["errors"]=errors
		return reqs		


class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	confirm_password = models.CharField(max_length=255, default = 'SOME STRING')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class TripManager(models.Manager):
	def trip_validation(self, data):
		errors=[]
		if not data["destination"]:
			errors.append("Please fill out your destination")
		if not data["description"]:
			errors.append("Please fill out your description")
		if not data["date_from"]:
			errors.append("Please fill out travel date from")
		if not data["date_to"]:
			errors.append("Please fill out travel date to")
		elif data["date_from"] == data["date_to"]:
			error.append("Travel date from cannot be same as travel date to")
		elif not data["date_from"] > data["date_to"]:
			errors.append("Travel to date must be after travel from date")

		valids={}
		if not errors:
			new_trip=self.create(destination=data["destination"], description=data["description"], date_from=data["date_from"], date_to=data["date_to"])
			valids ["valid"]=True
			valids ["new_trip"]= new_trip
		else:
			valids["valid"]=False
			valids["errors"]=errors
		return valids


class Trip(models.Model):
	destination=models.CharField(max_length=255)
	description=models.TextField(max_length=1000)
	date_from=models.DateTimeField(auto_now_add=True)
	date_to=models.DateField(auto_now=True)
	users= models.ManyToManyField(User, related_name="trips")


# Create your models here.
