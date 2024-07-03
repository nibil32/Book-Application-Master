from django import forms

from book.models import Books

from django.contrib.auth.models import User

class BooksForm(forms.Form):

    name=forms.CharField()
    author=forms.CharField()
    price=forms.IntegerField()
    genre=forms.CharField()
    

class BooksModelForm(forms.ModelForm):

    class Meta:
        model=Books
        fields="__all__"


        widgets={
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "author":forms.TextInput(attrs={"class":"form-control"}),
            "price":forms.NumberInput(attrs={"class":"form-control"}),
            "genre":forms.TextInput(attrs={"class":"form-control"}),
            "language":forms.TextInput(attrs={"class":"form-control"}),
            
            
             
             
            
        }



class RegistrationForm(forms.ModelForm):

    class Meta:
        model=User
        fields=["username","email","password"]


        widgets={
            "username":forms.TextInput(attrs={"class":"form-control","placeholder":"enter your username"}),
            "email":forms.EmailInput(attrs={"class":"form-control","placeholder":"enter your email"}),
            "password":forms.PasswordInput(attrs={"class":"form-control","placeholder":"enter your password"}),
        }



class LoginForm(forms.Form):
    
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))