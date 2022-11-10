from django.db import models


class Rainfall(models.Model):
    rainguage_code = models.FloatField(verbose_name="강우량계 코드")
    raingauge_name = models.CharField(max_length=20, verbose_name="강우량계명")
    gu_code = models.FloatField(verbose_name="구청 코드")
    gu_name = models.CharField(max_length=20, verbose_name="구청명")
    rainfall10 = models.CharField(max_length=20, verbose_name="10분우량")
    receive_time = models.DateTimeField(verbose_name="자료수집 시각")

    class Meta:
        verbose_name = "강우량"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.gu_name}({self.raingauge_name}): {self.rainfall10}"
