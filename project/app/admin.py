from django.contrib import admin

# Register your models here.
from .models import Test, StockInfo, FinancialProduct, StructuredFinancialInvestment

admin.site.register(Test)
admin.site.register(StockInfo)
admin.site.register(FinancialProduct)
admin.site.register(StructuredFinancialInvestment)