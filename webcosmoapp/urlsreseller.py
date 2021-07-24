from os import name
from webcosmoapp.viewsadmin import dashboard
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import viewsreseller

app_name = 'webcosmoappreseller'

urlpatterns = [
        path('', viewsreseller.index, name="index"),
        path('login/', viewsreseller.login, name="login"),
        path('register/', viewsreseller.register, name="register"),
        path('dashboard/', viewsreseller.dashboard, name="dashboard"),
        path('detail/<str:id_produk>/', viewsreseller.detail_produk, name="detail_produk"),
        path('belanjaproduk/', viewsreseller.belanjaproduk, name="belanjaproduk"),
        path('addreseller/', viewsreseller.addreseller, name="addreseller"),
        path('authreseller/', viewsreseller.authreseller, name="authreseller"),
        path('aturakun/', viewsreseller.aturakun, name="aturakun"),
        path('changereseller/', viewsreseller.changereseller, name="changereseller"),
        path('addalamat/', viewsreseller.addalamat, name="addalamat"),
        path('addnik/', viewsreseller.addnik, name="addnik"),
        path('addbank/', viewsreseller.addbank, name="addbank"),
        path('buy/<str:id_produk>/', viewsreseller.buy, name="buy"),
        path('logout/', viewsreseller.logout, name="logout"),
        path('statistik/', viewsreseller.statistik, name="statistik"),
        path('listpesanan/', viewsreseller.listpemesanan, name="listpesanan"),
        path('keranjang/', viewsreseller.keranjang, name="keranjang"),
        path('reward/', viewsreseller.reward, name="reward"),
        path('gantipassword/', viewsreseller.gantipassword, name="gantipassword")
]