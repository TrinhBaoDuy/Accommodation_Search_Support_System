from django.http import Http404
from rest_framework.decorators import action, permission_classes
from ASSSs import serializers, paginators
from ASSSs.models import House, Image, Post, Discount, PostingPrice, User, Follow, Booking
from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
# Create your views here.


class HouseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = House.objects.all()
    serializer_class = serializers.HouseSerializer
    pagination_class = paginators.ASSSPaginator
    # permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    #     queries = self.queryset
    #
    #     if self.action == 'list':
    #         return [permissions.AllowAny]
    #
    #     h = self.request.query_params.get("address")
    #     if h:
    #         queries = queries.filter(address__icontains=h)
    #
    #     return queries

    # @permission_classes([AllowAny])
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    # @permission_classes([IsAuthenticated])
    def retrieve(self, request, pk=None):
        house = self.get_object(pk)
        serializer = self.serializer_class(house)
        return Response(serializer.data)

    # @permission_classes([IsAuthenticated])
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @permission_classes([IsAuthenticated])
    def update(self, request, pk=None):
        house = self.get_object(pk)
        serializer = self.serializer_class(house, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @permission_classes([IsAuthenticated])
    def destroy(self, request, pk=None):
        house = self.get_object(pk)
        house.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return House.objects.get(pk=pk)
        except House.DoesNotExist:
            raise Http404

    def get_queryset(self):
        queryset = self.queryset

        address = self.request.query_params.get("address")
        if address:
            queryset = queryset.filter(address__icontains=address)

        return queryset

    @action(methods=['get'], detail=True)
    def images(self, request, pk):
        images = self.get_object().image_set.all()
        # import pdb
        # pdb.set_trace()
        return Response(serializers.ImageSerializer(images, many=True,  context={'request': request}).data,
                        status=status.HTTP_200_OK)


class ImageViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = serializers.ImageSerializer
    pagination_class = paginators.ASSSPaginator

    def get_queryset(self):
        queries = self.queryset

        q = self.request.query_params.get("houseID")
        if q:
            queries = queries.filter(house__id=q)

        return queries

    # def create(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def update(self, request, pk=None):
    #     image = self.get_object(pk)
    #     serializer = self.serializer_class(image, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #


class PostViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    pagination_class = paginators.ASSSPaginator

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        post = self.get_object(pk)
        serializer = self.serializer_class(post)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        post = self.get_object(pk)
        serializer = self.serializer_class(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get_queryset(self):
        queries = self.queryset

        q = self.request.query_params.get("address")
        if q:
            queries = queries.filter(house__address__icontains=q)
        return queries


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = serializers.DiscountSerializer
    pagination_class = paginators.ASSSPaginator


class PostingPriceViewSet(viewsets.ModelViewSet):
    queryset = PostingPrice.objects.all()
    serializer_class = serializers.PostingPriceSerializer
    pagination_class = paginators.ASSSPaginator


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    pagination_class = paginators.ASSSPaginator


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = serializers.FollowSerializer
    pagination_class = paginators.ASSSPaginator


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = serializers.BookingSerializer
    pagination_class = paginators.ASSSPaginator

