from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.hashers import make_password, check_password
from .models import UserManager

def authenticate(username, password):
    user = UserManager.get_user_by_username(username)
    if not user:
        return None
    
    # Check Password:
    hashed_password = user['password']
    if check_password(password, hashed_password):
        return user
    return None

@csrf_protect
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not (username and password):
            return render(request, 'register.html', { 'error' : '入力漏れ' })
        
        try:
            hashed_password = make_password(password)
            UserManager.create_user(username, hashed_password)
            return redirect('hotel_list')
        except Exception as e:
            return render(request, 'register.html', { 'error' : 'ユーザー作成に失敗' })
        
    # if Get request:
    return render(request, 'register.html')

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not (username and password):
            return render(request, 'login.html', { 'error' : '入力漏れ' })
        
        user = authenticate(username, password)
        if user:
            # Able Auth => Save UserInfo in Session
            request.session['user_id'] = user['id']
            request.session['username'] = user['username']
            return redirect('hotel_list')
        else:
            return render(request, 'login.html', { 'error' : 'ユーザー名またはパスワードが正しくありません' })
        
    # if Get request:
    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')