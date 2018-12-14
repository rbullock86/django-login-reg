from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django import forms


def index(request):
    print("*** running index() ***")
    return render(request, "octo_app/index.html")


def registration(request):
    print("*** running registration() ***")
    postData = request.POST
    errors = User.objects.register_validation(postData)

    if len(errors) > 0:
        print("*** registration validation errors ***")
        request.session['errors'] = errors
        request.session['first_name'] = postData['first_name']
        request.session['last_name'] = postData['last_name']
        request.session['birthday'] = postData['birthday']
        request.session['email'] = postData['email']
        return redirect("/")

    else:
        User.objects.create_user(postData)
        request.session.clear()
        request.session['first_name'] = postData['first_name']
        request.session['last_name'] = postData['last_name']
        request.session['email'] = postData['email']
        request.session['success_type'] = 'registered'
        return redirect("/success")


def login(request):
    request.session.clear()
    print("*** running login() ***")
    postData = request.POST
    errors = User.objects.login_validation(postData)

    if len(errors) > 0:
        request.session['errors'] = errors
        request.session['login_email'] = postData['login_email']
        return redirect("/")

    else:
        user = User.objects.get(email=postData['login_email'])
        request.session.clear()
        request.session['first_name'] = user.first_name
        request.session['success_type'] = "logged in"
        return redirect("/success")



def success(request):
    print("*** running success() ***")
    return render(request, "octo_app/success.html")