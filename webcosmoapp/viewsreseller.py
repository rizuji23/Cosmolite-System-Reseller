from os import pread
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

def login(request):
    if request.session.has_key("username_reseller"):
        username = request.session['username_reseller']
        users = get_object_or_404(Reseller, username=username)
        return HttpResponseRedirect(reverse('webcosmoappreseller:dashboard'))
    else:
        return render(request, 'reseller/login.html')

def index(request):
    return render(request, 'reseller/regjoin.html')

def register(request):
    return render(request, 'reseller/register.html')

def dashboard(request):
    if request.session.has_key("username_reseller"):
        username = request.session['username_reseller']
        users = get_object_or_404(Reseller, username=username)
        produk = Produk.objects.all()
        return render(request, 'reseller/index.html', {'reseller': users, 'produk':produk})
    else:
        if request.session.has_key("username_reseller"):
            del request.session['username_reseller']
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoappreseller:login'))
        else:
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoappreseller:login'))

def addreseller(request):
    nama_depan = request.POST['nama_depan']
    nama_belakang = request.POST['nama_belakang']
    email = request.POST['email']
    no_telp = request.POST['no_telp']
    username = request.POST['username']
    password = request.POST['password']
    laki = request.POST.get('laki', '3')
    perempuan = request.POST.get('perempuan', '3')
    subs = request.POST.get('subs', '0')

    tanggal = datetime.datetime.now()
    id_reseller = uuid.uuid4().hex[:6].upper()

    check_username = Reseller.objects.filter(username=username).exists()
    
    if not check_username:

        if laki == '1':
            password_new = make_password(password)
            reseller = Reseller(id_reseller=id_reseller, nama_depan=nama_depan, nama_belakang=nama_belakang, email=email, no_telp=no_telp, username=username, password=password_new, status='1', kebijakan='1', subscribe=subs, tanggal=tanggal, tanggal_update=tanggal, jk=laki)

            if reseller:
                reseller.save()
                check = Reseller.objects.get(id_reseller=id_reseller)
                id_detail_re = uuid.uuid4().hex[:6].upper()
                detailre = Detail_Reseller(id_reseller_detail=id_detail_re, tanggal=tanggal, tanggal_update=tanggal, alamat_user_id=None, id_bank_id=None, id_nik_id=None, id_reseller_id=check.id, tanggal_lahir=None)
                print(id_reseller)
                if detailre:
                    detailre.save()
                    messages.add_message(request, messages.SUCCESS, 'Akun anda sudah terdaftar...')
                    return HttpResponseRedirect(reverse('webcosmoappreseller:login'))
            else:
                messages.add_message(request, messages.ERROR, 'Terjadi kesalahan saat mendaftar akun!!')
                return HttpResponseRedirect(reverse('webcosmoappreseller:login'))
        elif perempuan == '0':
            password_new = make_password(password)
            reseller = Reseller(id_reseller=id_reseller,nama_depan=nama_depan, nama_belakang=nama_belakang, email=email, no_telp=no_telp, username=username, password=password_new, status='1', kebijakan='1', subscribe=subs, tanggal=tanggal, tanggal_update=tanggal, jk=perempuan)

            if reseller:
                reseller.save()
                check = Reseller.objects.get(id_reseller=id_reseller)
                id_detail_re = uuid.uuid4().hex[:6].upper()
                detailre = Detail_Reseller(id_reseller_detail=id_detail_re, tanggal=tanggal, tanggal_update=tanggal, alamat_user_id=None, id_bank_id=None, id_nik_id=None, id_reseller_id=check.id, tanggal_lahir=None)
                if detailre:
                    detailre.save()
                    messages.add_message(request, messages.SUCCESS, 'Akun anda sudah terdaftar...')
                    return HttpResponseRedirect(reverse('webcosmoappreseller:login'))
            else:
                messages.add_message(request, messages.ERROR, 'Terjadi kesalahan saat mendaftar akun!!')
                return HttpResponseRedirect(reverse('webcosmoappreseller:login'))
        else:
            messages.add_message(request, messages.ERROR, 'ERROR!!!')
            return HttpResponseRedirect(reverse('webcosmoappreseller:login'))
    else:
        messages.add_message(request, messages.ERROR, 'Username ' + str(username) + ' sudah digunakan!!')
        return HttpResponseRedirect(reverse('webcosmoappreseller:login'))
        
