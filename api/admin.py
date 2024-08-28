from django.contrib import admin
from .models import Site, Niche, LinkRequest, LinkRequestStatus

@admin.register(Niche)
class NicheAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'niche', 'domain_authority', 'organic_traffic', 'price_per_link', 'available_slots')
    list_filter = ('niche', 'support_casino', 'support_sports_betting', 'support_loans', 'support_dating', 'support_forex', 'support_crypto')
    search_fields = ('name', 'domain')

@admin.register(LinkRequestStatus)
class LinkRequestStatusAdmin(admin.ModelAdmin):
    list_display = ('status', 'timestamp')
    search_fields = ('status',)

@admin.register(LinkRequest)
class LinkRequestAdmin(admin.ModelAdmin):
    list_display = ('url', 'anchor_text', 'advertiser', 'site', 'status', 'type', 'created_at')
    list_filter = ('status', 'type', 'created_at')
    search_fields = ('url', 'anchor_text')
    readonly_fields = ('created_at', 'updated_at')