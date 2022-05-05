from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Book


@api_view()
def get_all_reviews(request):
    books = Book.objects.all()

    return Response({
        'success': True,
        'data': [
            {
                'id': book.no,
                'user_id': book.user.pk,
                'name': book.name,
                'title': book.title,
                'comment': book.comment
            }
            for book in books
        ]
    })


@api_view()
def get_review(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except:
        return Response({'success': False, 'message': '查無資料'}, status=status.HTTP_404_NOT_FOUND)

    return Response({
        'success': True,
        'data': {
            'id': book.no,
            'user_id': book.user.pk,
            'name': book.name,
            'title': book.title,
            'comment': book.comment
        }
    })


@api_view()
def get_critic_reviews(request):
    data = request.query_params
    user_id = data.get('user_id')

    user_id = str(user_id).strip()
    books = Book.objects.filter(user_id=user_id)

    return Response({
        'success': True,
        'data': [
            {
                'id': book.no,
                'user_id': book.user.pk,
                'name': book.name,
                'title': book.title,
                'comment': book.comment
            }
            for book in books
        ]
    })
