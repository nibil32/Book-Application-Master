from django.shortcuts import render,redirect
from book.forms import BooksForm,BooksModelForm,RegistrationForm,LoginForm
from django.views.generic import View
from book.models import Books
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper


@method_decorator(signin_required,name="dispatch")
class BooksCreateView(View):

    def get(self,request,*args,**kwargs):
        form=BooksModelForm()
        return render(request,"book_add.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=BooksModelForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"book has been added")
            print("created")
            return(render,"book_add.html",{"form":form})
        else:
            messages.error(request,"failed to add book")
            return(render,"book_add.html",{"form":form})
        
@method_decorator(signin_required,name="dispatch")
class BooksListView(View):

    def get(self,request,*args,**kwargs):
        qs=Books.objects.all()
        languages=Books.objects.all().values_list("language",flat=True).distinct
        print(languages)
        if "language" in request.GET:
            lang=request.GET.get("language")
            qs=qs.filter(language__iexact=lang)
        return render(request,"book_list.html",{"data":qs,"languages":languages})
     
    def post(self,request,*args,**kwargs):
        name=request.POST.get("box")
        qs=Books.objects.filter(name__icontains=name)
        return render(request,"book_list.html",{"data":qs})
    
@method_decorator(signin_required,name="dispatch")     
class BooksDetailView(View):
    
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Books.objects.get(id=id)
        return render(request,"book_detail.html",{"data":qs})
    

@method_decorator(signin_required,name="dispatch")
class BooksDeleteView(View):

    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Books.objects.get(id=id).delete()
        messages.error(request,"book removed")
        return redirect("book-all")
    
@method_decorator(signin_required,name="dispatch")
class BooksUpdateView(View):


    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Books.objects.get(id=id)
        form=BooksModelForm(instance=obj)
        return render(request,"book_edit.html",{"form":form})  
    
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Books.objects.get(id=id)
        form=BooksModelForm(request.POST,instance=obj,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"book updated")
            return redirect("book-detail",pk=id)
        else:
            messages.error(request,"failed to update")
            return render(request,"book_edit.html",{"form":form})  
        
class SignupView(View):

    
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})      
    
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            print("saved")
            messages.success(request,"account has been created")
            return render(request,"register.html",{"form":form})
        else:
            print("failed")
            messages.error(request,"failed to create account")
            return render(request,"register.html",{"form":form})
        


class SignInView(View):

    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            user_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            print(user_name,pwd)
            user_obj=authenticate(request,username=user_name,password=pwd)
            if user_obj:
                print("valid")
                login(request,user_obj)
                return redirect("book-all")
        messages.error(request,"invalid")
        return render(request,"login.html",{"form":form})
    
    
@method_decorator(signin_required,name="dispatch")
class SignOutView(View):

    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")

