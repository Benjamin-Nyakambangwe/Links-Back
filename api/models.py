from django.db import models
from accounts.models import PublisherProfile, AdvertiserProfile
from django.core.validators import MinValueValidator, MaxValueValidator

class Site(models.Model):
    publisher = models.ForeignKey(PublisherProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, unique=True)
    niche = models.ForeignKey('Niche', on_delete=models.CASCADE)
    domain_authority = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    organic_traffic = models.PositiveIntegerField()
    price_per_link = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    available_slots = models.PositiveIntegerField(blank=True, null=True)
    guidelines = models.TextField(blank=True, null=True)
    support_casino = models.BooleanField(default=False)
    support_sports_betting = models.BooleanField(default=False)
    support_loans = models.BooleanField(default=False)
    support_dating = models.BooleanField(default=False)
    support_forex = models.BooleanField(default=False)
    support_crypto = models.BooleanField(default=False)
    casino_multiplier = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sports_betting_multiplier = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    loans_multiplier = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    dating_multiplier = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    forex_multiplier = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    crypto_multiplier = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


    class Meta:
        indexes = [
            models.Index(fields=['domain']),
            models.Index(fields=['niche']),
        ]

    def __str__(self):
        return self.domain
    

class Niche(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class LinkRequest(models.Model):
    advertiser = models.ForeignKey(AdvertiserProfile, on_delete=models.CASCADE)
    publisher = models.ForeignKey(PublisherProfile, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    url = models.URLField()
    anchor_text = models.CharField(max_length=255)
    status = models.ForeignKey('LinkRequestStatus', on_delete=models.CASCADE, related_name='link_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    cost = models.DecimalField(max_digits=10, decimal_places=3)

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.url

class LinkRequestStatus(models.Model):
    status = models.CharField(max_length=50,)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
        ]


class Payment(models.Model):
    request = models.ForeignKey(LinkRequest, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_id = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class Rating(models.Model):
    advertiser = models.ForeignKey(AdvertiserProfile, on_delete=models.CASCADE)
    publisher = models.ForeignKey(PublisherProfile, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Report(models.Model):
    advertiser = models.ForeignKey(AdvertiserProfile, on_delete=models.CASCADE)
    publisher = models.ForeignKey(PublisherProfile, on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)



