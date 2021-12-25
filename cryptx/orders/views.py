from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.http import HttpResponse
from django.contrib.auth.models import User

from django.http import JsonResponse

#Auth and messages
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from uuid import uuid4

import json

from coins.models import Coin
from dashboard.models import AccountBook
from portfolio.models import Portfolio
from orders.models import Order
from dashboard.models import Profile

from django.conf import settings
from django.views.generic.base import TemplateView
import stripe

from dashboard.models import Profile, TransactionHistory



stripe.api_key = settings.STRIPE_SECRET_KEY


def handle_buy(request):
    user=request.user
    if user.is_authenticated and request.method=='POST':
        coin_symbol = request.POST.get("symbol")
        quantity = float(request.POST.get("quantity"))
        order_type = request.POST.get('order_type')
        limit_price=0
        if(order_type=="LIMIT"):
            limit_price = float(request.POST.get('price'))
        

        if order_type=="MARKET":
            order_type=Order.MARKET
        else:
            order_type=Order.LIMIT

        # user,coin_symbol,quantity,mode,order_type
        order_obj = {
            'user':user,
            'coin_symbol':coin_symbol,
            'quantity':quantity,
            'mode':Order.BUY,
            'order_type':order_type,
            'limit_price':limit_price
        }

        is_executable=Order.can_be_executed(order_obj)

        msg = ""
        success=1
        if is_executable[0]==True:
            msg="Order was Placed Successfully"
        else:
            success=0
            msg=is_executable[1]
        
        # Sending response to frontend for scheduling limit order task
        order = {
            'id':is_executable[1],
            'coin_symbol':coin_symbol,
            'order_type':order_type,
            'limit_price':limit_price,
            'order_mode':Order.BUY,
        }

        resp={
            'order':order,
            'msg':msg,
            'success':success
        }
        response=json.dumps(resp)
        return HttpResponse(response,content_type='application/json')

    return redirect('home')


class wallet_view(TemplateView):
    template_name = 'orders/wallet.html'

    def get_context_data(self, **kwargs): # new
        user = self.request.user
        print(user.username)
        history = TransactionHistory.objects.filter(email = user.username)
        # profile = Profile.objects.filter(email = user.username)
        context = super().get_context_data(**kwargs)
        context['money'] = Profile.get_money(user.username)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        context['history'] = history
        return context


def charge(request):
    user=request.user
    if user.is_authenticated:
        print(user.email + " is adding money")
        if request.method == 'POST':
            amount = request.POST.get('amount')
            set_amount = int(amount)*100
            # print(amount)
            charge = stripe.Charge.create(
                amount=set_amount,
                currency='INR',
                description='Money added to Wallet',
                source=request.POST['stripeToken']
            )

            user_profile = Profile.objects.get(email=user.email)
            account_message = 'Added Money to Wallet'
            Profile.add_money(user=user,amount=float(amount),msg=account_message)


            history = TransactionHistory(email = user.email , money = float(amount))
            history.save()

            return render(request, 'orders/charge.html')

    return redirect('home')



def handle_sell(request):
    user=request.user
    if user.is_authenticated and request.method=='POST':
        coin_symbol = request.POST.get("symbol")
        quantity = float(request.POST.get("quantity"))
        order_type = request.POST.get('order_type')
        limit_price=0
        if(order_type=="LIMIT"):
            limit_price = float(request.POST.get('price'))
        

        if order_type=="MARKET":
            order_type=Order.MARKET
        else:
            order_type=Order.LIMIT

        # user,coin_symbol,quantity,mode,order_type
        order_obj = {
            'user':user,
            'coin_symbol':coin_symbol,
            'quantity':quantity,
            'mode':Order.SELL,
            'order_type':order_type,
            'limit_price':limit_price
        }

        is_executable=Order.can_be_executed(order_obj)

        msg = ""
        success=1
        if is_executable[0]==True:
            msg="Order was Placed Successfully"
        else:
            success=0
            msg=is_executable[1]
        
        # Sending response to frontend for scheduling limit order task
        order = {
            'id':is_executable[1],
            'coin_symbol':coin_symbol,
            'order_type':order_type,
            'limit_price':limit_price,
            'order_mode':Order.SELL
        }

        resp={
            'order':order,
            'msg':msg,
            'success':success
        }
        response=json.dumps(resp)
        return HttpResponse(response,content_type='application/json')

    return redirect('home')



def order_history(request):
    user = request.user
    if user.is_authenticated:

        user_orders = Order.objects.filter(user=user)
        
        return render(request,'orders/order_history.html',context={'orders':user_orders})

    return redirect('home')



def handle_limit_orders(request):
    user=request.user
    if user.is_authenticated and request.method=='GET':
        order_id = request.GET.get('order_id')
        price = float(request.GET.get('price'))
        user_orders = Order.objects.filter(id=order_id)
        profile = Profile.objects.get(email=user.email)

        if len(user_orders):
            order = user_orders[0]

            # If order already executed
            if order.order_status==Order.EXECUTED:
                print("order already executed")
                resp={
                }
                response=json.dumps(resp)
                return HttpResponse(response,content_type='application/json') 


            order.order_status = Order.EXECUTED
            if order.mode == Order.BUY:
                profile.money += (float(order.quantity)*float(order.order_price))-(float(price)*float(order.quantity))
                order.order_price =  price
                Portfolio.buy_coin(user,order.quantity,price,order.coin)

            if order.mode == Order.SELL:
                profile.money += order.quantity * price
                order.order_price =  price
                
                # if quantity becomes zero after selling
                Portfolio.check_delete(user,order.coin)


            order.save()
            profile.save()
            
        resp={
            
        }
        response=json.dumps(resp)
        return HttpResponse(response,content_type='application/json') 
    return  redirect('home')


def handle_cancel_order(request):
    user=request.user
    if user.is_authenticated and request.is_ajax():
        order_id = request.GET.get('id')

        Order.cancel_order(order_id,user)

        return JsonResponse({})

    return redirect('home')