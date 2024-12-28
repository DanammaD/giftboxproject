from django.urls import path
from . import views
from giftbox import settings
from django.conf.urls.static import static
#from .views import SimpleView
#from ecomm_app import views

urlpatterns = [
    path('',views.home),
    path('register',views.register),
    path('login',views.userlogin),
    path('logout',views.userlogout),
    path('catfilter/<cv>',views.catfilter),
    path('productsearch',views.productsearch),
    path('contact',views.contact),
    path('product_details/<pid>',views.product_details),
    path('addtocart/<pid>',views.addtocart),
    path('cart',views.viewcart),
    path('sort/<sv>',views.sort),
    path('range',views.range),
    path('remove/<cid>',views.remove),
    path('placeorder',views.placeorder),
    path('viewcart',views.viewcart),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('makepayment',views.makepayment),
    path('sendmail/<uemail>',views.sendusermail)
    
]

if settings.DEBUG:
   urlpatterns+=static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)