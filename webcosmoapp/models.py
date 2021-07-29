from os import pardir
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import related
from django.db.models.fields.related import RelatedField
from django.db.models.lookups import LessThan
from django.db.models.query_utils import subclasses
from django.utils import tree

# Create your models here.
class Produk(models.Model):
    id = models.AutoField(primary_key=True)
    id_produk = models.CharField(max_length=30)
    nama_produk = models.CharField(max_length=100)
    harga_produk = models.BigIntegerField()
    kategori = models.ForeignKey('webcosmoapp.Kategori', on_delete=models.CASCADE, related_name='produkid_kategori')
    sub_kategori = models.ForeignKey('webcosmoapp.Sub_Kategori', on_delete=models.CASCADE, related_name='produkid_sub_kategori')
    stok = models.IntegerField(null=True)
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()
    status =  models.CharField(null=True, max_length=2, default='1')
    id_detail = models.ForeignKey('webcosmoapp.Detail_Produk', on_delete=models.CASCADE, related_name='detail_produkid', null=True)
    
    def __str__(self):
        return self.nama_produk

class Foto_Produk(models.Model):
    id = models.AutoField(primary_key=True)
    id_foto = models.CharField(max_length=30)
    id_produk = models.ForeignKey('webcosmoapp.Produk', on_delete=models.CASCADE, related_name='fotoprodukid', null=True)
    dir_foto = models.FileField(upload_to='foto_produk')
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()

    def __str__(self):
        return self.dir_foto

class Detail_Produk(models.Model):
    id = models.AutoField(primary_key=True)
    id_produk = models.ForeignKey('webcosmoapp.Produk', on_delete=models.CASCADE, related_name='detailprodukid')
    kode_produk = models.CharField(max_length=30, null=True)
    desk_produk = models.TextField()
    thumb_image = models.FileField(upload_to='thumbnail_produk')
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()

    def __str__(self):
        return self.id_produk

class Kategori(models.Model):
    id = models.AutoField(primary_key=True)
    id_kategori = models.CharField(max_length=30)
    kategori = models.CharField(max_length=100)
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()
    status = models.CharField(max_length=2, default='1', null=True)

    def __str__(self):
        return self.kategori

class Sub_Kategori(models.Model):
    id = models.AutoField(primary_key=True)
    id_subKat = models.CharField(max_length=30)
    sub_kategori = models.CharField(max_length=100)
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()
    id_kategori = models.ForeignKey('webcosmoapp.Kategori', on_delete=models.CASCADE, related_name='kategorisubid', null=True)
    status = models.CharField(max_length=2, default='1')

    def __str__(self):
        return self.sub_kategori

class Reseller(models.Model):
    id = models.AutoField(primary_key=True)
    id_reseller = models.CharField(max_length=30)
    nama_depan = models.CharField(max_length=100)
    nama_belakang = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    no_telp = models.CharField(max_length=15)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=200)
    status = models.CharField(max_length=30)
    kebijakan = models.IntegerField(max_length=2)
    subscribe = models.IntegerField(max_length=2)
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()
    jk = models.CharField(max_length=2, null=True)
    dir_image = models.FileField(upload_to='pp_reseller', default='pp_reseller/default.png')

    def __str__(self):
        return self.nama_depan

class Alamat(models.Model):
    id = models.AutoField(primary_key=True)
    id_alamat = models.CharField(max_length=30)
    id_user = models.CharField(max_length=30)
    label = models.CharField(max_length=100)
    provinsi = models.TextField()
    kotakab = models.TextField()
    kecamatan = models.TextField()
    kelurahan = models.TextField()
    kodepos = models.IntegerField(max_length=30)
    status = models.IntegerField(max_length=2)
    alamat_lengkap = models.TextField()
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()

    def __str__(self):
        return self.id_alamat

    
class Detail_Reseller(models.Model):
    id = models.AutoField(primary_key=True)
    id_reseller_detail = models.CharField(max_length=30)
    id_reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE)
    alamat_user = models.ForeignKey('webcosmoapp.Alamat', on_delete=models.CASCADE, related_name='id_alamat_user', null=True)
    tanggal_lahir = models.CharField(max_length=20, null=True)
    id_bank = models.ForeignKey('webcosmoapp.Account_Bank', on_delete=models.CASCADE, related_name='bankid', null=True)
    id_nik = models.ForeignKey('webcosmoapp.Nik', on_delete=models.CASCADE, related_name='nikid', null=True)
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()

    def __str__(self):
        return self.id_reseller_detail

