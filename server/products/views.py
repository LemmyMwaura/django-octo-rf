from rest_framework import generics
from products.models import Product
from products.serializers import ProductSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404
# Create your views here.

class ProductListCreateAPIView(generics.ListCreateAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer

  def perform_create(self, serializer):
    title = serializer.validated_data.get('title') 
    content = serializer.validated_data.get('content') or None
    if content is None:
      content = title
    serializer.save(content=content)
    # send a signal
    # return super().perform_create(serializer)

product_list_create_view = ProductListCreateAPIView.as_view()

class ProductDetailAPIView(generics.RetrieveAPIView):
  # get from id
  queryset = Product.objects.all()
  serializer_class = ProductSerializer

product_detail_view = ProductDetailAPIView.as_view()

class ProductListAPIView(generics.ListAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer

product_list_view = ProductListAPIView.as_view()

class ProductUpdateAPIView(generics.UpdateAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  lookup_field = "pk"

  def perform_update(self, serializer):
    instance = serializer.save()
    if not instance.content:
      instance.content = instance.title

product_update_view = ProductUpdateAPIView.as_view()

class ProductDeleteAPIView(generics.DestroyAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer

product_delete_view = ProductDeleteAPIView.as_view()

@api_view(['GET','POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
  # list, create and detail view
  method = request.method

  if method == "GET":
    if pk is not None:
      obj = get_object_or_404(Product, pk=pk)
      data = ProductSerializer(obj).data
    else:
      queryset = Product.objects.all(pk=pk)
      data = ProductSerializer(queryset, many=True).data
    return Response(data)

  if method == "POST":
    #create an item
    serializer = ProductSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
      title = serializer.validated_data.get('title') 
      content = serializer.validated_data.get('content') or None

      if content is None:
        content = title

      serializer.save(content=content)
      return Response(serializer.data)
    return Response({"invalid":"not good data"}, status=400)
