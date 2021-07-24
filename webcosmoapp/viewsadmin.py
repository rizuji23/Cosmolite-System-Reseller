from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.contrib.auth.models import User
import uuid
import datetime
from django.template.loader import render_to_string



def index(request):
    if request.session.has_key("username"):
        username = request.session['username']
        users = get_object_or_404(User, username=username)
        return HttpResponseRedirect(reverse('webcosmoapp:dashboard'))
    else:
        return render(request, 'cosmoadmin/login.html')

def auth(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            akun = User.objects.get(username=username)
            if check_password(password, akun.password):
                request.session['username'] = username
                return HttpResponseRedirect(reverse('webcosmoapp:dashboard'))
            else:
               messages.add_message(request, messages.ERROR, 'Username Atau Password Salah')
               return HttpResponseRedirect(reverse('webcosmoapp:index'))
        except User.DoesNotExist:
               messages.add_message(request, messages.ERROR, 'Username Atau Password Salah')
               return HttpResponseRedirect(reverse('webcosmoapp:index'))


def dashboard(request):
    if request.session.has_key("username"):
        username = request.session['username']
        users = get_object_or_404(User, username=username)
        return render(request, 'cosmoadmin/index.html', {'admin': users})
    else:
        if request.session.has_key("username"):
            del request.session['username']
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoapp:index'))
        else:
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoapp:index'))


def data_barang(request):
    if request.session.has_key("username"):
        username = request.session['username']
        users = get_object_or_404(User, username=username)
        databarang = Produk.objects.filter(status='1')
        return render(request, 'cosmoadmin/databarang.html', {'admin': users, 'databarang': databarang})
    else:
        if request.session.has_key("username"):
            del request.session['username']
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoapp:index'))
        else:
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoapp:index'))
    

def tambah_barang(request):
    if request.session.has_key("username"):
        username = request.session['username']
        users = get_object_or_404(User, username=username)
        kategori = Kategori.objects.all()
        sub_kategori = Sub_Kategori.objects.all()
        return render(request, 'cosmoadmin/tambah-b.html', {'admin': users, 'kategori': kategori, 'sub_kategori': sub_kategori})
    else:
        if request.session.has_key("username"):
            del request.session['username']
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoapp:index'))
        else:
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoapp:index'))
    
def addbarang(request):
    if request.method == 'POST':
        nama_barang = request.POST['nama_barang']
        stock = request.POST['stok']
        harga_satuan = request.POST['harga']
        kategori = request.POST['kategori']
        sub_kategori = request.POST['sub_kategori']
        desk_barang = request.POST['desk_barang']
        thumbnail = request.FILES['thumbnail_barang']
        gambar_barang = request.FILES.getlist('gambar_barang')

        id_produk = uuid.uuid4().hex[:6].upper()
        tanggal = datetime.datetime.now()

        add_barang = Produk(id_produk=id_produk, nama_produk=nama_barang, harga_produk=harga_satuan, tanggal=tanggal, tanggal_update=tanggal, kategori_id=kategori, sub_kategori_id=sub_kategori, stok=stock)

        if add_barang:
            add_barang.save()
            barang = Produk.objects.get(id_produk=id_produk)
            if barang:
                detail = Detail_Produk(desk_produk=desk_barang, thumb_image=thumbnail, tanggal=tanggal, tanggal_update=tanggal, id_produk_id=barang.id, kode_produk=id_produk)
                if detail:
                    detail.save()
                    dp = Detail_Produk.objects.get(kode_produk=id_produk)
                    p_up = Produk.objects.get(id_produk=id_produk)
                    p_up.id_detail_id = detail.id
                    p_up.save()
                    for gb in gambar_barang:
                        id_gambar = uuid.uuid4().hex[:6].upper()
                        fp = Foto_Produk(id_foto=id_gambar, dir_foto=gb, tanggal=tanggal, tanggal_update=tanggal, id_produk_id=barang.id)
                        fp.save()
                    messages.add_message(request, messages.SUCCESS, 'Data Barang Berhasil Disimpan.')
                    return HttpResponseRedirect(reverse('webcosmoapp:databarang'))
                else:
                    messages.add_message(request, messages.ERROR, 'Data Barang Gagal Disimpan.')
                    return HttpResponseRedirect(reverse('webcosmoapp:databarang'))
            else:
                messages.add_message(request, messages.ERROR, 'Data Barang Gagal Disimpan.')
                return HttpResponseRedirect(reverse('webcosmoapp:databarang'))
        else:
            messages.add_message(request, messages.ERROR, 'Data Barang Gagal Disimpan.')
            return HttpResponseRedirect(reverse('webcosmoapp:databarang'))
        
def addkategori(request):
    if request.method == 'POST':
        kategori = request.POST['kategori']

        id_kategori = uuid.uuid4().hex[:6].upper()
        tanggal = datetime.datetime.now()

        add_kategori = Kategori(id_kategori=id_kategori, kategori=kategori, tanggal=tanggal, tanggal_update=tanggal)
        
        if add_kategori:
            add_kategori.save()
            messages.add_message(request, messages.SUCCESS, 'Data Kategori Berhasil Disimpan.')
            return HttpResponseRedirect(reverse('webcosmoapp:pengaturan'))
        else:
            messages.add_message(request, messages.ERROR, 'Data Kategori Gagal Disimpan.')
            return HttpResponseRedirect(reverse('webcosmoapp:pengaturan'))

def addsubkategori(request):
    if request.method == 'POST':
        kategori = request.POST['kategori']
        sub_kategori = request.POST['sub_kategori']

        id_subKat = uuid.uuid4().hex[:6].upper()
        tanggal = datetime.datetime.now()

        add_subkategori = Sub_Kategori(id_subKat=id_subKat, sub_kategori=sub_kategori, tanggal=tanggal, tanggal_update=tanggal, id_kategori_id=kategori)
        
        if add_subkategori:
            add_subkategori.save()
            messages.add_message(request, messages.SUCCESS, 'Data Sub Kategori Berhasil Disimpan.')
            return HttpResponseRedirect(reverse('webcosmoapp:pengaturan'))
        else:
            messages.add_message(request, messages.ERROR, 'Data Sub Kategori Gagal Disimpan.')
            return HttpResponseRedirect(reverse('webcosmoapp:pengaturan'))

def detailbarang(request):
    if request.method == 'POST':
        if request.session.has_key("username"):
            username = request.session['username']
            user = get_object_or_404(User, username=username)
            id_produk = request.POST['id']
            databarang = Produk.objects.get(id_produk=id_produk)
            detailproduk = Detail_Produk.objects.get(id_produk=databarang.id)
            kategori = Kategori.objects.get(id=databarang.kategori_id)
            sub_kategori = Sub_Kategori.objects.get(id=databarang.sub_kategori_id)
            foto_produk = Foto_Produk.objects.filter(id_produk=databarang.id)
            context = {'db': databarang, 'kategori': kategori, 'sub_kategori': sub_kategori, 'detailp': detailproduk, 'fp': foto_produk}
            html_form = render_to_string('cosmoadmin/modal/detailbarang.html', context, request=request)
            return JsonResponse({'datas': html_form})

        else:
            if request.session.has_key("username"):
                del request.session['username']
                messages.add_message(request, messages.ERROR, 'Harus Login!!')
                return HttpResponseRedirect(reverse('webcosmoapp:index'))
            else:
                messages.add_message(request, messages.ERROR, 'Harus Login!!')
                return HttpResponseRedirect(reverse('webcosmoapp:index'))

def editbarang(request, id_barang):
    if request.session.has_key("username"):
        username = request.session['username']
        users = get_object_or_404(User, username=username)
        databarang = Produk.objects.get(id_produk=id_barang)
        detailproduk = Detail_Produk.objects.get(id_produk=databarang.id)
        kategori = Kategori.objects.all()
        sub_kategori = Sub_Kategori.objects.all()
        foto_produk = Foto_Produk.objects.filter(id_produk=databarang.id)
        return render(request, 'cosmoadmin/editbarang.html', {'admin': users, 'db': databarang, 'kategori': kategori, 'sub_kategori': sub_kategori, 'detailp': detailproduk, 'fp': foto_produk})
    else:
        if request.session.has_key("username"):
            del request.session['username']
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoapp:index'))
        else:
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoapp:index'))

def changefoto(request):
    if request.method == 'POST':
        if request.session.has_key("username"):
            username = request.session['username']
            user = get_object_or_404(User, username=username)
            id_foto = request.POST['dataproduk']
            id_produk = request.POST['idproduk']
            foto = Foto_Produk.objects.get(id_foto=id_foto)
            editfoto = request.FILES['editfoto']
            tanggal = datetime.datetime.now()
            if editfoto:
                fotopro = Foto_Produk.objects.get(id_foto=id_foto)
                fotopro.dir_foto = editfoto
                fotopro.tanggal_update = tanggal
                if fotopro:
                    fotopro.save()
                    messages.add_message(request, messages.SUCCESS, 'Foto berhasil diubah...')
                    return HttpResponseRedirect(reverse('webcosmoapp:editbarang', args=(id_produk, )))
                else:
                    messages.add_message(request, messages.ERROR, 'Foto gagal diubah...')
                    return HttpResponseRedirect(reverse('webcosmoapp:editbarang', args=(id_produk, )))
            else:
                messages.add_message(request, messages.ERROR, 'Terjadi kesalahan difields Edit Foto!!')
                return HttpResponseRedirect(reverse('webcosmoapp:editbarang', args=(id_produk, )))
        else:
            if request.session.has_key("username"):
                del request.session['username']
                messages.add_message(request, messages.ERROR, 'Harus Login!!')
                return HttpResponseRedirect(reverse('webcosmoapp:index'))
            else:
                messages.add_message(request, messages.ERROR, 'Harus Login!!')
                return HttpResponseRedirect(reverse('webcosmoapp:index'))
    else:
        messages.add_message(request, messages.ERROR, '403 forhibidden')
        return HttpResponseRedirect(reverse('webcosmoapp:dashboard'))

def changebarang(request):
    if request.method == 'POST':
        if request.session.has_key('username'):
            username = request.session['username']
            user = get_object_or_404(User, username=username)
            id_produk = request.POST['produk']
            produk = Produk.objects.get(id_produk=id_produk)
            nama_barang = request.POST['nama_barang']
            stock = request.POST['stok']
            harga_satuan = request.POST['harga']
            kategori = request.POST['kategori']
            sub_kategori = request.POST['sub_kategori']
            desk_barang = request.POST['desk_barang']
            detailproduk = Detail_Produk.objects.get(id_produk=produk.id)
            thumbnail = request.FILES.get('thumbnail_barang', detailproduk.thumb_image)
            tanggal = datetime.datetime.now()

            if thumbnail == '':
                pro = Produk.objects.get(id_produk=id_produk)
                pro.nama_barang = nama_barang
                pro.harga_satuan = harga_satuan
                pro.kategori_id = kategori
                pro.sub_kategori_id = sub_kategori
                pro.stok = stock
                pro.tanggal_update = tanggal
                if pro.save():
                    detailpro = Detail_Produk.objects.get(id_produk=produk.id)
                    detailpro.desk_produk = desk_barang
                    detailpro.thumb_image = detailproduk.thumb_image
                    detailpro.tanggal_update = tanggal

                    if detailpro.save():
                        messages.add_message(request, messages.SUCCESS, 'Data barang sudah diedit...')
                        return HttpResponseRedirect(reverse('webcosmoapp:databarang'))
                    else:
                        messages.add_message(request, messages.ERROR, 'Data barang gagal diedit!!')
                        return HttpResponseRedirect(reverse('webcosmoapp:editbarang', args=(id_produk,)))
                else:
                    messages.add_message(request, messages.ERROR, 'Terjadi kesalahan pada penambahan data Produk!!')
                    return HttpResponseRedirect(reverse('webcosmoapp:editbarang', args=(id_produk,)))
            else:
                pro = Produk.objects.get(id_produk=id_produk)
                pro.nama_produk = nama_barang
                pro.harga_satuan = harga_satuan
                pro.kategori_id = kategori
                pro.sub_kategori_id = sub_kategori
                pro.stok = stock
                pro.tanggal_update = tanggal
                if pro:
                    pro.save()
                    detailpro = Detail_Produk.objects.get(id_produk=produk.id)
                    detailpro.desk_produk = desk_barang
                    detailpro.thumb_image = thumbnail
                    detailpro.tanggal_update = tanggal

                    if detailpro:
                        detailpro.save()
                        messages.add_message(request, messages.SUCCESS, 'Data barang sudah diedit...')
                        return HttpResponseRedirect(reverse('webcosmoapp:databarang'))
                    else:
                        messages.add_message(request, messages.ERROR, 'Data barang gagal diedit!!')
                        return HttpResponseRedirect(reverse('webcosmoapp:editbarang', args=(id_produk,)))
                else:
                    messages.add_message(request, messages.ERROR, 'Terjadi kesalahan pada penambahan data Produk!!')
                    return HttpResponseRedirect(reverse('webcosmoapp:editbarang', args=(id_produk,)))
        else:
            if request.session.has_key("username"):
                del request.session['username']
                messages.add_message(request, messages.ERROR, 'Harus Login!!')
                return HttpResponseRedirect(reverse('webcosmoapp:index'))
            else:
                messages.add_message(request, messages.ERROR, 'Harus Login!!')
                return HttpResponseRedirect(reverse('webcosmoapp:index'))
    else:
        messages.add_message(request, messages.ERROR, '403 forhibidden')
        return HttpResponseRedirect(reverse('webcosmoapp:dashboard'))

def detelebarang(request):
    if request.method == 'POST':
        if request.session.has_key('username'):
            username = request.session['username']
            user = get_object_or_404(User, username=username)
            id_produk = request.POST['id']
            produk = Produk.objects.get(id_produk=id_produk)
            if produk:
                produk.status = '0'
                produk.save()
                return HttpResponseRedirect(reverse('webcosmoapp:databarang'))
            else:
                messages.add_message(request, messages.ERROR, 'Terjadi kesalahan pada menghapus data Produk!!')
        else:
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoapp:index'))
    else:
        messages.add_message(request, messages.ERROR, '403 forhibidden')
        return HttpResponseRedirect(reverse('webcosmoapp:dashboard'))   

def getkategori(request):
    if request.method == 'POST':
        if request.session.has_key('username'):
            username = request.session['username']
            user = get_object_or_404(User, username=username)
            id_kategori = request.POST['id']
            kategori = Kategori.objects.get(id_kategori=id_kategori, status='1')
            context = {'kategori':kategori}
            html_form = render_to_string('cosmoadmin/modal/editkategori.html', context, request=request)
            return JsonResponse({'datas': html_form})
        else:
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoapp:index'))
    else:
        messages.add_message(request, messages.ERROR, '403 forhibidden')
        return HttpResponseRedirect(reverse('webcosmoapp:dashboard'))

def getsubkategori(request):
    if request.method == 'POST':
        if request.session.has_key('username'):
            username = request.session['username']
            user = get_object_or_404(User, username=username)
            id_subkategori = request.POST['id']
            subkategori = Sub_Kategori.objects.get(id_subKat=id_subkategori)
            kategori = Kategori.objects.filter(status='1')
            context = {'subkategori':subkategori, 'kategori': kategori}
            html_form = render_to_string('cosmoadmin/modal/editsubkategori.html', context, request=request)
            return JsonResponse({'datas': html_form})
        else:
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoapp:index'))
    else:
        messages.add_message(request, messages.ERROR, '403 forhibidden')
        return HttpResponseRedirect(reverse('webcosmoapp:dashboard'))
            
def changekategori(request):
    if request.method == 'POST':
        if request.session.has_key('username'):
            username = request.session['username']
            user = get_object_or_404(User, username=username)
            id_kategori = request.POST['id']
            kategori_field = request.POST['kategori']
            kategori = Kategori.objects.get(id_kategori=id_kategori)
            tanggal = datetime.datetime.now()
            if kategori:
                kot = Kategori.objects.get(id_kategori=id_kategori)
                kot.kategori = kategori_field
                kot.tanggal_update = tanggal
                kot.save()
                messages.add_message(request, messages.SUCCESS, 'Data kategori berhasil diedit...')
                return HttpResponseRedirect(reverse('webcosmoapp:pengaturan'))
        else:
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoapp:index'))
    else:
        messages.add_message(request, messages.ERROR, '403 forhibidden')
        return HttpResponseRedirect(reverse('webcosmoapp:dashboard'))

def changesubkategori(request):
    if request.method == 'POST':
        if request.session.has_key('username'):
            username = request.session['username']
            user = get_object_or_404(User, username=username)
            id_subkategori = request.POST['id']
            kategori_field = request.POST['kategori']
            sub_kategori_field = request.POST['sub_kategori']
            sub_kat = Sub_Kategori.objects.get(id_subKat=id_subkategori)
            tanggal = datetime.datetime.now()
            if sub_kat:
                sb = Sub_Kategori.objects.get(id_subKat=id_subkategori)
                sb.sub_kategori = sub_kategori_field
                sb.tanggal_update = tanggal
                sb.id_kategori_id = kategori_field
                sb.save()
                messages.add_message(request, messages.SUCCESS, 'Data sub kategori berhasil diedit...')
                return HttpResponseRedirect(reverse('webcosmoapp:pengaturan'))
        else:
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoapp:index'))
    else:
        messages.add_message(request, messages.ERROR, '403 forhibidden')
        return HttpResponseRedirect(reverse('webcosmoapp:dashboard'))

def deletekategori(request):
    if request.method == 'POST':
        if request.session.has_key('username'):
            username = request.session['username']
            user = get_object_or_404(User, username=username)
            id_kategori = request.POST['id']
            kategori = Kategori.objects.get(id_kategori=id_kategori)
            if kategori:
                kategori.status = '0'
                kategori.save()
                return HttpResponseRedirect(reverse('webcosmoapp:pengaturan'))
            else:
                messages.add_message(request, messages.ERROR, 'Terjadi kesalahan pada menghapus data Produk!!')
        else:
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoapp:index'))
    else:
        messages.add_message(request, messages.ERROR, '403 forhibidden')
        return HttpResponseRedirect(reverse('webcosmoapp:dashboard'))

def deletesubkategori(request):
    if request.method == 'POST':
        if request.session.has_key('username'):
            username = request.session['username']
            user = get_object_or_404(User, username=username)
            id_subkategori = request.POST['id']
            subkategori = Sub_Kategori.objects.get(id_subKat=id_subkategori)
            if subkategori:
                subkategori.status = '0'
                subkategori.save()
                return HttpResponseRedirect(reverse('webcosmoapp:pengaturan'))
            else:
                messages.add_message(request, messages.ERROR, 'Terjadi kesalahan pada menghapus data Produk!!')
        else:
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoapp:index'))
    else:
        messages.add_message(request, messages.ERROR, '403 forhibidden')
        return HttpResponseRedirect(reverse('webcosmoapp:dashboard'))

def data_reseller(request):
    return render(request, 'cosmoadmin/datareseller.html')

def tambah_reseller(request):
    return render(request, 'cosmoadmin/tambah-r.html')

def transaksi_reseller(request):
    return render(request, 'cosmoadmin/transaksireseller.html')

def pemesanan(request):
    return render(request, 'cosmoadmin/pemesanan.html')

def pembayaran(request):
    return render(request, 'cosmoadmin/pembayaran.html')

def pengiriman(request):
    return render(request, 'cosmoadmin/pengiriman.html')

def pengaturan(request):
    if request.session.has_key("username"):
        username = request.session['username']
        users = get_object_or_404(User, username=username)
        kategori = Kategori.objects.filter(status='1')
        sub_kategori = Sub_Kategori.objects.filter(status='1')
        kurir = Kurir.objects.filter(status='1')
        return render(request, 'cosmoadmin/pengaturan.html', {'admin': users, 'kategori': kategori, 'sub_kategori': sub_kategori, 'kurir':kurir})
    else:
        if request.session.has_key("username"):
            del request.session['username']
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoapp:index'))
        else:
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoapp:index'))

def addkurir(request):
    if request.method == 'POST':
        if request.session.has_key('username'):
            username = request.session['username']
            user = get_object_or_404(User, username=username)
            id_kurir = uuid.uuid4().hex[:6].upper()

            nama_kurir = request.POST['nama_kurir']
            jenis_pengiriman = request.POST['jenis_pengiriman']
            estimasi = request.POST['estimasi']
            ongkir = request.POST['ongkir']
            tanggal = datetime.datetime.now()

            kurir = Kurir(id_kurir=id_kurir, nama_kurir=nama_kurir, jenis_pengiriman=jenis_pengiriman, estimasi=estimasi, ongkir=ongkir, tanggal=tanggal, tanggal_update=tanggal, status='1')

            if kurir:
                kurir.save()
                messages.add_message(request, messages.SUCCESS, 'Data kurir berhasil ditambah...')
                return HttpResponseRedirect(reverse('webcosmoapp:pengaturan'))
            else:
                messages.add_message(request, messages.SUCCESS, 'Data kurir gagal ditambah...')
                return HttpResponseRedirect(reverse('webcosmoapp:pengaturan'))


        else:
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoapp:index'))
    else:
        messages.add_message(request, messages.ERROR, '403 forhibidden')
        return HttpResponseRedirect(reverse('webcosmoapp:dashboard'))
    

def logout(request):
    del request.session['username']
    return HttpResponseRedirect(reverse('webcosmoapp:index'))