class Account_Bank(models.Model):
    id = models.AutoField(primary_key=True)
    id_bank = models.CharField(max_length=30)
    id_user = models.CharField(max_length=30)
    nama_bank = models.CharField(max_length=100)
    no_rekening = models.BigIntegerField(max_length=30)
    id_nik = models.ForeignKey('webcosmoapp.Nik', on_delete=models.CASCADE, related_name='banknikid')
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()

    def __str__(self):
        return self.id_bank

class Ulasan(models.Model):
    id = models.AutoField(primary_key=True)
    id_ulasan = models.CharField(max_length=30)
    id_user = models.ForeignKey('webcosmoapp.Reseller', on_delete=models.CASCADE, related_name='ulasanuserid')
    id_produk = models.ForeignKey('webcosmoapp.Produk', on_delete=models.CASCADE, related_name='ulasanprodukid')
    id_ranting = models.ForeignKey('webcosmoapp.Ranting', on_delete=models.CASCADE, related_name='rantingid')
    ulasan = models.TextField()
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()

    def __str__(self):
        return self.ulasan

class Ranting(models.Model):
    id = models.AutoField(primary_key=True)
    id_ranting = models.CharField(max_length=30)
    id_user = models.ForeignKey('webcosmoapp.Reseller', on_delete=models.CASCADE, related_name='rantinguserid')
    id_produk = models.ForeignKey('webcosmoapp.Produk', on_delete=models.CASCADE, related_name='rantingprodukid')
    score = models.CharField(max_length=20)
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()

    def __str__(self):
        return self.score

class Nik(models.Model):
    id = models.AutoField(primary_key=True)
    id_nik = models.CharField(max_length=30)
    id_user = models.ForeignKey('webcosmoapp.Reseller', on_delete=models.CASCADE, related_name='nikuserid')
    no_nik = models.BigIntegerField()
    dir_nik = models.FileField(upload_to='ktp')
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()

    def __str__(self):
        return self.no_nik

class Kurir(models.Model):
    id = models.AutoField(primary_key=True)
    id_kurir = models.CharField(max_length=30)
    nama_kurir = models.CharField(max_length=100)
    jenis_pengiriman = models.CharField(max_length=100)
    estimasi = models.CharField(max_length=100)
    ongkir = models.CharField(max_length=50)
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()
    status = models.CharField(max_length=2, default='1')

    def __str__(self):
        return self.nama_kurir

class Trolly(models.Model):
    id = models.AutoField(primary_key=True)
    id_trolly = models.CharField(max_length=30)
    id_produk = models.ForeignKey('webcosmoapp.Produk', related_name='trollyprodukid', on_delete=models.CASCADE)
    id_user = models.ForeignKey('webcosmoapp.Reseller', related_name='trollyuserid', on_delete=models.CASCADE)
    status = models.IntegerField(max_length=2)
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()

    def __str__(self):
        return self.id_trolly

class Discount(models.Model):
    id = models.AutoField(primary_key=True)
    id_discount = models.CharField(max_length=30)
    id_produk = models.ForeignKey('webcosmoapp.Produk', related_name='discountprodukid', on_delete=models.CASCADE)
    potongan = models.BigIntegerField(max_length=50)
    status = models.IntegerField(max_length=2)
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()

    def __str__(self):
        return self.id_potongan

