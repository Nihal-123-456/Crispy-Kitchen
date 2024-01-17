"""
URL configuration for food_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from food.views import *
from user.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView, name='home'),
    path('category/<slug:category_slug>/', HomeView, name='food_category'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('signin/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('active/<uid64>/<token>',activate,name='active'),
    path('order_food/<int:food_id>/', OrderFood.as_view(), name='order_food'),
    path('order_food_cart/', OrderFoodCart.as_view(), name='order_food_cart'),
    path('order_report/', OrderHistoryReport.as_view(), name='order_report'),
    path('add_to_cart/<int:food_id>/', AddToCart.as_view(), name='add_to_cart'),
    path('review/<int:id>', UserReview.as_view(), name='review'),
    path('remove_cart/<int:cart_id>', RemoveFromCart.as_view(), name='remove_cart'),
    path('cart_report/', CartReport.as_view(), name='cart_report'),
    path('specials/', SpecialItems, name='specials'),
    path('special_category/<slug:category_slug>/', SpecialItems, name='special_food_category'),
    path('food_reviews/<int:id>', FoodReview.as_view(), name='food_review'),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)