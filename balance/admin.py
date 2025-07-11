from django.contrib import admin
from .models import BalanceArticle, BalanceGroup, Account, Transaction

admin.site.register(BalanceArticle)
admin.site.register(BalanceGroup)
admin.site.register(Account)
admin.site.register(Transaction)
