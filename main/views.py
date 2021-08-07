from django.shortcuts import get_object_or_404, render, redirect
from .models import customer, transactions
from django.views.generic import ListView
from django.views.generic import CreateView, DetailView
from django.http.response import HttpResponseRedirect
from .forms import transactionForm, userForm
from django.views.generic.edit import ModelFormMixin
from django.contrib import messages
from django.views.generic.edit import FormMixin
import re
from unicodedata import decimal
from numpy.compat import unicode


# Create your views here.
def home(request):
    return render(request, 'main/home.html')

def customers(request):
    # model = customer
    # template_name = 'main/customer.html'
    # context_object_name = 'customers'
    # def get_queryset(self):
    #     # user = get_object_or_404(User, username=self.kwargs.get('username'))
    #     return customer.objects.all()
    return render(request, 'main/customer.html', {'customers': customer.objects.all()})

def transfer(request):
    c = customer.objects.all()
    form = transactionForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data.get('amount')
        fromUser = form.cleaned_data.get('fromUser')
        toUser = form.cleaned_data.get('toUser').name
        # selected_item = get_object_or_404(customer, pk=request.POST.get('toUser'))
        # toUser = selected_item
        if fromUser == toUser:
            messages.error(request, 'You can not transfer to yourself')
        else:
            for cust in c:
                if cust.name == fromUser:
                    customer.objects.filter(name=fromUser).update(balance=cust.balance - amount)
                if cust.name == toUser:
                    customer.objects.filter(name=toUser).update(balance=cust.balance + amount)
            form.save()
            messages.success(request, 'Your Transaction has been successfully completed !!')
            return redirect('transaction')
    return render(request, 'main/transfer.html', {'customers': customer.objects.all(), 'form': form})    

def transaction(request):
    # model = transactions
    # template_name = 'main/transaction.html'
    # context_object_name = 'transactions'
    # def get_queryset(self):
    #     # user = get_object_or_404(User, username=self.kwargs.get('username'))
    #     return transactions.objects.all()
    return render(request, 'main/transaction.html', {'transactions': transactions.objects.all()})

def customer_detail(request):
    return render(request, 'main/customer_detail.html')


def customer_detail(request, pk):
    sender = customer.objects.get(id=pk)
    if request.method == 'POST':
        recipient_id = request.POST['toUser']
        print("Recipient id : " + str(recipient_id))
        print("Sender id : " + str(sender.id))
        if request.POST['amount'] == '' or not re.match('[+-]?([0-9]*[.])?[0-9]+', request.POST['amount']):
            messages.error(request, 'Please Enter Valid amount')
        else:
            amount = float((request.POST['amount']))
        
        if recipient_id == 'Select Customer':
            messages.warning(request, 'Please Select Customer')
        elif float(recipient_id) == float(sender.id):
            messages.warning(request, 'You cannot transfer money to yourself !!')
        else:
            recipient = customer.objects.get(id=recipient_id)
            if float(sender.balance) < amount:
                messages.warning(request, 'Insufficient Balance')
            else:
                sender.balance = sender.balance - (amount)
                recipient.balance = recipient.balance + (amount)
                sender.save()
                recipient.save()
                transaction_info = transactions(fromUser=sender, toUser=recipient, amount=amount)
                transaction_info.save()
                messages.success(request, 'Your Transaction has been successfully completed !!')
    return render(request, 'main/customer_detail.html', {'sender': sender, 'customers': customer.objects.all()})

def register_user(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        balance = request.POST['balance']
        date = request.POST['dateCreated']
        newUserEntry = customer(dateCreated=date, name=name, email=email, balance=balance)
        newUserEntry.save()
        messages.success(request, 'Customer Registred Successfully !!')
        return redirect('customers')
    return render(request, 'main/registerUser.html', {'form': userForm()})