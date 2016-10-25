from __future__ import unicode_literals

from django.db import models

import re

passwordRegex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')
emailRegex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

import bcrypt
from datetime import date

class UserManager(models.Manager):
    def register(self, name, alias, email, password, confirm, dob):
        errors = 0
        messages = {}
        messages['name_error'] = []
        messages['alias_error'] = []
        messages['email_error'] = []
        messages['password_error'] = []
        messages['confirm_error'] = []
        messages['dob_error'] = []
        #Validations
        #First Name Field
        if len(name) <3:
            messages['name_error'].append('Name must be at least 3 characters!')
            errors += 1
        #Username Field
        if len(alias) <3:
            messages['alias_error'].append('Alias must be at least 3 characters!')
            errors += 1
        #Email Field
        if len(email) < 1:
            messages['email_error'].append('Email cannot be empty!')
            errors += 1
        elif not emailRegex.match(email):
            messages['email_error'].append('Email is not valid!')
            errors += 1
        #Password Field
        if len(password) < 8:
            messages['password_error'].append('Password must be more than 8 characters!')
            errors += 1
        elif not passwordRegex.match(password):
            messages['password_error'].append('Password must contain at least one lowercase letter, one uppercase letter, and one digit')
            errors += 1
        #Confirm Field
        if len(confirm) < 8:
            messages['confirm_error'].append('Confirm Password must be more than 8 characters!')
            errors += 1
        elif password != confirm:
            messages['confirm_error'].append("Passwords Do Not Match")
            errors += 1
        #DOB Field
        birthday = dob
        today = unicode(date.today())
        if birthday > today:
            messages['dob_error'].append("You can't be born in the future!")
            errors += 1
        elif len(dob) <1:
            messages['dob_error'].append('Please enter your birthday!')
            errors += 1
        #FAST-FAIL
        if errors>0:
            #return error messages
            return(False, messages)
        else:
            #register and add user to db
            secret = bcrypt.hashpw(str(password), bcrypt.gensalt())
            query = User.uManager.create(name=name, alias=alias, email=email, password=secret, dob=dob)
            query.save()
            return(True, query)

    def login(self, login_email, login_password):
        errors = 0
        login_messages = {}
        login_messages['login_email_error'] = []
        login_messages['login_password_error'] = []
        #Validations
        #Email Field
        if len(login_email) < 1:
            login_messages['login_email_error'].append("Please enter your email address!")
            errors += 1
        elif not emailRegex.match(login_email):
            login_messages['login_email_error'].append('Login Email is not valid!')
            errors += 1
        #Password Field
        if len(login_password) < 8:
            login_messages['login_password_error'].append("Password must be more than 8 characters!")
            errors += 1
        elif not passwordRegex.match(login_password):
            login_messages['login_password_error'].append("Password must contain at least one lowercase letter, one uppercase letter, and one digit")
            errors += 1
        #FAST-FAIL
        if errors>0:
            #return error messages
            return(False, login_messages)
        else:
            #check if username exists in db
            query = User.uManager.filter(email=login_email)
            input_password = login_password.encode()

            #if username doesn't match, return error message
            if len(query) == 0:
                login_messages['login_email_error'].append("Email not in database! Please register!")
                return(False, login_messages)

            #if username matches, check if passwords match
            elif bcrypt.checkpw(input_password, query[0].password.encode()):
                return(True, query)

            #if username matches and passwords do not match, return error message
            else:
                login_messages['login_password_error'].append('Incorrect Password!')
                return(False, login_messages)

        return redirect('/')



class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    dob = models.DateField(default=date.today())
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    uManager = UserManager()

class QuoteManager(models.Manager):
    def add(self, author, message, user_id):
        errors = 0
        messages = {}
        messages['author_error'] = []
        messages['message_error'] = []
        #Validations
        #Author Field
        if len(author) <3:
            messages['author_error'].append('Author must be more than 3 characters!')
            errors += 1
        #Plan Field
        if len(message) <10:
            messages['message_error'].append('Quote must be more than 10 characters!')
            errors += 1
        #FAST-FAIL
        if errors>0:
            #return error messages
            return(False, messages)
        else:
            #add quote to db
            query = Quote.qManager.create(author=author, message=message, user=User.uManager.get(id=user_id))
            query.save()
            return(True, query)

class Quote(models.Model):
    author = models.CharField(max_length=255)
    message = models.TextField(max_length=1000)
    user = models.ForeignKey(User)
    qManager = QuoteManager()

class Favorite(models.Model):
    user = models.ForeignKey(User)
    quote = models.ForeignKey(Quote)
