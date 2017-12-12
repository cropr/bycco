from django.contrib import admin
from .models import Subscription

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
   list_display = ('first_name', 'last_name', 'idbel')
   list_filter = ('federation', 'nationalityfide', 'nationalitybel', 'idclub',
                  'payamount', 'paydate')
   list_per_page = 50
   ordering = ['last_name', 'first_name']

