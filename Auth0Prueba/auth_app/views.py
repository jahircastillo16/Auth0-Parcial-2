from django.shortcuts import redirect, render
from django.conf import settings
from django.urls import reverse
from authlib.integrations.django_client import OAuth

oauth = OAuth()
oauth.register(
    'auth0',
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        'scope': 'openid profile email',
    },
    server_metadata_url=f'https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration',
)

def login(request):
    return oauth.auth0.authorize_redirect(request, redirect_uri=settings.AUTH0_CALLBACK_URL)

def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session['user'] = token
    return redirect('dashboard')

def logout(request):
    request.session.clear()
    return_url = request.build_absolute_uri(reverse('home'))
    return redirect(
        f'https://{settings.AUTH0_DOMAIN}/v2/logout?'
        f'client_id={settings.AUTH0_CLIENT_ID}&returnTo={return_url}'
    )

def dashboard(request):
    user = request.session.get('user')
    if not user:
        return redirect('home')
    return render(request, 'dashboard.html', {'user': user})

def home(request):
    return render(request, 'home.html')
