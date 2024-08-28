from rest_framework import serializers
from .models import Site, LinkRequest, LinkRequestStatus, Niche


class NicheSerializer(serializers.ModelSerializer):
    class Meta:
        model = Niche
        fields = ['id', 'name']

class SiteSerializer(serializers.ModelSerializer):
    niche = NicheSerializer(read_only=True)
    niche_id = serializers.PrimaryKeyRelatedField(queryset=Niche.objects.all(), source='niche', write_only=True)

    class Meta:
        model = Site
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['publisher'] = instance.publisher.phone  # Assuming publisher has a name field
        # representation['publisher'] = instance.publisher.name  # Assuming publisher has a name field
        return representation



class LinkRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkRequest
        fields = '__all__'

class LinkRequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkRequestStatus
        fields = '__all__'

