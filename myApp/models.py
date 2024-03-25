from django.db import models
from myApp.models import Product, Location, Order, Stock 
from .utils import decrease_stock 

class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def mark_invoice_as_paid(self):
        ordered_products = self.order.orderedproduct_set.all()
        for ordered_product in ordered_products:
            decrease_stock(ordered_product.product, self.order.client.default_location, ordered_product.quantity)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.mark_invoice_as_paid()

class TransferNote(models.Model):
    products = models.ManyToManyField(Product, through='TransferDetail')
    location_from = models.ForeignKey(Location, related_name='transfers_from', on_delete=models.CASCADE)
    location_to = models.ForeignKey(Location, related_name='transfers_to', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for transfer_detail in self.transferdetail_set.all():
            decrease_stock(transfer_detail.product, self.location_from, transfer_detail.quantity)

class TransferDetail(models.Model):
    transfer = models.ForeignKey(TransferNote, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name
