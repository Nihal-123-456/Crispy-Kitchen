from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import FormView,ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import *
from .models import *
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from food.models import *

# Create your views here.
class SignupView(FormView):
    template_name = 'form.html'
    form_class = SignupForm
    success_url = reverse_lazy('home')
    
    def form_valid(self,form):
        user = form.save()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_link = f"https://food-shop-siej.onrender.com//active/{uid}/{token}"
        email_subject = "Confirm Your Email"
        email_body = render_to_string('confirm_email.html', {'confirm_link' : confirm_link})
        
        email = EmailMultiAlternatives(email_subject , '', to=[user.email])
        email.attach_alternative(email_body, "text/html")
        email.send()
        messages.success(self.request, 'Signup Successful. Check your mail for confirmation')
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = 'form.html'
    def get_success_url(self):
        messages.success(self.request, 'Signin Successful')
        return reverse_lazy('home')

class UserLogoutView(LogoutView):
    def get_success_url(self):
        messages.warning(self.request, 'Logout Successful')
        return reverse_lazy('home')

def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None 
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,'Email verified. Now Please Login')
        return redirect('home')
    else:
        return redirect('signup')

class OrderFood(LoginRequiredMixin, View):
    def get(self, request, food_id):
        food = get_object_or_404(Food, id=food_id)
        OrderHistory.objects.create(user=request.user, food=food, order_price=food.price)
        messages.success(request, f'Your order is successful')
        return redirect('order_report')

class OrderFoodCart(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user)
        for cart_item in cart_items:
            OrderHistory.objects.create(
                user=request.user,
                food=cart_item.food,
                order_price=cart_item.food.price,
            )
        cart_items.delete()
        return redirect('order_report')

class OrderHistoryReport(LoginRequiredMixin, ListView):
    template_name = 'order_history.html'
    model = OrderHistory
    context_object_name = 'OrderReport'
    def get_queryset(self):
        user = self.request.user
        queryset = OrderHistory.objects.filter(user=user)
        return queryset

class AddToCart(LoginRequiredMixin, View):
    def get(self, request, food_id):
        food = get_object_or_404(Food, id=food_id)
        Cart.objects.create(user=request.user, food=food, food_price=food.price)
        messages.success(request, f'Item successfully added to Cart')
        return redirect('cart_report')

class RemoveFromCart(LoginRequiredMixin, View):
    def get(self, request, cart_id):
        cart = get_object_or_404(Cart, id=cart_id)
        cart.delete()
        return redirect('cart_report')

class CartReport(LoginRequiredMixin, ListView):
    template_name = 'cart.html'
    model = Cart
    context_object_name = 'CartReport'
    def get_queryset(self):
        user = self.request.user
        queryset = Cart.objects.filter(user=user)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_cost = sum(cart.food_price for cart in context['CartReport'] if cart.food_price is not None)

        context['total_cost'] = total_cost
        return context