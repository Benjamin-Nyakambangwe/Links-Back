from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from .models import Site
from .serializers import SiteSerializer
from .filters import SiteFilter
from rest_framework.permissions import AllowAny



class OwnSiteListView(APIView):
    def get(self, request):
        # Get the authenticated user
        # Filter sites by the authenticated user
        queryset = Site.objects.all()
        serializer = SiteSerializer(queryset, many=True)
        return Response(serializer.data)

class SiteListCreateView(APIView):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = SiteFilter
    search_fields = ['name', 'domain', 'niche__name']
    ordering_fields = ['domain_authority', 'organic_traffic', 'price_per_link', 'available_slots']
    permission_classes = [AllowAny]

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def get(self, request):
        queryset = Site.objects.select_related('niche', 'publisher').all()
        filtered_queryset = self.filter_queryset(queryset)
        serializer = SiteSerializer(filtered_queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SiteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SiteRetrieveUpdateDestroyView(APIView):
    def get_object(self, pk):
        try:
            return Site.objects.get(pk=pk)
        except Site.DoesNotExist:
            return None

    def get(self, request, pk):
        site = self.get_object(pk)
        if site is not None:
            serializer = SiteSerializer(site)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        site = self.get_object(pk)
        if site is not None:
            serializer = SiteSerializer(site, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        site = self.get_object(pk)
        if site is not None:
            site.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
    


