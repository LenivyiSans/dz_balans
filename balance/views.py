from django.shortcuts import render, redirect, get_object_or_404
from .models import Account, Transaction
from .forms import TransactionForm
from .services import process_transaction, annul_transaction


def account_list(request):
    accounts = Account.objects.all()
    return render(request, 'balance/account_list.html', {'accounts': accounts})


def transaction_list(request):
    transactions = Transaction.objects.order_by('-date')
    return render(request, 'balance/transaction_list.html', {'transactions': transactions})


def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            process_transaction(form.cleaned_data)
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'balance/transaction_form.html', {'form': form})


def transaction_annul(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    annul_transaction(transaction)
    return redirect('transaction_list')
