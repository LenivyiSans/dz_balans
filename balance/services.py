from .models import Transaction, Account
from django.db import transaction as db_transaction


def process_transaction(data):
    debit = data['debit_account']
    credit = data['credit_account']
    amount = data['amount']
    description = data['description']

    if debit == credit:
        raise ValueError("Счета не должны совпадать")

    with db_transaction.atomic():
        Transaction.objects.create(
            debit_account=debit,
            credit_account=credit,
            amount=amount,
            description=description
        )

        update_balances(debit, credit, amount)


def update_balances(debit, credit, amount):
    if debit.account_type == 'asset':
        debit.balance += amount
    else:
        debit.balance -= amount

    if credit.account_type == 'asset':
        credit.balance -= amount
    else:
        credit.balance += amount

    debit.save()
    credit.save()


def annul_transaction(original_tx: Transaction):
    if original_tx.is_annulled:
        return

    with db_transaction.atomic():
        reverse_tx = Transaction.objects.create(
            debit_account=original_tx.credit_account,
            credit_account=original_tx.debit_account,
            amount=original_tx.amount,
            description=f"Сторно транзакции #{original_tx.id}",
            reversed_transaction=original_tx
        )
        update_balances(reverse_tx.debit_account, reverse_tx.credit_account, reverse_tx.amount)
        original_tx.is_annulled = True
        original_tx.save()
