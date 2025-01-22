from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser
from home.models import Blog
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.urls import reverse
# Create your views here.


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact_number = request.POST.get('contact_number')
        profile_image = request.FILES.get('profile_image')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('register')

        user = CustomUser(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            contact_number=contact_number,
            profile_image=profile_image
        )
        user.set_password(password)
        user.save()
        messages.success(request, "Registration successful. You can now log in.")
        return redirect('login')

    return render(request, 'user/Register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                return redirect('dash_home')
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')  # Redirect to the homepage or dashboard
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'user/Login.html')


def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('login')  #


def show_profile(request):
    return render(request,'user/Profile.html')


def update_profile(request):
    if request.method == 'POST':
       
        user = request.user

        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.contact_number = request.POST.get('contact_number', user.contact_number)

        # If there's a new profile image, update it
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']
        
        user.save()

        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('profile') 

    else:
        user = request.user

    return render(request, 'user/updateprofile.html', {'user': user})




def admin_required(user):
    return user.is_superuser

@never_cache
def Dash_home(request):
    post_count = Blog.objects.count()

    return render(request,'dashboard/dash.html',{'post_count':post_count})

# @user_passes_test(admin_required)
def Manage_users(request):
    users = CustomUser.objects.exclude(is_staff=True)
    return render(request,'dashboard/manage_users.html',{'users':users})

def Manage_blog(request):
    blogs = Blog.objects.all()
    return render(request,'dashboard/dash_blog.html',{'blogs':blogs})

def admin_Logout(request):
        logout(request)
        return redirect("login")
    

def block_user(request, user_id):
    print('Entering block user view?????????')

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        print('User not found')
        return render(request, 'dashboard/manage_users.html', {"error": "User not found"})

    # Get the action from the request (e.g., block or unblock)
    action = request.GET.get('action', 'block')  # Default to 'block'

    if action == 'block':
        if user.is_active:
            user.is_active = False
            user.save()
            print(f'User {user.username} has been blocked.')

            subject = "Your Account is Blocked"
            message = f'Dear {user.username},\n\nYour account has been blocked by the admin. Please contact support for more details.'
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

    elif action == 'unblock':
        if not user.is_active:
            user.is_active = True
            user.save()
            print(f'User {user.username} has been unblocked.')

            subject = "Your Account is UnBlocked"
            message = f"Dear {user.username},\n\nYour account has been Unblocked by the admin. Please contact support for more details."
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


    users = CustomUser.objects.filter(is_superuser=False).order_by("id")
    context = {"users": users}

    return render(request, 'dashboard/manage_users.html', context)


def Block_blog(request, blog_id, action):
    blog = Blog.objects.get(id=blog_id)

    if action == 'block':
        if blog.is_active:
            blog.is_active = False
            blog.save()
            print(f'blog {blog.title} is blocked')

            subject = "Your Post is Blocked"
            message = f"Dear {blog.author},\n\nYour post titled '{blog.title}' has been blocked by the admin. Please contact support for more details."
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [blog.author_email])

            return redirect('manage_blogs')
    elif action == 'unblock':
        if not blog.is_active:
            blog.is_active = True
            blog.save()
            print(f'blog {blog.title} is unblocked')

            subject = "Your Post is UnBlocked"
            message = f"Dear {blog.author},\n\nYour post titled '{blog.title}' has been blocked by the admin. Please contact support for more details."
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [blog.author_email])

            return redirect('manage_blogs')


def Forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the email exists in the database
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, 'Email address not found.')
            return render(request, 'user/forgot_password.html', {'email': email})

        # Validate passwords
        if password != confirm_password:
            messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, 'user/forgot_password.html', {'email': email})

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'user/forgot_password.html', {'email': email})

        # Update the user's password securely
        user.set_password(password)
        user.save()
        messages.success(request, 'Your password has been reset successfully. You can now log in.')
        return redirect('login')  # Redirect to the login page

    return render(request, 'user/forgot_password.html')


