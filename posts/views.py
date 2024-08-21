from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
# Create your views here.
def home(request):
    return render(request,'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request,'signup.html',{
            'form':UserCreationForm
        })
    else:
        print(request.POST)
        if request.POST['password1'] == request.POST['password2']:
            try:
                #Guardar Usuario con un modelo Django si las password coinciden
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                return HttpResponse('Usuario creado')
            except:
                return HttpResponse('El usuario ya existe') 
        return HttpResponse('Las contraseñas no coinciden')