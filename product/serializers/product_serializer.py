from rest_framework import serializers
from product.models.category import Category
from product.models.product import Product
from product.serializers.category_serializer import CategorySerializer

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=True)
    categories_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True, many=True
    )

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'price',
            'active',
            'category',
            'categories_id'
        ]

    def create(self, validated_data):
        # Remove os IDs das categorias do validated_data
        category_data = validated_data.pop('categories_id', [])

        # Cria o produto sem as categorias
        product = Product.objects.create(**validated_data)

        # Adiciona as categorias ao produto
        product.category.set(category_data)

        return product