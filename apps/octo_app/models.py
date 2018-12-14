from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from datetime import *
import re
import bcrypt


class UserManager(models.Manager):
    def register_validation(self, postData):
        print("*** in UserManager.register_validation() ***")
        errors = {}
        # checking validity of name lengths
        if len(postData['first_name']) < 2:
            errors["first_name_error"] = "First name should be at least two characters"
        if len(postData['last_name']) < 2:
            errors["last_name_error"] = "Last name should be at least two characters"
 
        # checking to see if registering person is old enough!
        
        dob = postData["birthday"].split('-')
        dob = list(map(int, dob))
        now = date.today().strftime('%Y-%m-%d')
        now = now.split('-')
        now = list(map(int, now))


        if now[0] - dob[0] < 80:
            errors["birthday_error"] = "You are not old enough"
        elif now[0] - dob[0] == 80:
            if dob[1] > now[1]:
                errors["birthday_error"] = "You are not old enough"
            else:
                if (dob[2] > now[2]) and (dob[1] == now[1]):
                    errors["birthday_error"] = "You are not old enough"

            

        # checking to see if email is already taken
        e1 = postData['email']
        if User.objects.filter(email=e1).exists():
            errors["email_error"] = "Email is already taken"
        elif re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", postData['email']) == None:
            errors["email_error"] = "Not a valid email address"
        
        # checking password length and confirmation
        if len(postData['password']) < 8:
            errors["password_error"] = "Password should be at least eight characters"
        elif postData['password'] != postData['confirm_pw']:
            errors["password_error"] = "Passwords do not match"

        return errors

    def create_user(self, postData):
        print("*** in UserManager.create_user() ***")
        hash1 = make_password(postData["password"])
        User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], birthday=postData['birthday'], email=postData['email'], password=hash1)

    def login_validation(self, postData):
        print("*** in UserManager.login_user() ***")
        errors = {}

        if User.objects.filter(email=postData['login_email']).exists == False:
            errors['login_email_error'] = "No account under that email"
            return errors

        user = User.objects.get(email=postData['login_email'])

        if check_password(postData['login_password'], user.password) == True:
            print("password matches")
        else:
            errors['login_password_error'] = "Password does not match"
        return errors




class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()