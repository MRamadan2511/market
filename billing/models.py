from django.db import models
# from orders.models import Order
# from django.utils import timezone

'''
class PaymentStatus(models.Model):

    ## max_length=20, 
      ##  choices=(('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')), 
        ##default='pending
    
    name = models.CharField(max_length=50)


class Payment(models.Model):
    order = models.ForeignKey(Order, related_name="payments", on_delete=models.CASCADE)
    # customer = models.ForeignKey(accounts  , on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)  # e.g., 'credit_card', 'paypal'
    payment_reference = models.CharField(max_length=255, blank=True, null=True)  # External gateway reference
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.ForeignKey(PaymentStatus,  on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} for Order #{self.order.id}"


class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=100, unique=True)
    issue_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Invoice #{self.invoice_number} for Order #{self.order.id}"

    def generate_invoice_number(self):
        self.invoice_number = f"INV-{self.order.id}-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        self.save()
        return self.invoice_number
'''