import base64
import uuid
from collections import OrderedDict
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
print(redirect_uri)
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
    """
    app.get('/login', function(req, res) {

  var state = generateRandomString(16);
  res.cookie(stateKey, state);

  // your application requests authorization
  var scope = 'user-read-private user-read-email user-read-playback-state';
  res.redirect('https://accounts.spotify.com/authorize?' +
    querystring.stringify({
      response_type: 'code',
      client_id: client_id,
      scope: scope,
      redirect_uri: redirect_uri,
      state: state
    }));
});
    :return:
    """
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
    """
    app.get('/callback', function(req, res) {

  // your application requests refresh and access tokens
  // after checking the state parameter

  var code = req.query.code || null;
  var state = req.query.state || null;
  var storedState = req.cookies ? req.cookies[stateKey] : null;

  if (state === null || state !== storedState) {
    res.redirect('/#' +
      querystring.stringify({
        error: 'state_mismatch'
      }));
  } else {
    res.clearCookie(stateKey);
    var authOptions = {
      url: 'https://accounts.spotify.com/api/token',
      form: {
        code: code,
        redirect_uri: redirect_uri,
        grant_type: 'authorization_code'
      },
      headers: {
        'Authorization': 'Basic ' + (new Buffer(client_id + ':' + client_secret).toString('base64'))
      },
      json: true
    };

    request.post(authOptions, function(error, response, body) {
      if (!error && response.statusCode === 200) {

        var access_token = body.access_token,
            refresh_token = body.refresh_token;

        var options = {
          url: 'https://api.spotify.com/v1/me',
          headers: { 'Authorization': 'Bearer ' + access_token },
          json: true
        };

        // use the access token to access the Spotify Web API
        request.get(options, function(error, response, body) {
          console.log(body);
        });

        // we can also pass the token to the browser to make requests from there
        res.redirect('http://localhost:3000/#' +
          querystring.stringify({
            access_token: access_token,
            refresh_token: refresh_token
          }));
      } else {
        res.redirect('/#' +
          querystring.stringify({
            error: 'invalid_token'
          }));
      }
    });
  }
});
    :param request:
    :return:
    """


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
    """
    app.get('/refresh_token', function(req, res) {

  // requesting access token from refresh token
  var refresh_token = req.query.refresh_token;
  var authOptions = {
    url: 'https://accounts.spotify.com/api/token',
    headers: { 'Authorization': 'Basic ' + (new Buffer(client_id + ':' + client_secret).toString('base64')) },
    form: {
      grant_type: 'refresh_token',
      refresh_token: refresh_token
    },
    json: true
  };

  request.post(authOptions, function(error, response, body) {
    if (!error && response.statusCode === 200) {
      var access_token = body.access_token;
      res.send({
        'access_token': access_token
      });
    }
  });
});
    :param request:
    :return:
    """
    pass
