from django.shortcuts import render,redirect
from django.views.generic import DetailView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *

# Create your views here.
def HomeView(request, category_slug = None):
    food = Food.objects.all()
    if category_slug is not None:
        category = Category.objects.get(slug = category_slug)
        food = Food.objects.filter(category  = category)
    categories = Category.objects.all()
    return render(request, 'home.html', {'food' : food, 'category' : categories})

def SpecialItems(request, category_slug = None):
    food = Food.objects.filter(is_special=True)
    if category_slug is not None:
        category = Category.objects.get(slug = category_slug)
        food = Food.objects.filter(category  = category, is_special=True)
    categories = Category.objects.all()
    return render(request, 'specials.html', {'food' : food, 'category' : categories})

class UserReview(LoginRequiredMixin, DetailView):
    model = Food
    template_name = 'review.html'
    pk_url_kwarg = 'id'

    def post(self, request, *args, **kwargs):
        comment_form = ReviewForm(data=request.POST)
        food = self.get_object()

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.food = food
            new_comment.user = self.request.user
            new_comment.save()
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_form = ReviewForm()
        
        context['comment_form'] = comment_form
        return context

class FoodReview(DetailView):
    model = Food
    template_name = 'food_reviews.html'
    context_object_name = 'food'
    pk_url_kwarg = 'id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        food = self.object 
        comments = food.reviews.all()
        
        context['comments'] = comments
        return context