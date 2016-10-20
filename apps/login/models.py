from __future__ import unicode_literals
from django.db import models
import re, bcrypt

# NAME_REGEX = re.compile(r'^[A-Za-z]')
EMAIL_REGEX= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.



class UserManager(models.Manager):
    def validate_inputs(self, params):
        errors=[]
#Dont pass the request object around
        if not re.match(EMAIL_REGEX, params['email']):
            errors.append("Not a valid email format")

        user = User.objects.filter(email=params['email'])
        if user:
            errors.append("Email already exist")

        if len(params['f_name']) < 2 or len(params['l_name']) < 2:
            errors.append("First Name should be longer than 2 characters")

        # if not re.match(NAME_REGEX, params['f_name']) or re.match(NAME_REGEX, params['l_name']):
        #     errors.append("Name should have letters only")

        if len(params['password']) < 8:
            errors.append("Password should be longer than 8 characters")

        if not str(params['password'])== str(params['cpassword']):
            errors.append("passwords do not match")

        return errors

    def reg_valid(self, params):
        errors = self.validate_inputs(params)
        if len(errors) > 0:
            return (False, errors)

        pw_hash = bcrypt.hashpw(params['password'].encode(), bcrypt.gensalt())
        user = self.create(f_name = params['f_name'], pw_hash = pw_hash, email = params['email'], l_name = params['l_name'])
        return (True, user)

    def login_valid(self, params):
        print params['password']
        user = User.objects.filter(email = params['email'])
        if user:
            if bcrypt.hashpw(params['password'].encode(), user[0].pw_hash.encode()) == user[0].pw_hash.encode():
                print bcrypt.hashpw(params['password'].encode(), user[0].pw_hash.encode())
                print bcrypt.hashpw(params['password'].encode(), bcrypt.gensalt())
                print user[0].pw_hash
                return (True, user[0])
            else:
                return (False, ["Email/password inside do not exist"])
        else:
            return (False, ["Email/password do not exist"])

# * will unpack a list and ** will unpack a dictionary

class User(models.Model):
    f_name = models.CharField(max_length=255) #unique =True(model validations)
    l_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    pw_hash = models.CharField(max_length=255)
    cpassword= models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
