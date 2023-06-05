from django.db import models

# Create your models here.

class InformacionCliente(models.Model):
    ID = models.IntegerField(blank=True, null=True)
    Year_Birth = models.IntegerField(blank=True, null=True)
    Education = models.CharField(max_length=200) 
    Marital_Status = models.CharField(max_length=200) 
    Income =models.FloatField(blank=True, null=True)
    Kidhome=models.IntegerField(blank=True, null=True)
    Teenhome =models.IntegerField(blank=True, null=True)
    Dt_Customer = models.DateTimeField()
    Recency =models.IntegerField(blank=True, null=True)
    MntWines =models.IntegerField(blank=True, null=True)
    MntFruits=models.IntegerField(blank=True, null=True)
    MntMeatProducts =models.IntegerField(blank=True, null=True)
    MntFishProducts =models.IntegerField(blank=True, null=True)
    MntSweetProducts=models.IntegerField(blank=True, null=True)
    MntGoldProds =models.IntegerField(blank=True, null=True)
    NumDealsPurchases =models.IntegerField(blank=True, null=True)
    NumWebPurchases=models.IntegerField(blank=True, null=True)
    NumCatalogPurchases =models.IntegerField(blank=True, null=True)
    NumStorePurchases =models.IntegerField(blank=True, null=True)
    NumWebVisitsMonth=models.IntegerField(blank=True, null=True)
    Year_Enrolled =models.IntegerField(blank=True, null=True)
    Age=models.IntegerField(blank=True, null=True)
    class Meta:
        verbose_name = "Clientes"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return str(self.created)
