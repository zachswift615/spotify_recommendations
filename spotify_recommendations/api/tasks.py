# Create your tasks here
from __future__ import absolute_import, unicode_literals

import json

import requests
from celery import shared_task, Celery

from spotify_recommendations.api.models import RawNewReleases, SanitizedNewRelease


@shared_task
def get_new_releases_task(token):
    headers = {
        'Authorization': "Bearer {}".format(token)
    }
    new_releases_response = requests.get('https://api.spotify.com/v1/browse/new-releases', headers=headers)
    if new_releases_response.status_code == 200:
        new_releases = new_releases_response.json()
    else:
        raise Exception('Failed to get new releases')
    new_release = RawNewReleases(response=json.dumps(new_releases))
    new_release.save()
    return new_release.id


@shared_task
def transform_new_releases(raw_new_releases_id):
    raw_new_releases = RawNewReleases.objects.get(pk=raw_new_releases_id)
    new_releases = json.loads(raw_new_releases.response)
    for album in new_releases['albums']['items']:
        artists = ', '.join([artist['name'] for artist in album['artists']])
        SanitizedNewRelease(artists=artists, raw_response=raw_new_releases, release_name=album['name'], url=album['external_urls']['spotify']).save()


