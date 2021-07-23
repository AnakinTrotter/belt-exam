from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from wish_app.models import *
from django.contrib import messages
import datetime
import bcrypt

# Create your views here.

def index(request):
    if request.method == 'POST':
        if request.POST['pressed'] == 'register':
            errors = User.objects.basic_validator(request.POST)
            user = User.objects.filter(email=request.POST['email'])
            if user:
                errors[request] = 'Email already taken.'
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/')
            request.session['fname'] = request.POST['fname']
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() 
            user = User.objects.create(fname=request.POST['fname'], lname=request.POST['lname'], email=request.POST['email'], password=pw_hash)
            request.session['user_id'] = user.id
        elif request.POST['pressed'] == 'login':
            errors = {}
            user = User.objects.filter(email=request.POST['email'])
            if not user:
                errors[request] = 'Incorrect email or password.'
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/')
            else:
                logged_user = user[0]
                if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                    request.session['fname'] = logged_user.fname
                    request.session['user_id'] = logged_user.id
                else:
                    errors[request] = 'Incorrect email or password.'
                for key, value in errors.items():
                    messages.error(request, value)
                    return redirect('/')
        return redirect('/wishes')
    else:
        return render(request, 'index.html')

def wishes(request):
    if 'user_id' not in request.session:
        return redirect('/')
    granted = []
    ungranted = []
    user = User.objects.get(id=request.session['user_id'])
    for wish in Wish.objects.all():
        wish_data = {
            'id': wish.id,
            'title': wish.title,
            'date_added': wish.created_at.strftime('%B %d %Y'),
        }
        if wish.granted:
            wish_data['wisher'] = wish.uploaded_by.fname
            wish_data['date_granted'] = wish.updated_at.strftime('%B %d %Y')
            wish_data['likes'] = len(wish.users_who_like.all())
            if wish not in user.wishes_uploaded.all():
                wish_data['can_like'] = True
            granted.insert(0, wish_data)
        elif wish in user.wishes_uploaded.all():
            ungranted.insert(0, wish_data)
    request.session['granted'] = granted
    request.session['ungranted'] = ungranted
    return render(request, 'wishes.html')

def logout(request):
    if 'user_id' not in request.session:
        return redirect('/')
    request.session.flush()
    return redirect('/')

def new_wish(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == 'POST':
        errors = Wish.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/wishes/new')
        title = request.POST['title']
        desc = request.POST['desc']
        user = User.objects.get(id=request.session['user_id'])
        Wish.objects.create(title=title, desc=desc, uploaded_by=user)
        return redirect('/wishes')
    return render(request, 'new_wish.html')

def grant_wish(request, wish_id):
    if 'user_id' not in request.session:
        return redirect('/')
    wish = Wish.objects.get(id=wish_id)
    wish.granted = True
    wish.save()
    return redirect('/wishes')

def remove_wish(request, wish_id):
    if 'user_id' not in request.session:
        return redirect('/')
    wish = Wish.objects.get(id=wish_id)
    user = User.objects.get(id=request.session['user_id'])
    if wish not in user.wishes_uploaded.all():
        return redirect('/')
    wish.delete()
    return redirect('/wishes')

def edit_wish(request, wish_id):
    if 'user_id' not in request.session:
        return redirect('/')
    wish = Wish.objects.get(id=wish_id)
    if request.method == 'POST':
        errors = Wish.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/wishes/edit/' + str(wish_id))
        wish.title = request.POST['title']
        wish.desc = request.POST['desc']
        wish.save()
        return redirect('/wishes')
    user = User.objects.get(id=request.session['user_id'])
    if wish not in user.wishes_uploaded.all():
        return redirect('/')
    content = {
        "id": wish.id,
        "title": wish.title,
        "desc": wish.desc,
    }
    request.session['wish'] = content
    return render(request, 'edit_wish.html')

def like_wish(request, wish_id):
    if 'user_id' not in request.session:
        return redirect('/')
    wish = Wish.objects.get(id=wish_id)
    user = User.objects.get(id=request.session['user_id'])
    if wish in user.wishes_uploaded.all():
        return redirect('/')
    wish.users_who_like.add(user)
    return redirect('/wishes')

def stats(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    request.session['total_granted'] = len(Wish.objects.filter(granted=True))
    request.session['your_granted'] = 0
    request.session['your_pending'] = 0
    for wish in Wish.objects.filter(uploaded_by=user):
        if wish.granted:
            request.session['your_granted'] += 1
        else:
            request.session['your_pending'] += 1
    return render(request, 'stats.html')