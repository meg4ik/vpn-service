from django.db import models
from users.models import CustomUser


class Link(models.Model):
    original_url = models.URLField()
    site_attrs = models.CharField(max_length=512)
    user_site_name = models.CharField(max_length=64)
    is_delete = models.BooleanField(default = False)
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE,related_name="link")


class RedirectHistory(models.Model):
    enter_date = models.DateTimeField(auto_now_add=True)
    data_request_bytes = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    data_response_bytes = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    link = models.ForeignKey(Link, on_delete = models.CASCADE,related_name="link_history")
