from http.client import responses
import re
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class checkToken(MiddlewareMixin):
    def process_request(self, request):
        print(request.path_info)
        if request.path_info.startswith('/Media/') or request.path_info.startswith('/static/') or request.path_info.startswith('/admin/'):
            return None
        exempt_paths = ['/Token', '/Token/']
        dynamic_path_patterns = [
            r'^/Order/\w+/$',
            r'^/Order/\d+/submitorder/$',
            r'^/Order/\d+/curretorder/$',
            r'^/customercancleitem/\d+/\d+/\d+$',
            r'^/Srequest/\d+/\d+/\d+$',
            r'^/customercancleitem/\d+/\d+/\d+/$',
            r'^/Srequest/\d+/\d+/\d+$/',
            r'^/Order/\w+$',
            r'^/Order/\d+/submitorder$',
            r'^/Order/\d+/curretorder$',
        ]

        if request.path_info in exempt_paths:
            return None


        for pattern in dynamic_path_patterns:
            if re.match(pattern, request.path_info):
                return None

        # Check for Token in session
        token = request.session.get('Token')
        if token:
           # print('Token yse')
            return None
        else:
            print('No token')
            print(request.path_info)
            return redirect('/Token')

    def process_response(self, request, response):
        return response