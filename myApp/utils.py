from .models import Stock

def decrease_stock(product, location, quantity):
    try:
        stock = Stock.objects.get(product=product, location=location)
        stock.quantity -= quantity
        stock.save()
    except Stock.DoesNotExist:
        # Handle case where stock doesn't exist
        pass
