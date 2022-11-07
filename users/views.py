import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import HttpResponse, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from .forms import CustomUserCreateForm, Login
from .models import *

# Create your views here.

class SignInView(CreateView):
    form_class = CustomUserCreateForm
    success_url = reverse_lazy('homepage')
    template_name = "registration/login.html"

    def post(self, request, *args, **kwargs):
        form = CustomUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            return redirect('/')
        else:
            return render(request, self.template_name, {'form':form})

def SignUp(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = Login()
        if request.method == "POST":
            form = Login(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/')
                else:
                    messages.error(request, 'Логин или пароль мяумяу.')
                    return render(request,"registration/login.html", {"form":form,"message" : messages})
            else:
                messages.error(request, 'Логин или пароль woofwoof.')
                return HttpResponse("fafjasfkasfkasjk")
                # return render(request, "registration/login.html", {"form": form, "message": messages})
        else:
            return render(request,'registration/login.html', {'form':form,'method':'log'})

def LogoutUser(request):
    logout(request)
    return redirect('/')

def ShowProductCard(request,id):
    product = Product.objects.filter(id=id)[0]
    specText = Specifications.objects.filter(idProduct=product)[0]
    return render(request,'ProductCard.html',context={'productName':product.name,'smallSpecText':specText.shortSpecification, 'specText':specText.fullSpecification, 'photoLink':"images/ProductImages/"+product.photoLink,'id':product.id})

def ShowProduct(request,filter):
    cards = []
    productType = ProductType.objects.filter(typeName=filter)[0]
    if(Product.objects.filter(productType=productType).count()!=0):
        table = Product.objects.filter(productType=productType)
    else:
        return HttpResponse('Не правильно введён тип продукта, попробуйте ещё раз')

    for row in table:
        cards.append({"photoLink": 'images/ProductImages/' + row.photoLink, "Name": row.name,
                      "Cost": row.price, "id": row.id})
    return render(request, "catalog.html", context={"cards": cards})

def ShowProfile(request):
    if request.user.is_authenticated:
        currentUser = CustomUser.objects.filter(id=request.user.id)[0]
        return render(request,"Profile.html",context={"fio":currentUser.fullName,"email":currentUser.email,"phoneNumber":currentUser.phoneNumber,"adress":currentUser.adress})
    else:
        return render(request,'error.html')

def error(request):
    return render(request,'error.html')

def ShowBasket(request):
    if request.user.is_authenticated:
        cards = []
        if(request.method == "POST"):
            mas = ""
            productid = request.POST.getlist('basket')
            for i in productid:
                mas += i
            return redirect('checkout/' + mas)
        else:
            basketProduct = Basket.objects.filter(idUser_id=request.user.id)
            for row in basketProduct:
                specfic = Specifications.objects.filter(idProduct=row.idProduct)
                product = Product.objects.filter(id=row.idProduct_id)[0]
                if Product.objects.filter(id = row.idProduct.id)[0].count > 0:
                    cards.append({"photoLink": '/images/ProductImages/' + product.photoLink, "Name": product.name,
                              "smallSpec": specfic[0].shortSpecification,
                              "price": product.price, "id": product.id})
                else:
                    cards.append({"photoLink": '/images/ProductImages/' + product.photoLink, "Name": product.name,
                                  "smallSpec": specfic[0].shortSpecification,
                                  "price": 'Товар отсутсвтует', "id": product.id})
            return render(request, "Basket.html", context={"cards": cards, 'count': len(cards)})
    else:
        render(request,'error.html')


def checkout(request,prodid):
    if(request.method == "POST"):
        for i in range(len(prodid)):
            if(Purchases.objects.last() == None):
                purchase = Purchases(1,datetime.date.today(),"Оплачен",prodid[i],request.user.id)
            else:
                purchase = Purchases(id=int(Purchases.objects.latest('id').id) + 1 ,datePurchase=datetime.date.today(), orderStage="Оплачен", idProduct=Product.objects.filter(id=prodid[i])[0], idUser=CustomUser.objects.filter(id=request.user.id)[0])
            purchase.save()
            Product.objects.filter(id=prodid[i]).update(count=(Product.objects.filter(id=prodid[i])[0].count)-1)
            basket = Basket.objects.filter(idUser=request.user.id) & Basket.objects.filter(idProduct=prodid[i])
            basket.delete()
        return redirect('/')
    else:
        cost = 0.0
        for i in range(len(prodid)):
            cost+= float(Product.objects.filter(id=prodid[i])[0].price)
        count = len(prodid)
        email = CustomUser.objects.filter(id=request.user.id)[0].email
        name = str.split(' ',CustomUser.objects.filter(id=request.user.id)[0].fullName)[0]
        secname = str.split(' ', CustomUser.objects.filter(id=request.user.id)[0].fullName)[1]
        return render(request, 'checkout.html',context={'cost':cost,'count':count,'email':email,'name':name,'secname':secname})
def ShowLiked(request):
    return render()

def LikeProduct(request,id):
    if(request.method == "POST"):
        curProduct = LikedProducts.objects.filter(userId=CustomUser.objects.filter(id=request.user.id)[0].id) & LikedProducts.objects.filter(productId=Product.objects.filter(id=id)[0].id)
        if(len(curProduct) == 0):
            try:
                likedProduct = LikedProducts((LikedProducts.objects.last()).id+1,
                                             CustomUser.objects.filter(id=request.user.id)[0].id,
                                             Product.objects.filter(id=id)[0].id)
            except ObjectDoesNotExist:
                likedProduct = LikedProducts(1,
                                             CustomUser.objects.filter(id=request.user.id)[0].id,
                                             Product.objects.filter(id=id)[0].id)

            likedProduct.save()
            return redirect("/product/smartphones")
        else:
            curProduct.delete()
            return redirect("/product/smartphones")
    else:
        return redirect('/')

def AddToBasket(request, id):
    if request.user.is_authenticated:
        if (request.method == "POST"):
            curProduct = Basket.objects.filter(idUser=CustomUser.objects.filter(id=request.user.id)[0].id) & Basket.objects.filter(idProduct=Product.objects.filter(id=id)[0].id)
            if (len(curProduct) == 0):
                try:
                    toBasket = Basket((Basket.objects.latest('id').id) + 1,
                                      CustomUser.objects.filter(id=request.user.id)[0].id,
                                      Product.objects.filter(id=id)[0].id, 1)
                except ObjectDoesNotExist:
                    toBasket = Basket(1,
                                      CustomUser.objects.filter(id=request.user.id)[0].id,
                                      Product.objects.filter(id=id)[0].id, 1)

                toBasket.save()
                return redirect("/product/smartphones")
            else:
                curProduct.delete()
                return redirect("/product/smartphones")
        else:
            return redirect('/')
    else:
        render(request,'error.html')

def Home(request):
    cards = []
    table = Product.objects.filter(isAdvertisement=True)
    for row in table:
        cards.append({"photoLink": 'images/ProductImages/' + row.photoLink, "Name": row.name,
                      "Cost": row.price})
    return render(request,"mainPage.html",context={"cards":cards,"imagesource":'/images/advertImages/Group16.png',"imagesource2":'/images/advertImages/Group17.png'})