from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Cat
from .serializers import CatSerializer


@api_view(['GET', 'POST'])
def cat_list(request):
    if request.method == 'POST':
        serializer = CatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    cats = Cat.objects.all()
    serializer = CatSerializer(cats, many=True)
    return Response(serializer.data) 


@api_view(['GET','PUT', 'PATCH', 'DELETE'])
def cat_detail(request, pk):
    try:
        cat = Cat.objects.get(id=pk)
    except Cat.DoesNotExist:
        return Response(
            {'error': 'Cat not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = CatSerializer(cat)
        return Response(serializer.data)
    
    elif request.method == 'PUT' or request.method == 'PATCH':
        serializer = CatSerializer(cat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        cat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    