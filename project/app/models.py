from django.db import models
from djongo import models as mongo_models

class Test(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class StockInfo(models.Model):
    stock_id = models.IntegerField(default=0)
    company_name = models.CharField(max_length=50)
    date = models.CharField(default= "unknown", max_length=50)
    price = models.DecimalField(default=0, max_digits=100, decimal_places=50)

    def __str__(self):
        return self.company_name

class FinancialProduct(models.Model):
    fp_id = models.IntegerField(default=0)
    product_name = models.CharField(default= "unnamed", max_length=50)

    def __str__(self):
        return self.product_name

class StructuredFinancialInvestment(models.Model):
    fp_id = models.ForeignKey(FinancialProduct, null=True, on_delete=models.CASCADE)
    stock_id = models.ForeignKey(StockInfo, null = True, on_delete=models.CASCADE)
    SFI_id = models.IntegerField(default=0)
    Knock_in = models.DecimalField(default=0, max_digits=100, decimal_places=50)
    Knock_out = models.DecimalField(default=0, max_digits=100, decimal_places=50)
    put_strike = models.DecimalField(default=0, max_digits=100, decimal_places=50)



"""
MongoDB for the User Table
"""


class Users(mongo_models.Model):
    use_name = mongo_models.CharField(max_length=255, primary_key=True)
    password = mongo_models.CharField(max_length=255)
    object = mongo_models.DjongoManager()


class UserClicks(mongo_models.Model):
    _id = mongo_models.ObjectIdField()
    company = mongo_models.CharField(max_length=255, default='unknown')
    user_id = mongo_models.CharField(max_length=255)
    object = mongo_models.DjongoManager()


class UserSaves(mongo_models.Model):
    _id = mongo_models.ObjectIdField()
    company = mongo_models.CharField(max_length=255, default='unknown')
    user_id = mongo_models.CharField(max_length=255)
    object = mongo_models.DjongoManager()




