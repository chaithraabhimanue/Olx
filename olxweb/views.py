from django.shortcuts import render,redirect
from django.views.generic import CreateView,TemplateView,FormView,View,UpdateView
from django.contrib.auth.models import User
from api.models import Userprofile
from olxweb.forms import Registrationform,LoginForm,UserProfileForm
from django.urls import reverse_lazy
from django.contrib.auth import login,authenticate,logout
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper
decs=[signin_required,never_cache]

class Signupview(CreateView):
    form_class=Registrationform
    model=User
    template_name="register.html"
    success_url=reverse_lazy("signin")

class LoginView(FormView):
    form_class=LoginForm
    template_name="login.html"

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("home")
            else:
                return render(request,"login.html",{"form":form})
            
@method_decorator(decs,name='dispatch')  
class homeview(TemplateView):
    template_name="index.html"

class Signoutview(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
    
@method_decorator(decs,name="dispatch")
class ProfileCreateView(CreateView):
    model=Userprofile
    form_class=UserProfileForm
    template_name="profile-add.html"
    success_url=reverse_lazy("home")
    
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
        
@method_decorator(decs,name="dispatch")    
class ProfileDetailView(TemplateView):
    template_name="profile-detail.html"


@method_decorator(decs,name="dispatch")
class ProfileUpdateView(UpdateView):
    model=Userprofile
    form_class=UserProfileForm
    template_name="profile-edit.html"
    success_url=reverse_lazy("home")
    pk_url_kwarg="id"