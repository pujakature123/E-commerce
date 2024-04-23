
from django.shortcuts import redirect


def auth_middleware(get_response):
    def middleware(request):
        return_url = request.META['PATH_INFO']
        print('return url', return_url)
        if not request.session.get('customer_id'):
            return redirect('login')
        response = get_response(request)
        return response
    return middleware
