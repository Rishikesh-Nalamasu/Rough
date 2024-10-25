from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from core.models import Profile
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User,auth
from django.contrib import messages # used to make messages, when the user sign'sUP with the registered email, then need to show invalid error
# Create your views here.

@login_required(login_url='signin')

def publish(request):
    return render(request,'publish.html')




def signup(request):

    if request.method == 'POST':
        username = request.POST['username']  # very imp here ['username'] was the name in the html of name element
        #print(username)  for checking the entered username was printing ?
        email = request.POST['email'] 
        
        password = request.POST['password'] 
        department = request.POST['department']
        #print(username,email,department,password) worked
        if User.objects.filter(email = email).exists():
            messages.info(request,"Email already taken")
            return redirect('signup')
        else:
            user = User.objects.create_user(username=username,email=email,password=password)
            user.save()
            #log user in and redirect to setting page(where we upload profic pic)

            #create a profile obj for the new user
            user_model = User.objects.get(username = username) #CHANGE TO ,email .if email = email , This line will fetch the user instance based on the provided email address instead of the username. It's a useful approach, especially if you consider email addresses to be more unique and reliable identifiers than usernames.
            new_profile = Profile.objects.create(user = user_model,id_user=user_model.id,branch=department)
            new_profile.save()
            return redirect('signin')
    else:
        return render(request,'signup.html')
  

def signin(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            user = User.objects.get(email=email)
            username = user.username
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Invalid credentials')
                return redirect('signin')
        except User.DoesNotExist:
            messages.info(request, 'Email not registered')
            return redirect('signin')
    else:
        return render(request, 'signin.html')
  

def logout(request):
    auth.logout(request)
    return redirect('signin')

