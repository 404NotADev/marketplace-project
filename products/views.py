from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response    
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .permissions import IsOwner
from .models import Comment, Like, Favorite, ProductsModel
from .serializer import ProductModelSerializer,CommentSerializer, FavoriteSerializer


class ProductViewSet(ModelViewSet):
    queryset = ProductsModel.objects.all()
    serializer_class = ProductModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]

    def perform_create(self, serializer):
        serializer.save(salesman=self.request.user)



class CommentModelViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

class FavoriteModelViewSet(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

@api_view(['POST'])
def toogle_like(request, id):
    user = request.user
    if not user.is_authenticated:
        return Response(status=401)
    product = get_object_or_404(ProductsModel, id = id)
    if Like.objects.filter(user=user, product=product). exists():
        Like.objects.filter(user=user ,product=product).delete()
    else:
        Like.objects.create(user=user ,product=product)
    return Response(status=201)
