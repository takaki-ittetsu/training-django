from functools import wraps
from django.shortcuts import redirect

def login_required(view_func):
    """
    ログイン状態を確認するデコレータ
    セッションに 'user_id' が無い場合はログインページへリダイレクト
    """

    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    
    return wrapped_view