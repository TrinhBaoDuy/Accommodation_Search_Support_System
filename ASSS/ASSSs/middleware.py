from django.utils.deprecation import MiddlewareMixin


class OAuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # print("do")
        if request.path_info == '/o/token/' and request.method == 'POST':
            request.POST = request.POST.copy()
            request.POST['client_id'] = 'UXTi69lodcxqmENTZITNy3e0EHIJ64UzUqnb9Hu4'
            request.POST['client_secret'] = 'oIulUY0kY7FIYDIjCmzUlKi3u6lHhCmdVYAJxLaEzJpmX3hnZH51uyhTeMbhmRIJk0fUPFMiUggebg2JkxwFviYBPK9bejcaxlyK67GImarvBjGUCeD5rrL9O0EnrH38'
            request.POST['grant_type'] = 'password'
