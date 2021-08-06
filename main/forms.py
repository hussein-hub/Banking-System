from django import forms
from .models import transactions, customer

class transactionForm(forms.ModelForm):
    class Meta:
        model = transactions
        fields = ['amount', 'date', 'fromUser', 'toUser']

class userForm(forms.ModelForm):
    class Meta:
        model = customer
        fields = ['id', 'name', 'email', 'balance', 'dateCreated']