from django.contrib import admin
from .models import Comentario as comments, Oferta as bids, Subasta as listings

# Register your models here.
admin.site.register(comments)
admin.site.register(bids)
admin.site.register(listings)
