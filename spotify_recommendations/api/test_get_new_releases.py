import unittest
import requests

from spotify_recommendations.api.models import SanitizedNewRelease


class TestNewReleases(unittest.TestCase):
    new_releases = [
            {
                "release_name": "This is Us",
                "artists": "Jimmie Allen, Noah Cyrus",
                "raw_response_id": 10,
                "url": "https://open.spotify.com/album/4lMVogl1pJ3NXl2dMtdjFB"
            },
            {
                "release_name": "Bad Decisions",
                "artists": "The Strokes",
                "raw_response_id": 10,
                "url": "https://open.spotify.com/album/0XhfCV0t2XTMc5TLirBmT1"
            },
        ]

    def setUp(self):
        super().setUp()
        self.clear_new_releases()
        self.insert_new_releases()

    def clear_new_releases(self):
        SanitizedNewRelease.objects.all().delete()

    def insert_new_releases(self):
        for new_release in self.new_releases:
            SanitizedNewRelease(
                artists=new_release['artists'],
                release_name=new_release['release_name'],
                url=new_release['url'],
                raw_response_id=new_release['raw_response_id']
            ).save()

    def test_get_new_releases(self):
        """
        Make sure the app and celery are both running
        """
        response = requests.get('http://localhost:8000/new-releases/')
        loaded_response = response.json()
        results = loaded_response['results']
        self.assertEqual(loaded_response['count'], 2)
        for new_release in self.new_releases:
            self.assertTrue(
                any([new_release['release_name'] == result['release_name'] for result in results])
            )
