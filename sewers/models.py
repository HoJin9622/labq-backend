from django.db import models


class Sewer(models.Model):
    idn = models.CharField(max_length=20, verbose_name="고유번호")
    gubn = models.CharField(max_length=20, verbose_name="구분코드")
    gubn_nam = models.CharField(max_length=20, verbose_name="구분명")
    mea_ymd = models.DateTimeField(verbose_name="측정일자")
    mea_wal = models.FloatField(verbose_name="측정수위")
    sig_sta = models.CharField(max_length=20, verbose_name="통신상태")
    remark = models.TextField(verbose_name="위치정보")

    class Meta:
        verbose_name = "하수관"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.remark}: {self.mea_wal}"
