
from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
from datetime import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]')

# Create your models here.
class userManager(models.Manager):
	def register(self, post):
		first = post['first_name']
		alias  = post['alias']
		email = post['email']
		password = post['password']
		passwordCheck = post['passwordCheck']
		bday = post['bday']
		errors = []
		userId = 0


		if len(first) < 2:
			errors.append('first name must be longer than 2 characters')

		if len(alias) < 2:
			errors.append('alias name must be longer than 2 characters')

		if len(email) < 1:
			errors.append('email cannot be blank')
		elif not EMAIL_REGEX.match(email):
			errors.append('email not in right format')
		
		if len(password) < 1:
			errors.append('password cannot be blank')
		elif len(password) < 8:
			errors.append('password needs to be grater than 8 characters')

		if bday == "":
			errors.append('please enter a bday')

		if password != passwordCheck:
			errors.append('password does not match')


		if not errors:
			emailExist = User.objects.filter(email=email)
			if not emailExist:
				hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
				user = User.objects.create(email=email, first_name= first, alias=alias, password=hashed, birthday=bday)
				userId = user.id
			else:
				errors.append('Invalid login')
		
		return [errors, userId]

	def login(self, post):
		email = post['email']
		password = post['password']
		errors = []
		userId = 0
		
		if len(email) < 1:
			errors.append('email cannot be blank')
		elif not EMAIL_REGEX.match(email):
			errors.append('email not in right format')
		
		if len(password) < 1:
			errors.append('password cannot be blank')
		elif len(password) < 8:
			errors.append('password needs to be grater than 8 characters')
		
		if not errors:
			emailExist = User.objects.filter(email=email)

			if emailExist:
				hashed = emailExist[0].password

				if bcrypt.hashpw(password.encode(), hashed.encode()) == hashed:
					userId = emailExist[0].id
			else:
				errors.append('Invalid login')


		return [errors, userId]

class User(models.Model):
	first_name = models.CharField(max_length=50)
	alias = models.CharField(max_length=50, default="alias")
	email = models.CharField(max_length=100)
	password = models.CharField(max_length=255)
	birthday = models.DateField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = userManager()





class itemManager(models.Manager):
	def add_item_to_db(self, post, id):
		item = post['item']
		errors = []

		if len(item) < 1:
			errors.append("please enter a item")
		elif len(item) < 3:
			errors.append("items length must be longer that 3 characters")
		
		if not errors:
			userObject = User.objects.filter(id = id)
			userObject = userObject[0]
			item = Item.objects.create(item = item , user = userObject)

			Wishlist.objects.create(item = item , user = userObject)

		return errors
	def add_to_wishlist(self, itemId, userId):
		userObject = User.objects.filter(id = userId)
		userObject = userObject[0]
		item = Item.objects.filter(id=itemId)
		item = item[0]
		Wishlist.objects.create(item = item , user = userObject)
		return item

class Item(models.Model):
	item = models.CharField(max_length=50)
	user = models.ForeignKey('User')
	created_at = models.DateTimeField(auto_now_add = True)
	objects = itemManager()


class Wishlist(models.Model):
	user = models.ForeignKey('User')
	item = models.ForeignKey('Item')
	objects = itemManager()