def authreseller(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            akun = Reseller.objects.get(username=username)
            if check_password(password, akun.password):
                request.session['username_reseller'] = username
                return HttpResponseRedirect(reverse('webcosmoappreseller:dashboard'))
            else:
               messages.add_message(request, messages.ERROR, 'Username Atau Password Salah')
               return HttpResponseRedirect(reverse('webcosmoappreseller:login'))
        except Reseller.DoesNotExist:
               messages.add_message(request, messages.ERROR, 'Username Atau Password Salah')
               return HttpResponseRedirect(reverse('webcosmoappreseller:login'))
    else:
        messages.add_message(request, messages.ERROR, '403 Forhibbiden')
        return HttpResponseRedirect(reverse('webcosmoappreseller:login'))

def belanjaproduk(request):
    if request.session.has_key("username_reseller"):
        username = request.session['username_reseller']
        users = get_object_or_404(Reseller, username=username)
        produk = Produk.objects.all()
        return render(request, 'reseller/cari-produk.html', {'reseller': users, 'produk':produk})
    else:
        if request.session.has_key("username_reseller"):
            del request.session['username_reseller']
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoappreseller:login'))
        else:
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoappreseller:login'))

def aturakun(request):
    if request.session.has_key("username_reseller"):
        username = request.session['username_reseller']
        users = get_object_or_404(Reseller, username=username)
        detail = Detail_Reseller.objects.get(id_reseller_id=users.id)
        alamat = Alamat.objects.filter(id_user=users.id_reseller)
        return render(request, 'reseller/atur-akun.html', {'reseller': users, 'detail':detail, 'alamat': alamat})
    else:
        if request.session.has_key("username_reseller"):
            del request.session['username_reseller']
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoappreseller:login'))
        else:
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoappreseller:login'))

def detail_produk(request, id_produk):
    produk = Produk.objects.get(id_produk=id_produk)
    detail_produk = Detail_Produk.objects.get(kode_produk=id_produk)
    foto = Foto_Produk.objects.filter(id_produk_id=produk.id)
    return render(request, 'reseller/detail-produk.html', {'produk':produk, 'detailproduk':detail_produk, 'foto':foto})

def changereseller(request):
    if request.method == 'POST':
        if request.session.has_key("username_reseller"):
            username = request.session['username_reseller']
            user = get_object_or_404(Reseller, username=username)
            nama_depan = request.POST['nama_depan']
            nama_belakang = request.POST['nama_belakang']
            tanggal_lahir = request.POST['tanggal_lahir']
            
            change = Reseller.objects.get(id_reseller = user.id_reseller)
            change.nama_depan = nama_depan
            change.nama_belakang = nama_belakang

            if change:
                change.save()
                detail = Detail_Reseller.objects.get(id_reseller_id=change.id)
                detail.tanggal_lahir = tanggal_lahir
                if detail:
                    detail.save()
                    messages.add_message(request, messages.SUCCESS, 'Data diri sudah diedit...')
                    return HttpResponseRedirect(reverse('webcosmoappreseller:aturakun'))
                else:
                    messages.add_message(request, messages.ERROR, 'Gagal diedit!!')
                    return HttpResponseRedirect(reverse('webcosmoappreseller:aturakun'))
            else:
                messages.add_message(request, messages.SUCCESS, 'Gagal diedit!!')
                return HttpResponseRedirect(reverse('webcosmoappreseller:aturakun'))

        else:
            if request.session.has_key("username_reseller"):
                del request.session['username_reseller']
                messages.add_message(request, messages.ERROR, 'Harus Login!!')
                return HttpResponseRedirect(reverse('webcosmoapp:index'))
            else:
                messages.add_message(request, messages.ERROR, 'Harus Login!!')
                return HttpResponseRedirect(reverse('webcosmoapp:index'))
    else:
        messages.add_message(request, messages.ERROR, '403 Forhibbiden')
        return HttpResponseRedirect(reverse('webcosmoappreseller:login'))

def addalamat(request):
    if request.method == 'POST':
        if request.session.has_key('username_reseller'):
            username = request.session['username_reseller']
            user = get_object_or_404(Reseller, username=username)
            label = request.POST['label']
            provinsi = request.POST['provinsi']
            kotakab = request.POST['kotakab']
            kecamatan = request.POST['kecamatan']
            kelurahan = request.POST['kelurahan']
            kodepos = request.POST['kodepos']
            alamat_lengkap = request.POST['alamat_lengkap']

            tanggal = datetime.datetime.now()
            id_alamat = uuid.uuid4().hex[:6].upper()
            print(kodepos)
            alamat = Alamat(id_alamat=id_alamat, id_user=user.id_reseller, label=label, provinsi=provinsi, kotakab=kotakab, kecamatan=kecamatan, kelurahan=kelurahan, kodepos=kodepos, status='1', alamat_lengkap=alamat_lengkap, tanggal=tanggal, tanggal_update=tanggal)

            if alamat:
                alamat.save()
                return JsonResponse({'data': True})
            else:
                return JsonResponse({'data': False})

        else:
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoappreseller:login'))
    else:
        messages.add_message(request, messages.ERROR, '403 forhibidden')
        return HttpResponseRedirect(reverse('webcosmoappreseller:dashboard'))

def addnik(request):
    if request.method == 'POST':
        if request.session.has_key('username_reseller'):
            username = request.session['username_reseller']
            user = get_object_or_404(Reseller, username=username)
            
            nik = request.POST['nik']
            dir_nik = request.FILES['foto_nik']

            tanggal = datetime.datetime.now()
            id_nik = uuid.uuid4().hex[:6].upper()

            nik = Nik(id_nik=id_nik, no_nik=nik, dir_nik=dir_nik, tanggal=tanggal, tanggal_update=tanggal, id_user_id=user.id)

            if nik:
                nik.save()
                niks = Nik.objects.get(id_user_id=user.id)
                detail = Detail_Reseller.objects.get(id_reseller_id=user.id)
                detail.id_nik_id = niks.id
                detail.tanggal_update = tanggal
                if detail:
                    detail.save()
                    messages.add_message(request, messages.SUCCESS, 'Nik sudah diupload...')
                    return HttpResponseRedirect(reverse('webcosmoappreseller:aturakun'))
                else:
                    messages.add_message(request, messages.ERROR, 'Nik gagal diupload!!')
                    return HttpResponseRedirect(reverse('webcosmoappreseller:aturakun'))
            else:
                messages.add_message(request, messages.ERROR, 'Nik gagal diupload!!')
                return HttpResponseRedirect(reverse('webcosmoappreseller:aturakun'))

        else:
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoappreseller:login'))
    else:
        messages.add_message(request, messages.ERROR, '403 forhibidden')
        return HttpResponseRedirect(reverse('webcosmoappreseller:dashboard'))

def addbank(request):
    if request.method == 'POST':
        if request.session.has_key('username_reseller'):
            username = request.session['username_reseller']
            user = get_object_or_404(Reseller, username=username)
            
            nama_bank = request.POST['nama_bank']
            no_rekening = request.POST['no_rekening']

            tanggal = datetime.datetime.now()
            id_bank = uuid.uuid4().hex[:6].upper()

            nik = Nik.objects.get(id_user_id=user.id)

            bank = Account_Bank(id_bank=id_bank, id_user=user.id_reseller, nama_bank=nama_bank, no_rekening=no_rekening, tanggal=tanggal, tanggal_update=tanggal, id_nik_id=nik.id)

            if bank:
                bank.save()
                banks = Account_Bank.objects.get(id_nik_id=nik.id)
                detail = Detail_Reseller.objects.get(id_reseller_id=user.id)
                detail.id_bank_id = banks.id
                detail.tanggal_update = tanggal
                if detail:
                    detail.save()
                    messages.add_message(request, messages.SUCCESS, 'Akun Bank sudah ditambah...')
                    return HttpResponseRedirect(reverse('webcosmoappreseller:aturakun'))
                else:
                    messages.add_message(request, messages.ERROR, 'Akun Bank gagal ditambah!!')
                    return HttpResponseRedirect(reverse('webcosmoappreseller:aturakun'))
            else:
                messages.add_message(request, messages.ERROR, 'Nik gagal diupload!!')
                return HttpResponseRedirect(reverse('webcosmoappreseller:aturakun'))

        else:
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoappreseller:login'))
    else:
        messages.add_message(request, messages.ERROR, '403 forhibidden')
        return HttpResponseRedirect(reverse('webcosmoappreseller:dashboard'))

def logout(request):
    del request.session['username_reseller']
    return HttpResponseRedirect(reverse('webcosmoappreseller:login'))

def buy(request, id_produk):
    if request.session.has_key("username_reseller"):
        username = request.session['username_reseller']
        users = get_object_or_404(Reseller, username=username)
        detail = Detail_Reseller.objects.get(id_reseller_id=users.id)
        alamat = Alamat.objects.filter(id_user=users.id_reseller)
        produk = Produk.objects.filter(id_produk=id_produk)
        account_b = Account_Bank.objects.filter(id_user=users.id_reseller)
        kurir = Kurir.objects.filter(status='1')
        return render(request, 'reseller/detail-transaksi.html', {'reseller': users, 'detail':detail, 'alamat': alamat, 'produk':produk, 'bank':account_b, 'kurir':kurir})
    else:
        if request.session.has_key("username_reseller"):
            del request.session['username_reseller']
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoappreseller:login'))
        else:
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoappreseller:login'))

def statistik(request):
    if request.session.has_key("username_reseller"):
        username = request.session['username_reseller']
        users = get_object_or_404(Reseller, username=username)
        produk = Produk.objects.all()
        return render(request, 'reseller/statistik.html', {'reseller': users, 'produk':produk})
    else:
        if request.session.has_key("username_reseller"):
            del request.session['username_reseller']
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoappreseller:login'))
        else:
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoappreseller:login'))

def listpemesanan(request):
    if request.session.has_key("username_reseller"):
        username = request.session['username_reseller']
        users = get_object_or_404(Reseller, username=username)
        produk = Produk.objects.all()
        return render(request, 'reseller/list-pesanan.html', {'reseller': users, 'produk':produk})
    else:
        if request.session.has_key("username_reseller"):
            del request.session['username_reseller']
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoappreseller:login'))
        else:
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoappreseller:login'))

def keranjang(request):
    if request.session.has_key("username_reseller"):
        username = request.session['username_reseller']
        users = get_object_or_404(Reseller, username=username)
        produk = Produk.objects.all()
        return render(request, 'reseller/keranjang.html', {'reseller': users, 'produk':produk})
    else:
        if request.session.has_key("username_reseller"):
            del request.session['username_reseller']
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoappreseller:login'))
        else:
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoappreseller:login'))

def reward(request):
    if request.session.has_key("username_reseller"):
        username = request.session['username_reseller']
        users = get_object_or_404(Reseller, username=username)
        produk = Produk.objects.all()
        return render(request, 'reseller/reward.html', {'reseller': users, 'produk':produk})
    else:
        if request.session.has_key("username_reseller"):
            del request.session['username_reseller']
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoappreseller:login'))
        else:
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoappreseller:login'))

def gantipassword(request):
    if request.session.has_key("username_reseller"):
        username = request.session['username_reseller']
        users = get_object_or_404(Reseller, username=username)
        produk = Produk.objects.all()
        return render(request, 'reseller/ganti-password.html', {'reseller': users, 'produk':produk})
    else:
        if request.session.has_key("username_reseller"):
            del request.session['username_reseller']
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoappreseller:login'))
        else:
            messages.add_message(request, messages.ERROR, 'Harus Login!!')
            return HttpResponseRedirect(reverse('webcosmoappreseller:login'))

