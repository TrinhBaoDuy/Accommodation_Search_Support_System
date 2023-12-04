
from rest_framework.decorators import action
from ASSSs import serializers, paginators
from ASSSs.models import House, Image
from rest_framework import viewsets , generics, status
from rest_framework.response import Response
# Create your views here.


class HouseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = House.objects.all()
    serializer_class = serializers.HouseSerializer
    pagination_class = paginators.ASSSPaginator

    def get_queryset(self):
        queries = self.queryset

        h = self.request.query_params.get("address")
        if h:
            queries = queries.filter(address__icontains=h)

        return queries

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






