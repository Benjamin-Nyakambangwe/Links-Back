import django_filters
from .models import Site

class SiteFilter(django_filters.FilterSet):
    domain = django_filters.CharFilter(lookup_expr='icontains')
    niche = django_filters.CharFilter(field_name='niche__name')
    domain_authority_min = django_filters.NumberFilter(field_name='domain_authority', lookup_expr='gte')
    domain_authority_max = django_filters.NumberFilter(field_name='domain_authority', lookup_expr='lte')
    organic_traffic_min = django_filters.NumberFilter(field_name='organic_traffic', lookup_expr='gte')
    organic_traffic_max = django_filters.NumberFilter(field_name='organic_traffic', lookup_expr='lte')
    price_per_link_min = django_filters.NumberFilter(field_name='price_per_link', lookup_expr='gte')
    price_per_link_max = django_filters.NumberFilter(field_name='price_per_link', lookup_expr='lte')
    available_slots_min = django_filters.NumberFilter(field_name='available_slots', lookup_expr='gte')
    support = django_filters.MultipleChoiceFilter(
        choices=[
            ('casino', 'Casino'),
            ('sports_betting', 'Sports Betting'),
            ('loans', 'Loans'),
            ('dating', 'Dating'),
            ('forex', 'Forex'),
            ('crypto', 'Crypto'),
        ],
        method='filter_support'
    )

    class Meta:
        model = Site
        fields = ['domain', 'niche', 'domain_authority', 'organic_traffic', 'price_per_link', 'available_slots', 'support']

    def filter_support(self, queryset, name, value):
        for support_type in value:
            queryset = queryset.filter(**{f'support_{support_type}': True})
        return queryset