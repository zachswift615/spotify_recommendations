import base64
import uuid
from pprint import pprint
from urllib.parse import urlencode

from django.contrib.auth.models import User, Group
import requests
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect

from spotify_recommendations.api.models import Token, SanitizedNewRelease
from spotify_recommendations.api.serializers import UserSerializer, GroupSerializer, NewReleaseSerializer
from spotify_recommendations.api.tasks import get_new_releases_task, transform_new_releases
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


class NewReleasesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = SanitizedNewRelease.objects.all()
    serializer_class = NewReleaseSerializer


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
        Token.set_access_token(access_token)
        refresh_token = body['refresh_token']
        query_string = urlencode({
            'access_token': access_token,
            'refresh_token': refresh_token
        })
        response = redirect('{}/#{}'.format(get_config('ui_host'), query_string))
        response.delete_cookie(state_key)
        return response
    return Response('', status=status.HTTP_401_UNAUTHORIZED)


@api_view(http_method_names=['GET'])
def get_new_releases(request):
    token = Token.get_access_token()
    if token is None:
        return Response('', status=status.HTTP_401_UNAUTHORIZED)
    get_new_releases_task.apply_async((token.token,), link=transform_new_releases.s())
    return Response('test')


def is_low_speechiness(track_id):
    try:
        audio_features = make_spotify_request('/audio-features/{track_id}'.format(track_id=track_id))
    except Exception as e:
        return True
    speechiness = audio_features['speechiness']
    return speechiness < 0.5


def make_spotify_request(api_path, query_params=None):
    token = Token.get_access_token()
    if token is None:
        return Response('', status=status.HTTP_401_UNAUTHORIZED)
    headers = {
        'Authorization': "Bearer {}".format(token.token)
    }
    new_releases_response = requests.get(
        'https://api.spotify.com/v1{}'.format(api_path), headers=headers)
    if new_releases_response.status_code == 200:
        return new_releases_response.json()
    else:
        print(new_releases_response.text)
        print(new_releases_response.status_code)
        raise Exception('Request Failed')


@api_view(http_method_names=['GET'])
def get_new_music_friday_no_rap(request):
    new_releases = make_spotify_request('/playlists/37i9dQZF1DX4JAvHpjipBk?si=7CVrRBORReCRBgWcrW5a-g/tracks')
    no_rap = []
    for track in new_releases['tracks']['items']:
        inner_track = track.get('track')
        if inner_track:
            track_id = inner_track.get('id')
            if is_low_speechiness(track_id):
                no_rap.append(inner_track)
    return Response(no_rap)
