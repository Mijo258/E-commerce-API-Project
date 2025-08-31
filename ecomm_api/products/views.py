from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters import rest_framework as filters
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

class ProductFilter(filters.FilterSet):
    # Allow filtering by price range 
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte') # gte = greater than or equal to
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte') # lte = less than or equal to
    # Allow searching by name 
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Product
        # Define exact match filters here
        fields = ['category', 'name', 'min_price', 'max_price']

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing products.
    """
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = ProductFilter
    search_fields = ['name', 'category__name']

    def perform_create(self, serializer):
        """
        Overrides the default create behavior to automatically assign
        the logged-in user to the 'created_by' field.
        """
        # self.request.user gives us the user who made the request
        # We pass this user to the serializer's save method
        serializer.save(created_by=self.request.user)