from django.db import models


class Token(models.Model):
    access = 'access'
    refresh = 'refresh'
    TOKEN_TYPE_CHOICES = [
        (access, 'Access Token',),
        (refresh, 'Refresh Token',)
    ]
    token = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now=True)
    token_type = models.CharField(max_length=25, choices=TOKEN_TYPE_CHOICES, default=access)

    @staticmethod
    def get_access_token():
        return Token.objects.filter(token_type='access').first()

    @staticmethod
    def set_access_token(new_token):
        token = Token.get_access_token()
        if token is not None:
            token.token = new_token
            token.save()
        else:
            token = Token(token=new_token, token_type=Token.access).save()
        return token


class RawNewReleases(models.Model):
    response = models.TextField()


class SanitizedNewRelease(models.Model):
    raw_response = models.ForeignKey(RawNewReleases, on_delete=models.CASCADE)
    release_name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    artists = models.CharField(max_length=255)
