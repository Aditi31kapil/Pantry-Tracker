"""
URL configuration for restaurant_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from restaurant import views as hv
from customer.views import Index, About ,Order, OrderConfirmation,OrderPayConfirmation
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', Index.as_view(),name='index'),
    path('about/',About.as_view(),name= 'about'),
    path('order/',Order.as_view(),name= 'order'),
    path('order-confirmation/<int:pk>',OrderConfirmation.as_view(),name= 'order-confirmation'),
    path('payment-confirmation/',OrderPayConfirmation.as_view(),name= 'payment-confirmation'),
    path('menu/',hv.menu,name= 'menu'),
    path('contact/',hv.contact,name= 'contact'),
    path('login/',hv.login,name= 'login'),
    path('book_table/', hv.book_table,name= 'book_table'),
    path('emp/',hv.emp,name= 'emp'),
    path('all_emp/',hv.all_emp,name = 'all_emp' ),
    path('add_emp/',hv.add_emp,name = 'add_emp' ),
    path('remove_emp/',hv.remove_emp,name = 'remove_emp' ),
    path('remove_emp/<int:employee_id>',hv.remove_emp,name = 'remove_emp' ),
    path('filter_emp/',hv.filter_emp,name = 'filter_emp' ),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
