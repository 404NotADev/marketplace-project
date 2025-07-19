from rest_framework import serializers
from .models import ProductsModel, Comment, Favorite
from rest_framework.serializers import ModelSerializer

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ('user',)

    def validate(self, attrs):
        super().validate(attrs)
        attrs['user'] = self.context['request'].user
        return attrs
    
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['user'] = {
            'id': instance.user.id,
            'email': instance.user.email
        }
        repr['product'] = {
            'id':instance.product.id,
            'title':instance.product.title
        }
        return repr
    
class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:    
        model = ProductsModel
        fields = '__all__'
        read_only_fields = ['salesman']
    
    def create(self, validate_data):
        validate_data['salesman'] = self.context['request'].user
        return super().create(validate_data)
    
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['likes']= instance.likes.all().count()
        repr['comments']= CommentSerializer(instance.comments.all(),many=True).data
        return repr
    
    
class FavoriteSerializer(ModelSerializer):
    class Meta:
        model = Favorite
        exclude = ('user',)

    def validate(self, attrs):
        super().validate(attrs)
        attrs['user'] = self.context['request'].user
        return attrs
    
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['product'] = ProductModelSerializer(instance.product).data
        return repr