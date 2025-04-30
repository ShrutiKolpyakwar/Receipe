from django.shortcuts import render, redirect
from .models import Receipe
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Login View
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('receipes')  # Use the name of the receipes view here
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, 'vege/login.html')

# Register User View
def register_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                messages.success(request, "Registration successful! Please log in.")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match")

    return render(request, 'vege/register.html')

# Logout User View
def logout_user(request):
    logout(request)
    return redirect('login')

# Dashboard View (redirecting to receipes)
@login_required(login_url='login')
def dashboard(request):
    return redirect('receipes')

# Receipe Views
@login_required(login_url='login')
def receipes(request):
    if request.method == "POST":
        data = request.POST
        receipe_image = request.FILES.get('receipe_image')
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        
        # Save the new recipe
        Receipe.objects.create(
            receipe_name=receipe_name,
            receipe_description=receipe_description,
            receipe_image=receipe_image,
        )

        return redirect('receipes')  # Redirect using name-based view

    # Fetch all recipes
    queryset = Receipe.objects.all()

    context = {'receipes': queryset}
    return render(request, "vege/receipes.html", context)

# Update Receipe View
@login_required(login_url='login')
def update_receipe(request, id):
    try:
        queryset = Receipe.objects.get(id=id)
    except Receipe.DoesNotExist:
        messages.error(request, "Recipe not found!")
        return redirect('receipes')

    if request.method == "POST":
        data = request.POST
        receipe_image = request.FILES.get('receipe_image')
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        
        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description

        if receipe_image:
            queryset.receipe_image = receipe_image

        queryset.save()
        return redirect('receipes')
        
    context = {'receipe': queryset}
    return render(request, "vege/update_receipes.html", context)

# Delete Receipe View
@login_required(login_url='login')
def delete_receipe(request, id):
    try:
        queryset = Receipe.objects.get(id=id)
        queryset.delete()
        messages.success(request, "Recipe deleted successfully")
    except Receipe.DoesNotExist:
        messages.error(request, "Recipe not found!")
    
    return redirect('receipes')
