from django.db import models


class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=45)
    energy = models.FloatField(blank=True, null=True)
    fat = models.FloatField(blank=True, null=True)
    carbohydrate = models.FloatField(blank=True, null=True)
    protein = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'

class Receipts(models.Model):
    receipt_id = models.AutoField(primary_key=True)
    receipt_name = models.CharField(max_length=45)
    date = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'receipts'


class ReceiptsContent(models.Model):
    id = models.AutoField(primary_key=True)
    receipt = models.ForeignKey(Receipts, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.FloatField(blank=True, null=True)
    unit_of_measurement = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'receipts_content'


class ReceiptProcessingLogs(models.Model):
    receipt = models.ForeignKey('Receipts', models.DO_NOTHING, blank=True, null=True)
    message = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'receipt_processing_logs'


