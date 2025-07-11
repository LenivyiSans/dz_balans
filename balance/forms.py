from django import forms
from .models import Account


class TransactionForm(forms.Form):
    debit_account = forms.ModelChoiceField(queryset=Account.objects.all(), label="Дебет")
    credit_account = forms.ModelChoiceField(queryset=Account.objects.all(), label="Кредит")
    amount = forms.DecimalField(label="Сумма", min_value=0.01)
    description = forms.CharField(widget=forms.Textarea, label="Описание")
