from .models import Token


class InvalidToken:
    pass


class TokenMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if 'HTTP_AUTHORIZATION' in request.META:
            header_value = request.META['HTTP_AUTHORIZATION']
            token_key = header_value[6:]
            try:
                token = Token.objects.get(key=token_key)
            except Token.DoesNotExist:
                request.auth = InvalidToken()
            else:
                request.user = token.user
                request.auth = token.key

        response = self.get_response(request)

        return response
