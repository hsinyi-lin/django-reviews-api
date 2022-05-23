from rest_framework import status
from rest_framework.response import Response


def user_login_required(function):
    def wrapper(request, *args, **kw):
        if 'user_id' not in request.session:
            return Response({'success': False, 'message': '請登入'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return function(request, *args, **kw)
    return wrapper