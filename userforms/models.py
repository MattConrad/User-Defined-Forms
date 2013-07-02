from django.db import models

class UserForm(models.Model):
    title = models.CharField(max_length=50, unique=True)
    html = models.TextField()
    fields = models.CharField(max_length=2000)   # this is a python dict
    indt = models.DateTimeField(auto_now_add=True)
    updt = models.DateTimeField(auto_now=True)

class CompletedUserForm(models.Model):
    UserForm = models.ForeignKey(UserForm)
    indt = models.DateTimeField(auto_now_add=True)
    updt = models.DateTimeField(auto_now=True)

class CUFData(models.Model):
    CompletedUserForm = models.ForeignKey(CompletedUserForm)
    field = models.CharField(max_length=50)
    value = models.CharField(max_length=255)


