from django.shortcuts import render, HttpResponse, redirect
from .models import Contact, UserProfile
from django.contrib import messages
from blog.models import Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# from .models import Account as User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    allpost = Post.objects.all()
    context = {'allpost':allpost}
    return render(request, 'home/home.html',context)

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    # messages.error(request, 'Welcome to contact.')
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request,"Please fill the form correctly.")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request,"Your message has been sent successfully")
    return render(request, 'home/contact.html')

def search(request):
    query = request.GET['query']
    if len(query)>78:
        allpost = []
        if len(allpost) == 0:
            messages.error(request,"No result found.You search for very large query.Please search small query.")
    else:
        # __icontains used for filter query set.
        allpostTitle = Post.objects.filter(title__icontains=query)
        allpostContent = Post.objects.filter(content__icontains=query)
        allpostAuthor = Post.objects.filter(author__icontains=query)
        allpost = allpostTitle.union(allpostContent, allpostAuthor)

    context = {'allpost':allpost, 'query':query}
    return render(request, 'home/search.html', context)

def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if request.FILES['userprofile']:
            myuserpic = request.FILES['userprofile']

        users = User.objects.all()
        # Check errorneous inputs
        if len(username) > 25:
            messages.error(request,"Your username must be under 15 characters.")
            return redirect("home")

        for user in users:
            if username == user.username:
                messages.error(request,"Your username must be unique.")
                return redirect("home")
        
        if " " in username:
            messages.error(request,"username must must not contain any spaces.")
            return redirect("home")
        
        if not(all(char.isalpha() or char.isspace() for char in fname)):
            messages.error(request,"First name must be only Letters.")
            return redirect("home")
        
        if not(all(char.isalpha() or char.isspace() for char in lname)):
            messages.error(request,"Last name must be only Letters.")
            return redirect("home")
        
        if pass1 != pass2:
            messages.error(request,"Passwords do not match")
            return redirect("home")
        


        # Create the User
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        myuserprofile = UserProfile.objects.create(user=myuser, avatar=myuserpic)
        myuserprofile.save()
        messages.success(request,"Your account has been successfully created.")
        return redirect("home")

    else:
        return HttpResponse("404 - Not Found")

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']
        user = authenticate(username=loginusername, password=loginpass)
        if user is not None:
            login(request, user)
            messages.success(request,"Logged in successfully")
            return redirect('home')
        else:
            messages.error(request,"Invalid credentials. Please try agian")
            return redirect('home')
    return HttpResponse("404 - Not Found")

def handleLogout(request):
    logout(request)
    messages.success(request,"Logged out successfully")
    return redirect('home')

@login_required()
def editProfile(request, pk):
    user = User.objects.get(pk=pk)
    context = {'user':user}
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname= request.POST['lname']
        email = request.POST['email']
        oldpass = request.POST['Oldpass']
        pswd = request.POST['pswd']
        c_pswd = request.POST['c_pswd']
        success = user.check_password(oldpass)
        if not success:
            messages.error(request,"Old password did not match.")
            return render(request,'home/editProfile.html',context)
        if pswd == c_pswd:
            if len(pswd) < 1:
                pass
            else:
                messages.success(request,"Password change succesfully.")
                user.set_password(pswd)
                user.save()
                update_session_auth_hash(request, user)

        myuser = User.objects.filter(pk=pk).update(username=username,first_name=fname,last_name=lname,email=email)
        messages.success(request,"Your profile hase been updated successfully.")
        return redirect("home")   
    return render(request,'home/editProfile.html',context)

@login_required()
def deleteProfile(request, pk):
    user = User.objects.get(pk=pk)
    user.delete()
    messages.success(request,"Your account has been deleted successfully.")
    return redirect("home")


def handleforget(request):
    if request.method == 'POST':
        username = request.POST['forgetusername']
        fname = request.POST['forgetfname']
        email = request.POST['forgetemail']
        user = User.objects.get(username=username)
        reset = True
        if username == user.username and fname == user.first_name and email == user.email:
            return render(request,"home/password_reset.html",{'user':user, 'reset':reset})
        else:
            messages.error(request,"Invalid details. Can't reset your password.")
            return redirect("home")
    else:
        return HttpResponse("404 - page not found")

def handlereset(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        pass1 = request.POST['pswd']
        pass2 = request.POST['c_pswd']
        if pass1 == pass2:
            user.set_password(pass1)
            user.save()
            messages.success(request,"Password reset successfully. Please login")
            return redirect("home")
        else:
            messages.error(request,"Password and confirm password did not match.")
            return redirect("home")