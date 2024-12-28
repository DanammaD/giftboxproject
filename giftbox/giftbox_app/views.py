from django.shortcuts import render,HttpResponse,redirect
from .models import Product
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q
from .models import Cart,Order
import random
import razorpay

# Create your views here.
def home(request):
    #userid=request.user.id
    #print("logged in userid",+userid)
    #print(request.user.is_authenticated)
     #objects
    context={}
    p=Product.objects.filter(is_active=True) #objects
    print(p)
    context['products']=p
    return render(request,'index.html',context)

def register(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        context={}
        if uname=="" or upass=="" or ucpass=="":
           context['errmsg']="fields can not be empty"
        elif upass != ucpass:
            context['errmsg']="password and confirm password didn't matched"
        else:
            try:
                u=User.objects.create(password=upass,username=uname,email=uname)
                u.set_password(upass)
                u.save()
                context['success']="User created successfully"
            except Exception:
                context['errmsg']="Username already exist!"
        return render(request,'register.html',context)
    else:
        return render(request,'register.html')

def userlogin(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        context={}
        if uname=="" or upass=="":
           context['errmsg']="fields can not be empty"
           return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)        #session start
                return redirect('/')    #home
            else:
                context['errmsg']="Invalid Username & Password"
                return render(request,'login.html',context)
    else:
        return render(request,'login.html')

def userlogout(request):
    logout(request)
    return redirect('/')

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=Product.objects.filter(q1 & q2)
    print(p)     #2 objects
    context={}
    context['products']=p
    return render(request,'index.html',context)

def contact(request):
    return render(request,'contact.html')

def product_details(request,pid):
    p=Product.objects.filter(id=pid)
    context={}
    context['products']=p
    return render(request, 'product_details.html',context)

def addtocart(request,pid):
    if request.user.is_authenticated:
       userid=request.user.id
       #print(userid)
       u=User.objects.get(id=userid)
       #print(pid)
       p=Product.objects.get(id=pid)
       #print(u,p)
       #check product exist or not
       q1=Q(uid=u)
       q2=Q(pid=p)
       c=Cart.objects.filter(q1 & q2)
       #print(c)
       n=len(c)
       context={}
       if n==1:
           context['errmsg']="Product already exist in cart"
       else:
           c=Cart.objects.create(uid=u,pid=p)
           c.save()
           context['success']="Product added successfully"
       p=Product.objects.filter(id=pid)
       context['products']=p
       return render(request,'product_details.html',context)
    else:
        return redirect('/login')

def viewcart(request):
    c=Cart.objects.filter(uid=request.user.id)
    print(c)
    s=0
    for x in c:
        #print(x.pid.price)
        s=s+x.pid.price*x.qty
    np=len(c)
    context={}
    context['total']=s
    context['n']=np
    context['data']=c
    return render(request,'cart.html',context)

def remove(request,cid):   #1
    c=Cart.objects.filter(id=cid)       #id=1
    c.delete()
    return redirect('/viewcart')

def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    print(c)
    oid=random.randrange(1000,9999)
    print(oid)
    for x in c:
        #print(x)
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=request.user.id)
    context={}
    context['data']=orders
    np=len(orders)
    s=0
    for x in orders:
        s=s+x.pid.price*x.qty
    context['total']=s
    context['n']=np
    return render(request,'placeorder.html',context)

def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    print(c[0])
    print(c[0].qty)
    if qv == '1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    return redirect('/viewcart')

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=Product.objects.filter(q1 & q2 & q3)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def sort(request,sv):
    if sv == '0':
        col='price'
    else:
        col='price'
    p=Product.objects.filter(is_active=True).order_by(col)  
    context={}
    context['products']=p
    return render(request,'index.html',context)

def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    for x in orders:
        s=s+x.pid.price * x.qty
        oid=x.order_id
    #print(oid)
    #print(s)
    client=razorpay.Client(auth=("rzp_test_pjmfONoAV5hhRJ", "2qLFlWxOv0vaA1jxWEEHwbcA"))
    data = { "amount": s*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    #print(payment)
    uemail=request.user.email
    print(uemail)
    context={}
    context['data']=payment
    context['uemail']=uemail
    #return HttpResponse("Success")
    return render(request,'pay.html',context)

def sendusermail(request,uemail):
    msg="Order details are:"
    print(uemail)
    send_mail(
        "Gift Corner order placed successfully",
        msg,
        "danammad94@gmail.com",
        [],
        fail_silently=False,
    )
    return HttpResponse("Mail sent successfully")

def productsearch(request):
    pname=request.GET['pname']
    if pname=="cake":
        cat=1
        q1=Q(is_active=True)
        q2=Q(cat=cat)
        p=Product.objects.filter(q1 & q2)
    elif pname=="chocolates":
        cat=2
        q1=Q(is_active=True)
        q2=Q(cat=cat)
        p=Product.objects.filter(q1 & q2)
    elif pname=="flower":
        cat=3
        q1=Q(is_active=True)
        q2=Q(cat=cat)
        p=Product.objects.filter(q1 & q2)
    elif pname=="personlisedgift":
        cat=4
        q1=Q(is_active=True)
        q2=Q(cat=cat)
        p=Product.objects.filter(q1 & q2)
    elif pname=="plants":
        cat=5
        q1=Q(is_active=True)
        q2=Q(cat=cat)
        p=Product.objects.filter(q1 & q2)
    elif pname=="perfumes":
        cat=6
        q1=Q(is_active=True)
        q2=Q(cat=cat)
        p=Product.objects.filter(q1 & q2)
    else:
        p=Product.objects.filter(is_active=True)
    context={}
    context['products']=p
    return render(request,'index.html',context)