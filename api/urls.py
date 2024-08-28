from django.urls import path
from .views import SiteListCreateView, SiteRetrieveUpdateDestroyView, OwnSiteListView

urlpatterns = [
    path('own-sites/', OwnSiteListView.as_view(), name='own-sites'),
    path('sites/', SiteListCreateView.as_view(), name='site-list-create'),
    path('sites/<int:pk>/', SiteRetrieveUpdateDestroyView.as_view(), name='site-retrieve-update-destroy'),
]