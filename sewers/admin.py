from django.contrib import admin
from .models import Sewer


@admin.register(Sewer)
class SewerAdmin(admin.ModelAdmin):
    list_display = (
        "idn",
        "gubn",
        "gubn_nam",
        "mea_ymd",
        "mea_wal",
        "sig_sta",
        "remark",
    )
