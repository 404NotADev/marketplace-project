from rest_framework import serializers
from .models import ProductsModel

class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:    
        model = ProductsModel
        fields = '__all__'
        read_only_salesman = ['salesman']
    
    def autho_create(self, validate_data):
        validate_data['salesman'] = self.context['request'].user
        return super().create(validate_data)