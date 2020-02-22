import base64
import uuid
from urllib.parse import urlencode

from django.contrib.auth.models import User, Group
import requests
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect

from spotify_recommendations.api.serializers import UserSerializer, GroupSerializer
from spotify_recommendations.config import get_config

state_key = 'spotify_auth_state'
redirect_uri = get_config('redirect_uri')
client_id = get_config('client_id')
client_secret = get_config('client_secret')


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@api_view(http_method_names=['GET'])
def login(request):
    scope = ''
    state = uuid.uuid4()
    query_string = dict(
        response_type='code',
        client_id=client_id,
        scope=scope,
        redirect_uri=redirect_uri,
        state=state
    )
    query_string = urlencode(query_string)
    url = 'https://accounts.spotify.com/authorize?' + query_string
    response = redirect(url)
    response.set_cookie(state_key, state)
    return response


@api_view(http_method_names=['GET'])
def callback(request):
    state = request.query_params.get('state')
    code = request.query_params.get('code')
    stored_state = request.COOKIES.get(state_key)

    if state is None or state != stored_state:
        return Response('', status=status.HTTP_401_UNAUTHORIZED)

    form_data = {
        'code': code,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(bytes(client_id + ':' + client_secret, 'utf-8')).decode('utf-8'),
        'content-type': 'application/x-www-form-urlencoded'
    }
    token_response = requests.post('https://accounts.spotify.com/api/token', data=form_data, headers=headers)
    if token_response.status_code == 200:
        body = token_response.json()
        access_token = body['access_token']
        refresh_token = body['refresh_token']
        query_string = urlencode({
            'access_token': access_token,
            'refresh_token': refresh_token
        })
        response = redirect('{}/#{}'.format(get_config('ui_host'), query_string))
        response.delete_cookie(state_key)
        return response
    return Response('test')


def refresh_token(request):
    pass
