from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt  # Importa csrf_exempt aquí
import random
import string
import requests
import os

# Clase personalizada para manejar el error de coincidencia de estado
class MismatchingStateError(Exception):
    pass

# Configuración de Auth0 (variables de entorno)
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
AUTH0_CALLBACK_URL = os.getenv('AUTH0_CALLBACK_URL')

def login(request):
    # Genera un valor aleatorio para 'state' y lo almacena en la sesión
    state = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    request.session['auth0_state'] = state
    # Redirige al usuario a la página de login de Auth0 con el estado generado
    return redirect(f'https://{AUTH0_DOMAIN}/authorize?response_type=code&client_id={AUTH0_CLIENT_ID}&redirect_uri={AUTH0_CALLBACK_URL}&state={state}')

@csrf_exempt  # Aplica el decorador aquí para desactivar CSRF en esta vista
def callback(request):
    # Recupera el estado almacenado y el recibido desde la URL de Auth0
    stored_state = request.session.get('auth0_state')
    received_state = request.GET.get('state')

    # Debug: Imprime los valores de los estados almacenado y recibido
    print(f"Estado almacenado: {stored_state}, Estado recibido: {received_state}")

    # Elimina el estado de la sesión solo si existe
    if stored_state:
        del request.session['auth0_state']

    # Obtiene el código de autorización desde la URL de Auth0
    code = request.GET.get('code')

    # Configura la URL y los datos para la solicitud de token a Auth0
    token_url = f'https://{AUTH0_DOMAIN}/oauth/token'
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': AUTH0_CLIENT_ID,
        'client_secret': AUTH0_CLIENT_SECRET,
        'code': code,
        'redirect_uri': AUTH0_CALLBACK_URL,
    }

    # Realiza la solicitud POST a Auth0 para obtener el token
    token_response = requests.post(token_url, json=token_data)

    # Si hay un error en la solicitud del token, devuelve un mensaje de error
    if token_response.status_code != 200:
        return HttpResponse("Error al obtener el token", status=token_response.status_code)

    # Extrae los tokens de la respuesta
    tokens = token_response.json()
    access_token = tokens.get('access_token')
    id_token = tokens.get('id_token')

    # Almacena los tokens en la sesión del usuario
    request.session['access_token'] = access_token
    request.session['id_token'] = id_token

    # Muestra una página de éxito con los tokens obtenidos
    return render(request, 'dashboard.html', {'tokens': tokens})

    # Recupera el estado almacenado y el recibido desde la URL de Auth0
    stored_state = request.session.get('auth0_state')
    received_state = request.GET.get('state')

    # Debug: Imprime los valores de los estados almacenado y recibido
    print(f"Estado almacenado: {stored_state}, Estado recibido: {received_state}")

    # Elimina el estado de la sesión una vez verificado
    del request.session['auth0_state']

    # Obtiene el código de autorización desde la URL de Auth0
    code = request.GET.get('code')

    # Configura la URL y los datos para la solicitud de token a Auth0
    token_url = f'https://{AUTH0_DOMAIN}/oauth/token'
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': AUTH0_CLIENT_ID,
        'client_secret': AUTH0_CLIENT_SECRET,
        'code': code,
        'redirect_uri': AUTH0_CALLBACK_URL,
    }

    # Realiza la solicitud POST a Auth0 para obtener el token
    token_response = requests.post(token_url, json=token_data)

    # Si hay un error en la solicitud del token, devuelve un mensaje de error
    if token_response.status_code != 200:
        return HttpResponse("Error al obtener el token", status=token_response.status_code)

    # Extrae los tokens de la respuesta
    tokens = token_response.json()
    access_token = tokens.get('access_token')
    id_token = tokens.get('id_token')

    # Almacena los tokens en la sesión del usuario
    request.session['access_token'] = access_token
    request.session['id_token'] = id_token

    # Muestra una página de éxito con los tokens obtenidos
    return render(request, 'success.html', {'tokens': tokens})

    # Recupera el estado almacenado y el recibido desde la URL de Auth0
    stored_state = request.session.get('auth0_state')
    received_state = request.GET.get('state')

    # Debug: Imprime los valores de los estados almacenado y recibido
    print(f"Estado almacenado: {stored_state}, Estado recibido: {received_state}")

    # Verifica si el estado recibido coincide con el estado almacenado
    if stored_state != received_state:
        raise MismatchingStateError("El estado no coincide, posible ataque CSRF.")

    # Elimina el estado de la sesión una vez verificado
    del request.session['auth0_state']

    # Obtiene el código de autorización desde la URL de Auth0
    code = request.GET.get('code')

    # Configura la URL y los datos para la solicitud de token a Auth0
    token_url = f'https://{AUTH0_DOMAIN}/oauth/token'
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': AUTH0_CLIENT_ID,
        'client_secret': AUTH0_CLIENT_SECRET,
        'code': code,
        'redirect_uri': AUTH0_CALLBACK_URL,
    }

    # Realiza la solicitud POST a Auth0 para obtener el token
    token_response = requests.post(token_url, json=token_data)

    # Si hay un error en la solicitud del token, devuelve un mensaje de error
    if token_response.status_code != 200:
        return HttpResponse("Error al obtener el token", status=token_response.status_code)

    # Extrae los tokens de la respuesta
    tokens = token_response.json()
    access_token = tokens.get('access_token')
    id_token = tokens.get('id_token')

    # Almacena los tokens en la sesión del usuario
    request.session['access_token'] = access_token
    request.session['id_token'] = id_token

    # Muestra una página de éxito con los tokens obtenidos
    return render(request, 'success.html', {'tokens': tokens})

def logout(request):
    try:
        request.session.flush()  # Limpia la sesión
        # Redirige al usuario a la página de logout de Auth0
        return redirect(f'https://{AUTH0_DOMAIN}/v2/logout?client_id={AUTH0_CLIENT_ID}&returnTo=http://localhost:8000/')
    except Exception as e:
        return HttpResponse(f"Ocurrió un error al cerrar sesión: {str(e)}")


def dashboard(request):
    # Recupera el usuario de la sesión
    user = request.session.get('user')  # Asegúrate de que esto se está almacenando correctamente en el paso anterior
    if not user:
        return redirect('home')  # Redirige si no hay un usuario autenticado
    return render(request, 'dashboard.html', {'user': user})  # Pasa la información del usuario al contexto


def home(request):
    # Renderiza la página de inicio
    return render(request, 'home.html')
