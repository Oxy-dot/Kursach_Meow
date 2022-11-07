from django.urls import include, path
import django.contrib.auth.urls
from django.contrib import admin
from users.views import *
urlpatterns = [
    # Главная страница
    path('', Home, name='home'),
    # Авторизация
    path('signin/', SignInView.as_view(),name="Reg"),
    path('signup/', SignUp,name="Login"),
    path('admin/',admin.site.urls),
    path('user/logout/',LogoutUser,name="Logout"),
    # Отображение товаров
    path('product/<str:filter>',ShowProduct,name="showproduct"),
    path('product/productcard/<int:id>',ShowProductCard,name="showproductcard"),
    # Профиль
    path('profile/', ShowProfile, name='showProfile'),
    path('profile/basket',ShowBasket, name='showBasket'),
    path('profile/liked', ShowLiked,name='showWhatYouLike'),
    path('', include('django.contrib.auth.urls')),
    # Менеджмент товаров
    path('product/likeProduct/<int:id>',LikeProduct,name="add in like"),
    path('product/addToBasket/<int:id>',AddToBasket, name="add in basket"),
    path('profile/checkout/<str:prodid>',checkout),
]