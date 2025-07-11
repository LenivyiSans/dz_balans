from django.db import models
import uuid


class BalanceArticle(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class BalanceGroup(models.Model):
    name = models.CharField(max_length=255)
    article = models.ForeignKey(BalanceArticle, on_delete=models.CASCADE, related_name="groups")

    def __str__(self):
        return self.name


class Account(models.Model):
    ACCOUNT_TYPES = (
        ('asset', 'Актив'),
        ('liability', 'Пассив'),
        ('both', 'Активно-пассивный'),
    )
    number = models.CharField(max_length=10, unique=True, editable=False)
    name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)
    balance_group = models.ForeignKey(BalanceGroup, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = uuid.uuid4().hex[:10]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.number} — {self.name}"


class Transaction(models.Model):
    description = models.TextField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    debit_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="debit_transactions")
    credit_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="credit_transactions")
    reversed_transaction = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True)
    is_annulled = models.BooleanField(default=False)

    def __str__(self):
        return f"#{self.id} {self.description} ({self.amount})"
