from rest_framework.viewsets import ModelViewSet
from .models import ProductsModel
from .serializer import ProductModelSerializer

class ProductViewSet(ModelViewSet):
    queryset = ProductsModel.objects.all()
    serializer_class = ProductModelSerializer