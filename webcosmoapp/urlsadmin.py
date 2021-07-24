from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import viewsadmin

app_name = 'webcosmoapp'

urlpatterns = [
    path('', viewsadmin.index, name="index"),
    path('auth/', viewsadmin.auth, name="auth"),
    path('dashboard/', viewsadmin.dashboard, name="dashboard"),
    path('databarang/', viewsadmin.data_barang, name="databarang"),
    path('tambahbarang/', viewsadmin.tambah_barang, name="tambahbarang"),
    path('datareseller/', viewsadmin.data_reseller, name="datareseller"),
    path('tambahreseller/', viewsadmin.tambah_reseller, name="tambahreseller"),
    path('transaksireseller/', viewsadmin.transaksi_reseller, name="transaksireseller"),
    path('pemesanan/', viewsadmin.pemesanan, name="pemesanan"),
    path('pembayaran/', viewsadmin.pembayaran, name="pembayaran"),
    path('pengiriman/', viewsadmin.pengiriman, name="pengiriman"),
    path('pengaturan/', viewsadmin.pengaturan, name="pengaturan"),
    path('logout/', viewsadmin.logout, name="logout"),
    path('addbarang/', viewsadmin.addbarang, name='addbarang'),
    path('addkategori/', viewsadmin.addkategori, name="addkategori"),
    path('addsubkategori/', viewsadmin.addsubkategori, name="addsubkategori"),
    path('detailbarang/', viewsadmin.detailbarang, name="detailbarang"),
    path('editbarang/<str:id_barang>', viewsadmin.editbarang, name="editbarang"),
    path('changefoto/', viewsadmin.changefoto, name="changefoto"),
    path('changebarang/', viewsadmin.changebarang, name="changebarang"),
    path('detelebarang/', viewsadmin.detelebarang, name="detelebarang"),
    path('getkategori/', viewsadmin.getkategori, name="getkategori"),
    path('changekategori/', viewsadmin.changekategori, name="changekategori"),
    path('deletekategori/', viewsadmin.deletekategori, name="deletekategori"),
    path('getsubkategori/', viewsadmin.getsubkategori, name="getsubkategori"),
    path('changesubkategori/', viewsadmin.changesubkategori, name="changesubkategori"),
    path('deletesubkategori/', viewsadmin.deletesubkategori, name="deletesubkategori"),
    path('addkurir/', viewsadmin.addkurir, name="addkurir")
]