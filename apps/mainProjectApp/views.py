from django.shortcuts import render, redirect
from . import models
from django.contrib import messages

# Create your views here.
def index(request):
	return render(request, 'mainProjectApp/index.html')

def newUser(request):
	res = models.User.objects.register(request.POST)
	message = "registered"
	return processSignon(request, res, message)

def signOn(request):
	res = models.User.objects.login(request.POST)
	message = "logged on"
	return processSignon(request, res, message)

def processSignon(request, res, message):	
	if not res[0]:
		messages.success(request, "You have successfully {}!!!!".format(message))
		request.session['id'] = res[1]
		return redirect('/success')

	for error in res[0]:
		messages.warning(request, error)
	return redirect('/')

def success(request):
	if request.session.get('id'):
		userWishlistIds =[]
		userInfo = models.User.objects.filter(id = request.session['id'])
		userWishlist = models.Wishlist.objects.all().filter(user__id = userInfo)
		for ids in userWishlist:
			userWishlistIds.append(ids.item.id)
		items = models.Item.objects.all().exclude(id__in = userWishlistIds)
		data = {"user":userInfo[0], "userWishlist": userWishlist, "items":items}
		return render(request, "mainProjectApp/success.html", data)
	return redirect('/')

def add_item(request):
	if request.session.get('id'):
		return render(request, 'mainProjectApp/add_item.html')
	return redirect('/')

def add_item_db(request):
	response = models.Item.objects.add_item_to_db(request.POST, request.session['id'])
	if not response:
		messages.success(request, "You have successfully added a item!")
		return redirect('/success')
	else:
		for error in response:
			messages.warning(request, error)
		return redirect('/add_item')

def add_to_wishlist(request, id):
	item = models.Wishlist.objects.add_to_wishlist(id, request.session['id'])
	return redirect('/success')

def item_page(request, id):
	if request.session.get('id'):
		users = models.Wishlist.objects.filter(item__id = id)
		data = {"users":users, "item":users[0].item}
		return render(request, 'mainProjectApp/item_page.html', data)
	return redirect('/')


def remove_wishlist(request, id):
	models.Wishlist.objects.filter(item__id = id, user__id = request.session['id']).delete()
	return redirect('/success')


def delete(request, id):
	models.Wishlist.objects.filter(item__id= id).delete()
	models.Item.objects.filter(id= id).delete()
	return redirect('/success')

def logout(request):
	request.session.clear()
	return redirect('/')