from django.contrib import admin
from .models import CdSubscription

@admin.register(CdSubscription)
class CdSubscriptionAdmin(admin.ModelAdmin):
   list_display = ('firstname', 'name', 'id_national')
   list_filter = ('federation', 'fidenation', 'nationality', 'id_club',
                  'payamount', 'paydate')
   list_per_page = 50
   ordering = ['name', 'firstname']