class Pemesanan(models.Model):
    id = models.AutoField(primary_key=True)
    id_pemesanan = models.CharField(max_length=30)
    id_produk = models.ForeignKey('webcosmoapp.Produk', related_name='pemesananprodukid', on_delete=models.CASCADE)
    id_user = models.ForeignKey('webcosmoapp.Reseller', related_name='pemesananuserid', on_delete=models.CASCADE)
    invoice = models.CharField(max_length=100)
    qty = models.IntegerField(max_length=10)
    sub_total = models.BigIntegerField()
    status = models.CharField(max_length=100)
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()
    id_pengiriman = models.CharField(max_length=30, null=True)
    id_bank = models.CharField(max_length=30, null=True)
    id_alamat = models.CharField(max_length=30, null=True)
    pengirimanid = models.ForeignKey('webcosmoapp.Pengiriman', related_name='pengirimanid', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.invoice

class Pembayaran(models.Model):
    id = models.AutoField(primary_key=True)
    id_pembayaran = models.CharField(max_length=30)
    id_pemesanan = models.ForeignKey('webcosmoapp.Pemesanan', related_name='pembayaranpemesananid', on_delete=models.CASCADE)
    id_user = models.ForeignKey('webcosmoapp.Reseller', related_name='userid', on_delete=models.CASCADE)
    id_buktipem = models.ForeignKey('webcosmoapp.Bukti_Pembayaran', related_name='pembayaranbuktipemid', on_delete=models.CASCADE, null=True)
    harga_total = models.BigIntegerField()
    status = models.CharField(max_length=100)
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()

    def __str__(self):
        return self.id_pembayaran

class Bukti_Pembayaran(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.CharField(max_length=30)
    via = models.CharField(max_length=30)
    id_pembayaran = models.ForeignKey('webcosmoapp.Pembayaran', related_name='buktipem_pembayaran', on_delete=models.CASCADE)
    id_pemesanan = models.ForeignKey('webcosmoapp.Pemesanan', related_name='buktipem_pemesanan', on_delete=models.CASCADE)
    dir_image = models.FileField(upload_to='buktipembayaran')
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()

    def __str__(self):
        return self.via


class Pengiriman(models.Model):
    id = models.AutoField(primary_key=True)
    id_pengiriman = models.CharField(max_length=30)
    id_pemesanan = models.ForeignKey('webcosmoapp.Pemesanan', related_name='pengirimanpemesananid', on_delete=models.CASCADE)
    id_pembayaran = models.ForeignKey('webcosmoapp.Pembayaran', related_name='pengirimanpemebayaranid', on_delete=models.CASCADE)
    id_user = models.ForeignKey('webcosmoapp.Reseller', related_name='pengirimanuserid', on_delete=models.CASCADE)
    via_kurir = models.ForeignKey('webcosmoapp.Kurir', related_name='pengirimankuririd', on_delete=models.CASCADE)
    resi = models.CharField(max_length=150, null=True)
    status = models.CharField(max_length=100)
    tanggal_pengiriman = models.CharField(max_length=100, null=True)
    tanggal_tiba = models.CharField(max_length=100, null=True)
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()

    def __str__(self):
        return self.id_pengiriman

class Dropshipper(models.Model):
    id = models.AutoField(primary_key=True)
    id_dropshipper = models.CharField(max_length=30)
    nama_depan = models.CharField(max_length=100)
    nama_belakang = models.CharField(max_length=100)
    email = models.CharField(max_length=90)
    no_telp = models.CharField(max_length=15)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=150)
    status = models.CharField(max_length=100)
    kebijakan = models.IntegerField(max_length=2)
    subscribe = models.IntegerField(max_length=2)
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()

    def __str__(self):
        return self.id_dropshipper

class Dropshipper_Detail(models.Model):
    id = models.AutoField(primary_key=True)
    id_dropshipper_detail = models.CharField(max_length=30)
    id_dropshipper = models.ForeignKey('webcosmoapp.Dropshipper', related_name='detaildropshipperid', on_delete=models.CASCADE)
    alamat_user = models.ForeignKey('webcosmoapp.Alamat', related_name='detailalamatid', on_delete=models.CASCADE)
    id_nik = models.ForeignKey('webcosmoapp.Nik', related_name='detailnikid', on_delete=models.CASCADE)
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()

    def __str__(self):
        return self.id_dropshipper_detail

class Invite_Dropshiper(models.Model):
    id = models.AutoField(primary_key=True)
    id_invite = models.CharField(max_length=30)
    id_reseller = models.ForeignKey('webcosmoapp.Reseller', related_name='inviteresellerid', on_delete=models.CASCADE)
    id_dropshipper = models.ForeignKey('webcosmoapp.Dropshipper', related_name='invitedropshipperid', on_delete=models.CASCADE)
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()

    def __str__(self):
        return self.id_invite

class Pemesanan_Dropshipper(models.Model):
    id = models.AutoField(primary_key=True)
    id_pemesanan_drop = models.CharField(max_length=30)
    id_reseller = models.ForeignKey('webcosmoapp.Reseller', related_name='pemedropresellerid', on_delete=models.CASCADE)
    id_dropshipper = models.ForeignKey('webcosmoapp.Dropshipper', related_name='pemedropdropshipperid', on_delete=models.CASCADE)
    id_produk = models.ForeignKey('webcosmoapp.Produk_Reseller', related_name='pemedropprodukid', on_delete=models.CASCADE)
    qty = models.IntegerField(max_length=50)
    sub_total = models.BigIntegerField()
    status = models.CharField(max_length=100)
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()

    def __str__(self):
        return self.id_pemesanan_drop


class Pemesanan_EndUser(models.Model):
    id = models.AutoField(primary_key=True)
    id_pemesanan_enduser = models.CharField(max_length=30)
    id_reseller = models.ForeignKey('webcosmoapp.Reseller', related_name='pemeendresellerid', on_delete=models.CASCADE)
    id_enduser = models.CharField(max_length=30)
    id_produk = models.ForeignKey('webcosmoapp.Produk', related_name='pemeendprodukid', on_delete=models.CASCADE)
    invoice = models.CharField(max_length=100)
    qty = models.IntegerField(max_length=10)
    subtotal = models.BigIntegerField()
    status = models.CharField(max_length=2)
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()
    nama_enduser = models.CharField(max_length=100, null=True)
    alamat = models.CharField(max_length=100,  null=True)
    pembayaran = models.CharField(max_length=100,  null=True)
    pengiriman = models.CharField(max_length=100,  null=True)

    def __str__(self):
        return self.id_pemesanan_enduser


class Point(models.Model):
    id = models.AutoField(primary_key=True)
    id_point = models.CharField(max_length=30)
    id_reseller = models.ForeignKey('webcosmoapp.Reseller', related_name='pointresellerid', on_delete=models.CASCADE)
    point = models.CharField(max_length=30)
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()

    def __str__(self):
        return self.point

class Reward(models.Model):
    id = models.AutoField(primary_key=True)
    id_reward = models.CharField(max_length=30)
    nama_reward = models.CharField(max_length=150)
    desk_reward = models.TextField()
    jenis_reward = models.CharField(max_length=30)
    harga_reward = models.CharField(max_length=100)
    point = models.CharField(max_length=30)
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()

    def __str__(self):
        return self.nama_reward

class Pembayaran_Dropshipper(models.Model):
    id = models.AutoField(primary_key=True)
    id_pemb_dropshipper = models.CharField(max_length=30)
    id_reseller = models.ForeignKey('webcosmoapp.Reseller', related_name='pembdropresellerid', on_delete=models.CASCADE)
    id_dropshipper = models.ForeignKey('webcosmoapp.Dropshipper', related_name='pembdropdropshipperid', on_delete=models.CASCADE)
    id_pemesanan = models.ForeignKey('webcosmoapp.Pemesanan_Dropshipper', related_name='pembdroppemesanandropid', on_delete=models.CASCADE)
    harga_total = models.CharField(max_length=100)
    status = models.CharField(max_length=2)
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()

    def __str__(self):
        return self.id_pemb_dropshipper


class Pesan(models.Model):
    id = models.AutoField(primary_key=True)
    id_pesan = models.CharField(max_length=30)
    judul = models.CharField(max_length=150)
    deskripsi = models.TextField()
    dir_foto = models.CharField(max_length=150)
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()

    def __str__(self):
        return self.judul

class Notifikasi_Admin(models.Model):
    id = models.AutoField(primary_key=True)
    id_notifikasi = models.CharField(max_length=30)
    notifikasi = models.TextField()
    status = models.CharField(max_length=2)
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()

    def __str__(self):
        return self.notifikasi

class Produk_Reseller(models.Model):
    id = models.AutoField(primary_key=True)
    id_produk_reseller = models.CharField(max_length=30)
    id_reseller = models.ForeignKey('webcosmoapp.Reseller', related_name='produkre_resellerid', on_delete=models.CASCADE)
    id_produk = models.ForeignKey('webcosmoapp.Produk', related_name='produkre_produkid', on_delete=models.CASCADE)
    qty = models.IntegerField(max_length=100)
    harga_komisi = models.CharField(max_length=100)
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()

    def __str__(self):
        return self.id_produk_reseller

class Komisi(models.Model):
    id = models.AutoField(primary_key=True)
    id_komisi = models.CharField(max_length=30)
    id_reseller = models.ForeignKey('webcosmoapp.Reseller', related_name='komisiresellerid', on_delete=models.CASCADE)
    komisi = models.BigIntegerField(0)
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()

    def __str__(self):
        return self.komisi

class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    id_admin = models.CharField(max_length=30)
    nama = models.CharField(max_length=100)
    dir_foto = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    username = models.CharField(max_length=30)
    password = models.TextField()
    tanggal = models.DateTimeField()
    tanggal_update = models.DateTimeField()

    def __str__(self):
        return self.nama




