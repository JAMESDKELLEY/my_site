from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.contrib import messages

def index(request):
    return render(request, 'main/index.html')

def register(request):
    is_valid = User.objects.validate_user(request.POST)
    
    if is_valid[0]:
        user = User.objects.create(
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            password = bcrypt.hashpw(request.POST.get('password').encode(), bcrypt.gensalt()),
        )
        request.session['user_id'] = user.id
        return redirect('/success')
    else:
        for error in is_valid[1]:
            messages.error(request, error)
        return redirect('/')

def login(request):
    if request.method == 'POST':
        login = User.objects.login_user(request.POST)
        if login[0]:
            request.session['user_id']=login[1].id
            return redirect('/success')
        else:
            messages.error(request, 'Invalid Login Information')
        return redirect('/')

def success(request):
    favorite = []
    fav_list = Favorite.objects.filter(user= request.session['user_id'])
    for fav in fav_list:
        favorite.append(fav.quote.id)
        favorite.append(request.session['user_id'])
    
    context = {
        'current_user' : User.objects.get(id=request.session['user_id']),
        'quotes' : Quote.objects.exclude(id__in=favorite),
        'favorites' : Favorite.objects.filter(user=request.session['user_id']),
        'user' : User.objects.exclude(id=request.session['user_id'])
    }
    return render(request, 'main/success.html', context)

def submit(request):
    if len(request.POST.get('quoted_by')) < 3:
        messages.error(request, 'Quoted by should be more than 3 characters')
    elif len(request.POST.get('message')) < 10:
        messages.error(request, 'Message should be more than 10 characters')
    else:
        Quote.objects.create(
            user = User.objects.get(id=request.session['user_id']),
            author= request.POST.get('quoted_by'),
            quote= request.POST.get('message'),
        )
    return redirect('/success')

def my_list(request, id):
    Favorite.objects.create(
        user = User.objects.get(id=request.session['user_id']),
        quote = Quote.objects.get(id=id)
    )
    return redirect('/success')

def remove(request, id):
    Favorite.objects.filter(quote__id = id).delete()
    return redirect('/success')

def user_profile(request, id):
    context = {
        'user': Quote.objects.filter(user = id).first(),
        'quotes': Quote.objects.filter(user = id),
        'count': len(Quote.objects.filter(user = id))

    }
    return render(request, 'main/profile.html', context)

def dashboard(request):
    return redirect('/success')

def logout(request):
    request.session.clear()
    return redirect('/')







