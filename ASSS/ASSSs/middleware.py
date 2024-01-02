from django.utils.deprecation import MiddlewareMixin


class OAuthMiddleware(MiddlewareMixin):


    def process_request(self, request):
        print("do")
        if request.path_info == '/o/token/' and request.method == 'POST':
            request.POST = request.POST.copy()
            request.POST['client_id'] = 'cN1kSkRY92F0i41vOzIeNrtRHhHK3axzq5rOS6yA'
            request.POST['client_secret'] = 'MyADr80ht4KhA1kRwBa4jKoQzUFlSGuVVyUdc4Pe3BdRVQVx45kkQOAWBojYcRj4Yfn0pmxLFuXwYIHrqvrQmKTFkGDIBfg03vzEWmNW2NxZHgURXDYBEXvcmgffp1fw'
            request.POST['grant_type'] = 'password'
