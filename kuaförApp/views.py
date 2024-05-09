from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
import openpyxl

from .forms import FirmaEkle, KatEkle, KategoriEkle, MasaEkle, UrunEkle, UserEkle, UserUpdateForm, FirmaDüzenle, KatGüncelle, MasaDüzenle

from .models import Firma, FirmaUser, Kat, Kategori, Log, Masa, ShortUrl, SiparisUrun, Urun, Yetki
import random,string
from django.contrib import messages
# Firma oluşturma ve listeleme ekranı
def check_ip_address(request):
    if request.method == 'GET':
        ip_adresi = request.GET.get('ip_adresi', None)
        print(ip_adresi)
        if ip_adresi:
            print('İp', ip_adresi)
            if Firma.objects.filter(firma_dis_ip=ip_adresi).exists():
                return JsonResponse({'exists': True})
    return JsonResponse({'exists': False})
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# sadece orqerr erişebilir
from django.contrib.auth.decorators import login_required
@login_required(login_url='user_giris')
def firma_ekle(request):
    yetki = get_object_or_404(Yetki, user=request.user)
    
    if not (request.user.username == "orqerr" or (request.user.user_frm_kod == "-1" and yetki.firma_ekle)):
        messages.error(request, 'Firma ekleyemezsiniz.')
        return redirect(request.META.get('HTTP_REFERER'))
    
    if not request.user.user_frm_kod == "-1":
        messages.error(request, 'Firma ekleme yetkiniz bulunmamaktadır.')
        return redirect('admin_dashboard', firma_kod=request.user.user_frm_kod)
    
    firmalar = Firma.objects.all().order_by('id')
    paginator = Paginator(firmalar, 10)  # Her sayfada 10 firma göster
    page = request.GET.get('page')
    
    try:
        firmalar = paginator.page(page)
    except PageNotAnInteger:
        firmalar = paginator.page(1)
    except EmptyPage:
        firmalar = paginator.page(paginator.num_pages)

    if not request.method == "POST":
        form = FirmaEkle()
        return redirect(request.META.get('HTTP_REFERER'))

    form = FirmaEkle(request.POST)
    if not form.is_valid():
        messages.error(request, form.errors)
        return redirect(request.META.get('HTTP_REFERER'))
    
    firma_kod = ''.join(random.choices(string.digits, k=6))
    # Firma kodunun benzersiz olup olmadığını kontrol et
    while Firma.objects.filter(firma_kod=firma_kod).exists():
        firma_kod = ''.join(random.choices(string.digits, k=6))
    
    firma = form.save(commit=False)
    firma.firma_kod = firma_kod
    
    if firma.firma_bas_tar > firma.firma_bit_tar:
        messages.add_message(request, messages.ERROR, "Anlaşma Başlama Tarihi Bitiş Tarihinden Büyük Olamaz")
        return redirect(request.META.get('HTTP_REFERER'))
    
    firma.firma_create_user = request.user.username
    firma.save()
    messages.success(request, f'Firma Başarıyla Eklendi. Firma Kodu: {firma_kod}')
    return redirect(request.META.get('HTTP_REFERER'))
def tum_firmalar(request):
    yetki = get_object_or_404(Yetki, user=request.user)
    if not (request.user.username == "orqerr" or (request.user.user_frm_kod == "-1" and yetki.firma_ekle)):
        messages.error(request, 'Bu alana erişemezsiniz.')
        return redirect(request.META.get('HTTP_REFERER'))
        
    firmalar = Firma.objects.all()
    context = {
        'firmalar':firmalar,
    }
    return render(request,'admin_alani/tum_firmalar.html',context)
def firma_düzenle(request, pk, firma_kod):
    print('firma_düzenle viewsi çalıştı')
    print(request.user.username)
    
    # Execute common operations regardless of user
    firma = get_object_or_404(Firma, pk=pk, firma_kod=firma_kod)

    if firma.firma_kod == "-1":
         messages.error(request, 'Bu Firma Düzenlenemez')
         return redirect(request.META.get('HTTP_REFERER'))
    yetki = get_object_or_404(Yetki, user=request.user)
    if not (request.user.username == "orqerr" or (request.user.user_frm_kod == "-1" and yetki.firma_duzenle)):
        messages.error(request, "Firma düzenleme yetkiniz bulunmuyor")
        return redirect(request.META.get('HTTP_REFERER'))
    # POST kontrolü
    if not request.method == "POST":
        messages.error(request, "Firma düzenleme sadece POST istekleriyle kabul edilir.")
        return redirect(request.META.get('HTTP_REFERER'))
    
    # Form işlemleri
    form = FirmaDüzenle(request.POST, instance=firma)
    if not form.is_valid():
        messages.error(request, "Formda bulunan hataları düzeltiniz.")
        return redirect(request.META.get('HTTP_REFERER'))

    form.save()  # Formu kaydet
    messages.success(request, 'Firma üstündeki değişiklikler kaydedildi.')
    return redirect(request.META.get('HTTP_REFERER'))

def firma_detay_redirect(request):
    if request.method != 'POST':
        messages.warning(request, 'Bu istek kabul edilmez.')
        print('istek post değil')
        return redirect(request.META.get('HTTP_REFERER'))
    
    firma_kod = request.POST.get('firma_kod')
    print('firma_kod',firma_kod)
    firma = Firma.objects.filter(firma_kod=firma_kod).first()
    if not firma:
        messages.warning(request, 'Belirtilen firma kodu ile eşleşen firma bulunamadı.')
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('admin_dashboard', firma_kod=firma_kod)
def firma_detay(request, firma_kod):
    firma = get_object_or_404(Firma, firma_kod=firma_kod)
        
    # Kullanıcı firma_koduna sahip değilse veya firma_kod -1 ise sayfaya erişim engellenir
    # if request.user.user_frm_kod != firma_kod and request.user.user_frm_kod != '-1':
    #     messages.warning(request, 'Bu Sayfaya Gidemezsiniz.')
    #     return redirect('firma_detay', firma_kod=request.user.user_frm_kod)
    urunler = Urun.objects.filter(urun_frm_kod=firma_kod)
    masalar = Masa.objects.filter(masa_frm_kod=firma_kod)
    kategoriler = Kategori.objects.filter(kategori_frm=firma)
    katlar = Kat.objects.filter(kat_frm_kod=firma_kod).order_by('id')
    düzenleForm = FirmaDüzenle()
    userform = UserEkle()
    masaForm = MasaEkle()
    katForm = KatEkle()
    kategoriForm = KategoriEkle()
    # UrunEkle formuna firma bilgisini gönderin
    urunForm = UrunEkle(firma=firma)

    
    firma_kullanicilari = FirmaUser.objects.filter(user_frm_kod=firma_kod)

    context = {
        'kategoriler':kategoriler,
        'urunler':urunler,
        'kategoriForm': kategoriForm,
        'urunForm': urunForm,
        'katlar': katlar,
        'masalar': masalar,
        'katForm': katForm,
        'masaForm': masaForm,
        'düzenleForm': düzenleForm,
        'firma_kullanicilari': firma_kullanicilari,
        'userform': userform,
        'firma': firma
    }

    return render(request, 'firma_detay.html', context)
def user_ekle(request, firma_kod):
    firma = get_object_or_404(Firma, firma_kod=firma_kod)
    
    if request.method == 'POST':
        user_form = UserEkle(request.POST)
        yetki_id_listesi = request.POST.getlist('yetkiler[]')

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.user_kyt_user = request.user.username
            user.user_frm_kod = firma.firma_kod
            user.save()

            for yetki_id in yetki_id_listesi:
                try:
                    yetki = Permission.objects.get(id=yetki_id)
                    user.user_permissions.add(yetki)
                except Permission.DoesNotExist:
                    print(f"Yetki bulunamadı: {yetki_id}")
            
            user.user_firma.add(firma)
            return redirect('admin_dashboard', firma_kod=firma_kod)
        else:
            print(user_form.errors)
    else:
        user_form = UserEkle()
    
    return render(request, 'user_create.html', {'user_form': user_form})
import requests
from django.contrib.auth import authenticate, login
def user_giris(request):
    # Gelen istekten IP adresini al
    real_ip = request.META.get('HTTP_X_REAL_IP')
    external_ip = None
    response = requests.get("https://api.ipify.org?format=json")
    if response.status_code == 200:
        external_ip = response.json()['ip']
    print('external ip',external_ip)
    remote_addr = request.META.get('REMOTE_ADDR')
    print(remote_addr)
    real_ip = request.META.get('HTTP_X_REAL_IP')
    print('Real ip',real_ip)
    log = Log.objects.create(
        ip_adresi = real_ip
    )
    log.save()
    # Firmanın dış IP adresi ile eşleşen firmayı bul
    firma = Firma.objects.filter(firma_dis_ip=real_ip).first()
    
    if not firma:
        # Eğer firma bulunamazsa, bir hata mesajı göster
        messages.error(request, "Firma bulunamadıq.")
        return render(request, 'user_giris.html', {'firma': None})
    
    context = {
        'external_ip': external_ip,
        'remote_addr': remote_addr,
        'real_ip': real_ip,
        'firma': firma,  # Eşleşen firma
    }
    return render(request, 'user_giris.html', context)

from django.contrib.auth import authenticate, login

from django.contrib.auth import authenticate, login
def check_company_agreement():
    today = date.today()
    expired_companies = Firma.objects.filter(firma_bit_tar__lt=today)
    
    for company in expired_companies:
        # Firma bitiş tarihi bugünden önceyse, işlem yapılabilir
        # Örneğin, bir uyarı gönderilebilir veya firma durumu güncellenebilir
        # Burada sadece bir örnek olarak print ile konsola çıktı veriyorum
        print(f"{company.firma_adi} firmasının anlaşması {company.firma_bit_tar} tarihinde sona erdi.")
        # Firma durumunu güncelle
        if not company.firma_kod == "-1":
            company.firma_durum = False
            company.save()
    
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        manuel_kod_gir = request.POST.get('manuel_firma_kod')
        firma_kod = request.POST.get('firma_kod')
        if manuel_kod_gir == 'on':
            firma_kod = request.POST.get('firma_kod_manuel')
            print('manuel firma kodu alınacak')
        
        # Admin kullanıcısı için doğrulama
        if username == 'orqerr' and password == 'SEYASA':
            user = FirmaUser.objects.filter(username=username, user_frm_kod="-1").first()
            if user is not None:
                check_company_agreement()
                login(request, user)
                
                # Kullanıcının Yetki modelini oluştur veya var olanı al
                yetki, created = Yetki.objects.get_or_create(user=user)

                # Tüm yetki alanlarını döngü içinde True olarak ayarla
                for field in Yetki._meta.fields:
                    if field.name != 'user':  # Kullanıcı alanını atla
                        setattr(yetki, field.name, True)

                # Değişiklikleri kaydet
                yetki.save()
                
                return redirect('admin_dashboard', firma_kod=firma_kod)
            messages.error(request, 'Kullanıcı Adı veya Şifre Hatalı Kontrol Ediniz.')
        
        # Diğer kullanıcılar için doğrulama
        else:
            user = FirmaUser.objects.filter(username=username).first()
            if user is not None:
                # Kullanıcının user_tag değerini kontrol et
                if user.user_tag == 'Destek':
                    login(request, user)
                    return redirect('admin_dashboard', firma_kod=firma_kod)
                if user.user_frm_kod == firma_kod:
                    login(request, user)
                    return redirect('admin_dashboard', firma_kod=firma_kod)
                messages.error(request, 'Geçersiz firma kodu.')
            messages.error(request, 'Kullanıcı Adı veya Şifre Hatalı Kontrol Ediniz.')

    return redirect('user_giris')
from django.contrib.auth import logout
def user_logout(request):
    logout(request)
    return redirect('user_giris')
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, user_passes_test

def tum_kullanicilar(request):
    if request.user.user_frm_kod == "-1":
        if request.user.has_perm('kuaförApp.kullanicilari_listele'):
            users = FirmaUser.objects.all()
            context={
                'users':users,
            }
            return render(request, 'admin_alani/tum_kullanicilar.html',context)
        else:
            messages.error(request,'Bu sayfayı görüntülemek için yetkiniz bulunmamaktadır.')
            return render(request, 'admin_alani/tum_kullanicilar.html')
    else:
        messages.warning(request, 'Bu Sayfaya Erişemezsiniz.')
        return redirect(user_giris)

from django.contrib.auth.models import Permission
@login_required
def kullanici_detay(request, uuid4):
    user = get_object_or_404(FirmaUser, unique_id=uuid4)

    if request.method == 'POST':
        yetki_kimlikleri = request.POST.getlist('yetkiler')
        user.user_permissions.clear()
        for yetki_id in yetki_kimlikleri:
            yetki = get_object_or_404(Permission, id=yetki_id)
            user.user_permissions.add(yetki)
        return redirect('kullanici_detay', uuid4=uuid4)

    else:
        yetkiler = Permission.objects.all()
        user_yetkileri = user.user_permissions.all()

        context = {
            'user': user,
            'yetkiler': yetkiler,
            'user_yetkileri': user_yetkileri,
        }
        return render(request, 'admin_alani/kullanici_detay.html', context)
    
    import openpyxl
from django.shortcuts import render
from .models import Firma

def excel_aktar(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        try:
            # Excel dosyasını aç
            workbook = openpyxl.load_workbook(excel_file)
            worksheet = workbook.active
            
            # Her satırı oku ve modele aktar
            for row in worksheet.iter_rows(min_row=2, values_only=True):  # Başlıkları atla
                urun = Urun.objects.create(
                    urun_frm_kod=row[0],
                    urun_frm=Firma.objects.get(firma_kod=row[1]),
                    urun_ad=row[2],
                    urun_kategori=Kategori.objects.get(id=row[3]),
                    urun_durum=row[4],
                    urun_img=row[5],
                    urun_fiyat=row[6],
                    urun_kayit_user=row[7],
                    urun_kayit_zaman=row[8],
                    urun_frm_id=row[9]
                )
                urun.save()
                print(urun)
            
            return render(request, 'excel_aktar.html', {'success': True})
        except Exception as e:
            return render(request, 'excel_aktar.html', {'error': str(e)})
    
    return render(request, 'excel_aktar.html')
# KAT EKLEME VİEWSİ
def kat_ekle(request, firma_kod):
    if request.method == "POST":
        firma = get_object_or_404(Firma, firma_kod=firma_kod)
        if request.user.user_frm_kod == '-1' or request.user.user_frm_kod == firma.firma_kod:
            form = KatEkle(request.POST)
            if form.is_valid():
                kat_ad = form.cleaned_data['kat_ad']
                
                # Aynı ada sahip bir kategorinin olup olmadığını kontrol et
                if Kat.objects.filter(kat_firma=firma, kat_ad=kat_ad).exists():
                    messages.error(request, 'Bu isimde bir kat zaten mevcut.')
                    return redirect('admin_dashboard', firma_kod=firma_kod)
                kat = form.save(commit=False)  # veritabanına kaydetme
                kat.kat_firma = firma
                kat.kat_frm_kod = firma.firma_kod
                kat.kat_kayit_user = request.user.username
                kat.save()  #firma kodunu ayarladıktan sonra kaydet
                messages.success(request, 'Kat Başarıyla Eklendi')  # mesajı gönder
                return redirect('admin_dashboard', firma_kod=firma_kod)
            else:
                messages.success(request, 'Formda Bazı Hatalar Oluştu Lütfen Tekrar Deneyin..')  # mesajı gönder
                return redirect('admin_dashboard', firma_kod=firma_kod)
        else:
                if request.user.user_frm_kod != firma.firma_kod:
                    messages.error(request, 'İstek Yapılan Firma Size Ait Görünmüyor')  # mesajı gönder
                    print('İstek yapılan')
                    return redirect('admin_dashboard', firma_kod=firma_kod)
    else:
        # Handle GET request here, if necessary
        pass
# Kat düzenle

def kat_düzenle(request, firma_kod, kat_id):
    user_id = request.user.id

    # Master kullanıcı kontrolü
    if request.user.user_frm_kod == '-1':
        # Master kullanıcı, yetki kontrolü yapmadan doğrudan devam edebilir
        pass
    else:
        # Master kullanıcı değilse, yetkileri kontrol et
        try:
            yetki = Yetki.objects.get(user=request.user)
        except Yetki.DoesNotExist:
            # Kullanıcının yetkisi yoksa, uygun bir hata mesajı göster ve başka bir sayfaya yönlendir
            messages.error(request, 'Bu işlemi gerçekleştirmek için yetkiniz bulunmamaktadır.')
            return redirect('anasayfa')  # veya başka bir sayfaya yönlendir

        # Kullanıcının konum eklemeye yetkisi yoksa hata mesajı göster ve yönlendir
        if not yetki.konum_ekle:
            messages.error(request, 'Konum ekleme yetkiniz bulunmamaktadır.')
            return redirect('admin_dashboard', firma_kod=request.user.user_frm_kod)

    firma = get_object_or_404(Firma, firma_kod=firma_kod)
    kat = get_object_or_404(Kat, id=kat_id)
    yeni_kat_ad = request.POST.get('kat_ad')
    kat_durum = request.POST.get('kat_durum')

    # Eğer yeni kat adı boşsa veya mevcut bir kategorinin adıyla aynıysa hata döndür
    if Kat.objects.filter(kat_frm_kod=firma.firma_kod, kat_ad=yeni_kat_ad).exists():
        messages.error(request, 'Bu isimde bir kat zaten mevcut.')
        return redirect('admin_dashboard', firma_kod=request.user.user_frm_kod)
    if not yeni_kat_ad:
        yeni_kat_ad = kat.kat_ad
    kat.kat_ad = yeni_kat_ad

    if kat_durum == 'on':
        kat.kat_durum = True
    else:
        kat.kat_durum = False

    kat.kat_kayit_user = request.user.username
    kat.save()
    messages.success(request, 'Güncelleme Başarılı')
    return redirect('admin_dashboard', firma_kod=firma_kod)

        

        
# Masa Ekle
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import MasaEkle
from .models import Firma, Kat, Masa

def masa_ekle(request, firma_kod):
    firma = get_object_or_404(Firma, firma_kod=firma_kod)
    
    if (request.user.username == 'orqerr' and request.user.user_frm_kod == '-1') or (request.user.user_frm_kod == firma_kod):
        if request.method == 'POST':
            form = MasaEkle(request.POST)
            kat_id = request.POST.get('masa_kat')
            if form.is_valid():
                kat = get_object_or_404(Kat, id=kat_id)
                masa = form.save(commit=False)
                if Masa.objects.filter(masa_frm_kod=firma_kod, masa_kat=kat, masa_num=masa.masa_num).exists():
                    messages.error(request, 'Bu isimde bir masa zaten mevcut.')
                    return redirect('admin_dashboard', firma_kod=firma_kod)
                masa.masa_kat = kat
                masa_firma = get_object_or_404(Firma, firma_kod=firma_kod)
                masa.masa_firma = masa_firma
                masa.masa_frm_kod = masa_firma.firma_kod
                masa.masa_kayit_user = request.user.username
                masa.save()
                messages.success(request, 'Masa Başarıyla Eklendi')
                return redirect('admin_dashboard', firma_kod=masa_firma.firma_kod)
            else:
                print(form.errors)
                messages.error(request, 'Formda Bazı Hatalar Oluştu. Lütfen Tekrar Deneyin.')
        else:
            form = MasaEkle()

        return render(request, 'masa_ekle.html', {'form': form, 'firma_kod': firma_kod})
    else:
        return redirect('admin_dashboard',firma_kod = request.user.user_frm_kod)
from django.http import JsonResponse

import json

def get_user_location(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        print(latitude)
        print(longitude)

        # Kullanıcı konumunu işleyin
        # Örneğin, veritabanına kaydedebilir veya başka bir işlem yapabilirsiniz
        
        return JsonResponse({'message': 'Kullanıcı konumu alındı.'})
    else:
        return JsonResponse({'error': 'Geçersiz istek methodu.'}, status=400)


def masa_düzenle(request, firma_kod):
    yetki = get_object_or_404(Yetki, user=request.user)
    
    # Yetki kontrolü
    if not (
        (request.user.username == "orqerr" and request.user.user_frm_kod == "-1") or
        (request.user.user_frm_kod == "-1" and yetki.masa_guncelle) or 
        (request.user.user_frm_kod == firma_kod and yetki.masa_guncelle)
    ):
        messages.error(request, 'Masayı Güncellenemez. Hata Kodu: MGYY:001')
        return redirect(request.META.get('HTTP_REFERER'))
    
    if not request.method == 'POST':
        messages.error(request, "Geçersiz istek türü.")
        return redirect('admin_dashboard', firma_kod=firma_kod)
    
    masa_id = request.POST.get('masa_id')
    masa = get_object_or_404(Masa, id=masa_id)
    
    yeni_kat_id = request.POST.get('yeni_kat_id')
    yeni_masa_durum = request.POST.get('yeni_masa_durum')
    yeni_masa_num = request.POST.get('yeni_masa_num')
    
    # Masa durumu güncelleme
    if yeni_masa_durum == 'on':
        masa.masa_durum = True
    else:
        masa.masa_durum = False
    
    # Masa numarası veya kat değişti mi kontrolü
    if yeni_masa_num != masa.masa_num or yeni_kat_id != masa.masa_kat.id:  
        yeni_kat = get_object_or_404(Kat, id=yeni_kat_id)
        
        # Aynı katta ve aynı masa numarasına sahip başka bir masa var mı kontrolü
        if Masa.objects.filter(masa_kat=yeni_kat, masa_num=yeni_masa_num).exclude(id=masa_id).exists():
            messages.error(request, "Belirtilen katta aynı masa numarasına sahip başka bir masa mevcut.")
            return redirect('admin_dashboard', firma_kod=firma_kod)
        
        # Masa numarası ve kat güncelleme
        masa.masa_kat = yeni_kat
        masa.masa_num = yeni_masa_num
    
    masa.save()
    messages.success(request, "Masa Başarıyla Düzenlendi.")
    return redirect('admin_dashboard', firma_kod=firma_kod)
    
def urun_ekle(request, firma_kod):
    firma = get_object_or_404(Firma, firma_kod=firma_kod)
    yetki = get_object_or_404(Yetki, user=request.user)
    if not (
    (request.user.username == 'orqerr' and request.user.user_frm_kod == "-1") or 
    (request.user.user_frm_kod == "-1" and yetki.ürün_ekle) or 
    (yetki.ürün_ekle and request.user.user_frm_kod == firma.firma_kod)
    ):
        print(request.user.username)
        print(request.user.user_frm_kod)
        messages.error(request, 'İşlem yapılan firma size ait değil.')
        return redirect('admin_dashboard', firma_kod=firma_kod)
    
    if request.method == 'POST':
        form = UrunEkle(request.POST, request.FILES)
        if form.is_valid():
            urun = form.save(commit=False)
            urun.urun_frm_kod = firma.firma_kod
            urun.urun_frm = firma
            urun.urun_kayit_user = request.user.username
            
            # Aynı kategori ve isimde bir ürün varsa eklenmemesi için kontrol edin
            if Urun.objects.filter(urun_ad=urun.urun_ad, urun_kategori=urun.urun_kategori).exists():
                messages.error(request, 'Aynı kategoride aynı isimde bir ürün zaten mevcut.')
            else:
                urun.save()
                messages.add_message(request, messages.SUCCESS, "Ürün Başarıyla Kaydedildi")
                return redirect('admin_dashboard', firma_kod=firma_kod)
        else:
            print(form.errors)
            messages.add_message(request, messages.ERROR, "Formda bazı hatalar var hataları düzeltin.")
            

    return redirect('admin_dashboard', firma_kod=firma_kod)
def urun_guncelle(request, firma_kod):
    # Firma nesnesini al
    yetki = get_object_or_404(Yetki, user=request.user)
    firma = get_object_or_404(Firma, firma_kod=firma_kod)
    if not (
    (request.user.username == 'orqerr' and request.user.user_frm_kod == "-1") or 
    (request.user.user_frm_kod == "-1" and yetki.urun_guncelle) or 
    (yetki.urun_guncelle and request.user.user_frm_kod == firma.firma_kod)
    ):
        messages.error(request, 'Bu işlemi gerçekleştirmek için yetkiniz bulunmamaktadır. Hata Kodu : UGYY:001')
        return redirect('admin_dashboard', firma_kod=firma_kod)
    if not request.method == 'POST':
        # POST isteği değilse hata mesajı göster ve yönlendirme yap
        messages.add_message(request, messages.ERROR, "İstek Doğru Değil")
        return redirect('admin_dashboard', firma_kod=firma_kod)
        # Formdan gelen verileri al
    urun_id = request.POST.get('urun_id')
    yeni_urun_adi = request.POST.get('urun_adi')
    yeni_kategori_id = request.POST.get('urun_kategori')
    yeni_urun_durum = request.POST.get('urun_durum')
    yeni_urun_image = request.FILES.get('urun_image')
    
    # Ürün nesnesini al
    kategori = get_object_or_404(Kategori,id=yeni_kategori_id)
    urun = get_object_or_404(Urun, id=urun_id)
    
    # Ürün adı değişmişse
    if yeni_urun_adi != urun.urun_ad:
        urun.urun_ad= yeni_urun_adi

    # Ürün kategorisi değişmişse
    if kategori != urun.urun_kategori:
        urun.urun_kategori = kategori

    # Ürün durumunu güncelle
    urun.urun_durum = yeni_urun_durum == 'on'

    # Ürün resmini güncelle
    if yeni_urun_image:
        urun.urun_img = yeni_urun_image

    # Değişiklikleri kaydet
    urun.save()
    messages.success(request, 'Ürün başarıyla güncellendi.')

    # Yönlendirme yap
    return redirect('admin_dashboard', firma_kod=firma_kod)
        
def kategori_ekle(request, firma_kod):
    firma = get_object_or_404(Firma, firma_kod=firma_kod)
    
    # Kullanıcının işlem yapılan firmanın sahibi olup olmadığını kontrol edin
    if (request.user.user_frm_kod == firma.firma_kod) or (request.user.username == 'orqerr' and request.user.user_frm_kod == "-1"):
        
    
        if request.method == 'POST':
            form = KategoriEkle(request.POST,request.FILES)
            
            if form.is_valid():
                kategori = form.save(commit=False)
                kategori.kategori_frm_kod = firma.firma_kod
                kategori.kategori_frm = firma
                kategori.kategori_kayit_user = request.user.username
                
                # Aynı kategori koduna sahip bir kategori varsa hata mesajı gönder
                if Kategori.objects.filter(kategori_kod=kategori.kategori_kod, kategori_frm_kod=firma_kod).exists():
                    messages.error(request, 'Bu kodda bir kategori zaten mevcut.')
                    return redirect('admin_dashboard', firma_kod=firma_kod)
                if Kategori.objects.filter(kategori_ad=kategori.kategori_ad, kategori_frm_kod=firma_kod).exists():
                    messages.error(request, 'Bu adda bir kategori zaten mevcut.')
                    return redirect('admin_dashboard', firma_kod=firma_kod)
                
                # Aynı kategori adı ve koduna sahip bir kategori varsa hata mesajı gönder
                if Kategori.objects.filter(kategori_ad=kategori.kategori_ad, kategori_kod=kategori.kategori_kod, kategori_frm_kod=firma_kod).exists():
                    messages.error(request, 'Bu isimde ve kodda bir kategori zaten mevcut.')
                else:
                    kategori.save()
                    messages.success(request, 'Kategori Başarıyla Kaydedildi')
                    
                return redirect('admin_dashboard', firma_kod=firma_kod)
        else:
            # GET isteği geldiğinde, işlem yapılan firmanın kullanıcıya ait olup olmadığını kontrol edin
            if request.user.user_frm_kod != firma_kod:
                messages.error(request, 'İşlem yapılan firma size ait görünmüyor.')
                return redirect('admin_dashboard', firma_kod=firma_kod)
            
    return redirect('admin_dashboard', firma_kod=firma_kod)
def kategori_düzenle(request, firma_kod):
    # Firma nesnesini al
    firma = get_object_or_404(Firma, firma_kod=firma_kod)
    
    if request.method == 'POST':
        # Formdan gelen verileri al
        kategori_id = request.POST.get('kategori_id')
        yeni_kategori_adi = request.POST.get('kategori_adi')
        print('Yeni Kategori Adı',yeni_kategori_adi)
        yeni_kategori_kodu = request.POST.get('kategori_kodu')
        yeni_kategori_durum = request.POST.get('kategori_durum')
        yeni_kategori_image = request.FILES.get('kategori_image')
        
        # Kategori nesnesini al
        kategori = get_object_or_404(Kategori, id=kategori_id)
        
        # Kategori adı değişmişse
        if yeni_kategori_adi != kategori.kategori_ad:
            kategori.kategori_ad = yeni_kategori_adi

        # Kategori kodu değişmişse
        if yeni_kategori_kodu != kategori.kategori_kod:
            # Yeni kategori kodunun var olup olmadığını kontrol et
            if Kategori.objects.filter(kategori_frm=firma, kategori_frm_kod=firma_kod, kategori_kod=yeni_kategori_kodu).exists():
                messages.error(request, 'Bu kodda bir kategori zaten mevcut.')
                return redirect('admin_dashboard', firma_kod=firma_kod)
            else:
                kategori.kategori_kod = yeni_kategori_kodu

        # Kategori durumunu güncelle
        kategori.kategori_durum = yeni_kategori_durum == 'on'

        # Kategori resmini güncelle
        if yeni_kategori_image:
            kategori.kategori_image = yeni_kategori_image

        # Değişiklikleri kaydet
        kategori.save()
        messages.success(request, 'Kategori başarıyla güncellendi.')

        # Yönlendirme yap
        return redirect('admin_dashboard', firma_kod=firma_kod)
    
    else:
        # POST isteği değilse hata mesajı göster ve yönlendirme yap
        messages.add_message(request, messages.ERROR, "İstek Doğru Değil")
        return redirect('admin_dashboard', firma_kod=firma_kod)

        # POST isteği yoksa, düzenleme formunu göster
# def ürün_düzenle(request,firma_kod,ürün_id):
    # firma = get_object_or_404(Firma,firma_kod=firma_kod)
    # ürün = get_object_or_404(Urun,id=ürün_id)
    # print('Bulunan Ürün',ürün)
    # if (request.user.user_frm_kod == firma.firma_kod) or (request.user.username == 'orqerr' and request.user.user_frm_kod == "-1"):
    #     if request.method=="POST":
    #         yeni_ürün_adi = request.POST.get('ürün_adi') # yeni ürün adını al
    #         print('Adı',yeni_ürün_adi)
    #         yeni_ürün_fiyati = request.POST.get('ürün_fiyat')# yeni ürün fiyatı al
    #         print('Fiyat',yeni_ürün_fiyati)
    #         yeni_ürün_durum = request.POST.get('ürün_durum') # yeni ürün durumunu al
    #         print('Durum',yeni_ürün_durum)
    #         yeni_ürün_kategori = request.POST.get('ürün_kategori') # yeni ürün adını al
    #         print('Kategori',yeni_ürün_kategori)
    #         yeni_ürün_kategori_id = request.POST.get('ürün_kategori')# yeni kategori adını al
    #         yeni_kategori = get_object_or_404(Kategori, id=yeni_ürün_kategori_id)

    #         # Belirtilen kategori altında aynı isimde ürün var mı kontrol et
    #         if Urun.objects.filter(urun_ad=yeni_ürün_adi, urun_kategori=yeni_kategori).exists(): 
    #             messages.error(request, 'Bu kategoride aynı isimde bir ürün bulunmaktadır.')
    #             return redirect('firma_detay', firma_kod=firma_kod)
    #         # O kategoride aynı isimde bir ürün yoksa
    #         else:
    #             ürün.urun_kategori = yeni_kategori
    #         if yeni_ürün_adi == '':
    #             ürün.urun_ad= ürün.urun_ad
    #         else: #ürün adı boş değilse
    #             ürün.urun_ad = yeni_ürün_adi
    #         if yeni_ürün_fiyati == '':
    #             yeni_ürün_fiyati = ürün.urun_fiyat
    #         else: # ürün adı boş değilse
    #             ürün.urun_fiyat=yeni_ürün_fiyati
    #         if yeni_ürün_durum == None:
    #             ürün.urun_durum = False
    #         else: # ürün durumu on ise
    #             ürün.urun_durum = True
    #         ürün.save()
    #         messages.success(request,'Ürün Güncelle')
    #         return redirect('firma_detay',firma_kod=firma_kod)
    #     else:
    #         return redirect('firma_detay',firma_kod=firma_kod)
    # else:
    #     messages.error(request,'İşlemde yapılan firma size ait gözükmüyor')
    #     return redirect('firma_detay',firma_kod=firma_kod)

def toplu_urun_guncelle(request, firma_kod):
    firma = get_object_or_404(Firma, firma_kod=firma_kod)
    if (request.user.user_frm_kod == firma.firma_kod) or (request.user.username == 'orqerr' and request.user.user_frm_kod == "-1"):
        if request.method == 'POST':
            # FormData'dan gelen verileri al
            urun_id_list = request.POST.getlist('ürün_id')
            urun_adi_list = request.POST.getlist('ürün_adi')
            urun_fiyat_list = request.POST.getlist('ürün_fiyat')
            urun_durum_list = request.POST.getlist('ürün_durum')
            urun_kategori_list = request.POST.getlist('ürün_kategori')

            print("Alınan Ürünler:")
            for urun_id, urun_adi, urun_fiyat, urun_durum, urun_kategori_id in zip(urun_id_list, urun_adi_list, urun_fiyat_list, urun_durum_list, urun_kategori_list):
                print(f"Ürün ID: {urun_id}, Adı: {urun_adi}, Fiyat: {urun_fiyat}, Durum: {urun_durum}, Kategori ID: {urun_kategori_id}")

            # Güncellenecek ürünleri toplu bir şekilde al
            urunler = Urun.objects.filter(id__in=urun_id_list, urun_frm_kod=firma_kod)

            for urun, urun_adi, urun_fiyat, urun_durum, urun_kategori_id in zip(urunler, urun_adi_list, urun_fiyat_list, urun_durum_list, urun_kategori_list):
                # Ürün adını kontrol et, eğer boşsa eski ürün adını al
                if not urun_adi.strip():
                    urun_adi = urun.urun_ad
                urun.urun_ad = urun_adi
                
                # Fiyatı kontrol et, eğer boşsa eski fiyatı al
                if not urun_fiyat.strip():
                    urun_fiyat = urun.urun_fiyat
                urun.urun_fiyat = urun_fiyat
            
                urun.urun_durum = urun_durum
                urun.urun_kategori_id = urun_kategori_id

            # Tüm güncellemeleri tek bir save() çağrısı ile gerçekleştir
            try:
                Urun.objects.bulk_update(urunler, ['urun_ad', 'urun_fiyat', 'urun_durum', 'urun_kategori_id'])
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})

            # Başarılı bir şekilde güncellendiğine dair bir JSON yanıtı döndür
            return JsonResponse({'success': True})
        else:
            # POST isteği yapılmadıysa hata mesajı döndür
            return JsonResponse({'success': False, 'error': 'Sadece POST istekleri desteklenmektedir.'})
    else:
        messages.error(request,'istek yapılan firma size ait görünmüyor.')
        return redirect('admin_dashboard',firma_kod = firma_kod)
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt  # CSRF korumasını devre dışı bırakmak için eklenmiştir

def toplu_kategori_guncelle(request,firma_kod):
    firma = get_object_or_404(Firma,firma_kod =firma_kod)
    if (request.user.user_frm_kod == firma.firma_kod) or (request.user.username == 'orqerr' and request.user.user_frm_kod == "-1"):
        if request.method == 'POST':
            for key, value in request.POST.items():
                if key.startswith('kategori_adi_'):
                    kategori_id = key.split('_')[-1]
                    kategori = Kategori.objects.get(id=kategori_id)
                    kategori.kategori_ad = value
                    kategori.kategori_durum = request.POST.get('kategori_durum_' + kategori_id) == 'on'
                    kategori.save()
            messages.success(request,'Kategoriler Güncellendi Lütfen Kontrol Ediniz..')
            return redirect('admin_dashboard',firma_kod=firma_kod)  # İşlem tamamlandığında kullanıcıyı bir sayfaya yönlendirin veya başka bir işlem yapın
        else:
            # GET isteği durumunda gereken işlemler
            pass
    else:
        pass # firma kodu tutmazsa
# def siparis_ver(request, firma_kod):
#     firma = get_object_or_404(Firma, firma_kod=firma_kod)
#     kategoriler = Kategori.objects.filter(kategori_frm=firma, kategori_frm_kod=firma_kod)
    
#     # Kategori bazında ürünleri gruplayacak bir sözlük oluşturalım
#     kategorili_ürünler = {}
#     for kategori in kategoriler:
#         kategorili_ürünler[kategori] = Urun.objects.filter(urun_frm=firma, urun_frm_kod=firma_kod, urun_kategori=kategori)
#     print(kategorili_ürünler)

#     context = {
#         'firma': firma,
#         'kategoriler': kategoriler,
#         'kategorili_ürünler': kategorili_ürünler,
#     }
#     return render(request, 'siparis_ver.html', context)
from django.http import JsonResponse
import json
from .models import Siparis
import csv
def import_urun_from_excel(request):
    if request.method == "POST" and request.FILES.get("excel_file"):
        excel_file = request.FILES['excel_file']

        if not excel_file.name.endswith(('.xls', '.xlsx')):
            return render(request, 'error.html', {'message': 'Lütfen bir Excel dosyası yükleyin.'})

        # Excel dosyasını oku ve veritabanına ekle
        excel_data = xlrd.open_workbook(file_contents=excel_file.read())
        sheet = excel_data.sheet_by_index(0)  # İlk çalışma sayfasını kullan

        for row_num in range(1, sheet.nrows):  # Başlık satırını atla
            row = sheet.row_values(row_num)
            urun = Urun.objects.create(
                urun_frm_kod=row[0],
                urun_frm=Firma.objects.get(firma_kod=row[1]),  
                urun_ad=row[2],
                urun_kategori=Kategori.objects.get(kategori_adi=row[3]),  
                urun_durum=row[4],
                urun_fiyat=row[5],
                urun_kayit_user=row[6],
                urun_kayit_zaman=row[7]
            )
            print(urun)

        return render(request, 'excel_aktar.html', {'message': 'Excel dosyası başarıyla yüklendi.'})
    else:
        return render(request, 'excel_aktar.html', {'message': 'Lütfen bir dosya seçin ve yüklediğiniz dosyanın uygun bir format olduğundan emin olun.'})

def siparis_olustur(request, firma_kod):
    if request.method == 'POST':
        print('Siparis_oluştura geldi')
        # print(request.session["short_url"])
        received_data = json.loads(request.body.decode('utf-8'))
        urunler = received_data.get('urunler', [])
        siparis_masa = get_object_or_404(Masa, id=request.session["masa_num"])
        
        if not urunler:
            return JsonResponse({'error': 'Boş sipariş alınamaz.'}, status=400)

        son_siparis = Siparis.objects.filter(siparis_frm_kod=firma_kod).last()
        son_siparis_fis_num = son_siparis.siparis_fis_num + 1 if son_siparis else 0
        
        firma = get_object_or_404(Firma, firma_kod=firma_kod)
        siparis = Siparis.objects.create(
            siparis_frm_kod=firma_kod,
            siparis_frm=firma,
            siparis_fis_num=son_siparis_fis_num,
            siparis_masa=str(siparis_masa.masa_kat.kat_ad) + "-" + str(siparis_masa.masa_num),
            siparis_durum = 1
        )

        for urun_data in urunler:
            urun_id = urun_data.get('urun_id')
            miktar = urun_data.get('miktar')

            try:
                urun = Urun.objects.get(pk=urun_id)
                siparis_urun = SiparisUrun.objects.create(
                    siparis=siparis,
                    urun=urun,
                    miktar=miktar
                )
                print('siparis_oluştur')
                
                # WebSocket mesajı gönder
                channel_layer = get_channel_layer()
                print('channel_layera geldi')
                async_to_sync(channel_layer.group_send)(
                    "siparis_durumu",  # Grup adı
                    {
                        'type': 'siparis_durumu.update',  # Tüketici fonksiyonunu çağırmak için type belirtiyoruz
                        'firma_kod': firma_kod,  # Firma kodunu mesaja ekle
                        "message": "Sipariş durumu güncellendi!"  # Mesaj içeriği
                    }
                )
                print(f"Ürün ID: {urun_id}, Miktar: {miktar} - Siparişe eklendi.")
            except Urun.DoesNotExist:
                return JsonResponse({'error': f'Ürün bulunamadı: {urun_id}'}, status=400)

        return JsonResponse({'message': 'Sipariş başarıyla oluşturuldu.'})
    else:
        return JsonResponse({'error': 'Geçersiz istek methodu'}, status=405)

def siparis_takip(request, firma_kod):
    # Firma nesnesini al
    firma = get_object_or_404(Firma, firma_kod=firma_kod)
    
    # Kullanıcı kontrolü
    print(type(request.user.user_frm_kod))
    print(type(request.user.username))
    if not (request.user.user_frm_kod == firma.firma_kod) or (request.user.username == 'orqerr' and request.user.user_frm_kod == -1):
        return redirect('siparis_takip', firma_kod=request.user.user_frm_kod)
    
    # Firma koduna bağlı olarak sipariş ürünlerini filtrele
    bekleyen_siparisler = get_siparisler(firma, firma_kod,durum=1)
    print(bekleyen_siparisler)
    hazir_siparisler = get_siparisler(firma, firma_kod,durum=2)
    iptal_siparisler = get_siparisler(firma, firma_kod,durum=9) # Burada firma alanını kullanıyoruz
    # Context'i oluştur
    context = {
        'firma': firma,
        'iptal_siparisler':iptal_siparisler,
        'hazir_siparisler':hazir_siparisler,
        # 'onaylanan_siparisler':onaylanan_siparisler,
        # 'onaylanan_siparisler':onaylanan_siparisler,
        'bekleyen_siparisler': bekleyen_siparisler,
    }
    
    # Şablon dosyasını kullanarak render et ve HTTP yanıtını geri döndür
    return render(request, 'siparis_takip.html', context)        
def get_siparisler(firma, firma_kod, durum):
    return Siparis.objects.filter(siparis_frm=firma, siparis_frm_kod=firma_kod, siparis_durum=durum).select_related('siparis_frm')
def siparis_bar_takip(request, firma_kod):
    if not request.user.is_authenticated:
        return redirect('user_giris')
    
    firma = get_object_or_404(Firma, firma_kod=firma_kod)
    user = request.user
    
    if not (
    (request.user.username == 'orqerr' and request.user.user_frm_kod == "-1") or 
    (request.user.user_frm_kod == "-1" and user.user_tag == 'Destek') or 
    (request.user.user_frm_kod == firma.firma_kod)
    ):
        return redirect('siparis_takip', user.user_frm_kod)
    bekleyen_siparisler = get_siparisler(firma, firma_kod,durum=1)
    print('Bekleyen Siparişler',bekleyen_siparisler)
    hazirlanan_siparisler = get_siparisler(firma, firma_kod,durum=2)
    print('Hazirlanan Siparişler',hazirlanan_siparisler)
    iptal_siparisler = get_siparisler(firma, firma_kod,durum=9)
    print(iptal_siparisler)
    
    context = {
        'firma': firma,
        'iptal_siparisler': iptal_siparisler,
        'bekleyen_siparisler': bekleyen_siparisler,
        'hazirlanan_siparisler': hazirlanan_siparisler,
    }
    
    return render(request, 'siparis_bar_takip.html', context)
        
        
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# views.py

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from kuaförApp.apscheduler import schedule_task
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
def siparis_durumu_hazir(request,
    firma_kod, siparis_id):
    firma = get_object_or_404(Firma, firma_kod=firma_kod)
    if not (
    (request.user.username == 'orqerr' and request.user.user_frm_kod == "-1") or 
    (request.user.user_frm_kod == "-1" and request.user.user_tag =='Destek') or 
    (request.user.user_frm_kod == firma.firma_kod)
    ):
        messages.error(request, 'Bu Firmada İşlem Yapmaya Yetkiniz Bulunmuyor')
        return redirect('siparis_bar_takip', firma_kod=request.user.user_frm_kod)
    if request.method == "POST":
        
        siparis = get_object_or_404(Siparis, id=siparis_id)
        if siparis.siparis_frm_kod != firma_kod:
            messages.error(request, 'Bu sipariş firmanıza ait gözükmüyor')
            return redirect('siparis_bar_takip', firma_kod=request.user.user_frm_kod)
        siparis.siparis_durum = 2
        siparis.siparis_hazir_zaman = timezone.now()
        # siparis durum 2 hazır siparişler
        schedule_task(firma.firma_kod)
        print('schedule_task çalıştı')
        siparis.save()
        
        # WebSocket mesajı gönder
        channel_layer = get_channel_layer()
        print('channel_layera geldi')
        async_to_sync(channel_layer.group_send)(
            "siparis_durumu",  # Grup adı
            {
                'type': 'siparis_durumu.update',  # Tüketici fonksiyonunu çağırmak için type belirtiyoruz
                'firma_kod': firma_kod,  # Firma kodunu mesaja ekle
                "message": "Sipariş durumu güncellendi!"  # Mesaj içeriği
            }
        )

        # Anasayfaya yönlendirme yap
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request,'Hatalı Bir İşlem Yaptınız Hata Kodu : SP-001')
        return redirect(request.META.get('HTTP_REFERER',messages))

def siparis_durumu_hazir_degil(request,
    firma_kod, siparis_id):
    firma = get_object_or_404(Firma, firma_kod=firma_kod)
    if (request.user.username == "osqerr" and request.user.frm_kod =="-1") or (request.user.user_frm_kod == firma_kod):
        if request.method == "POST":
            
            siparis = get_object_or_404(Siparis, id=siparis_id)
            if siparis.siparis_frm_kod != firma_kod:
                messages.error(request, 'Bu sipariş firmanıza ait gözükmüyor')
                return redirect('siparis_bar_takip', firma_kod=request.user.user_frm_kod)
            siparis.siparis_durum = 1
            siparis.siparis_hazir_zaman = None
            # siparis durum 2 hazır siparişler
            schedule_task(firma.firma_kod)
            print('schedule_task çalıştı')
            siparis.save()
            
            # WebSocket mesajı gönder
            channel_layer = get_channel_layer()
            print('channel_layera geldi')
            async_to_sync(channel_layer.group_send)(
                "siparis_durumu",  # Grup adı
                {
                    'type': 'siparis_durumu.update',  # Tüketici fonksiyonunu çağırmak için type belirtiyoruz
                    'firma_kod': firma_kod,  # Firma kodunu mesaja ekle
                    "message": "Sipariş durumu güncellendi!"  # Mesaj içeriği
                }
            )

            # Anasayfaya yönlendirme yap
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request,'Hatalı Bir İşlem Yaptınız Hata Kodu : SP-001')
            return redirect(request.META.get('HTTP_REFERER',messages))
    else:
        messages.error(request, 'Bu Firmada İşlem Yapmaya Yetkiniz Bulunmuyor')
        return redirect('siparis_bar_takip', firma_kod=request.user.user_frm_kod)
def siparis_durumu_iptal(request,
    firma_kod, siparis_id):
    firma = get_object_or_404(Firma, firma_kod=firma_kod)
    if (request.user.username == "osqerr" and request.user.frm_kod =="-1") or (request.user.user_frm_kod == firma_kod):
        if request.method == "POST":
            
            siparis = get_object_or_404(Siparis, id=siparis_id)
            if siparis.siparis_frm_kod != firma_kod:
                messages.error(request, 'Bu sipariş firmanıza ait gözükmüyor')
                return redirect('siparis_bar_takip', firma_kod=request.user.user_frm_kod)
            siparis.siparis_durum = 9
            print('İptal Siparişe Gelen Sipariş',siparis.siparis_durum)
            # siparis durum 2 hazır siparişler
            siparis.save()

            # WebSocket mesajı gönder
            channel_layer = get_channel_layer()
            print('channel_layera geldi')
            async_to_sync(channel_layer.group_send)(
                "siparis_durumu",  # Grup adı
                {
                    'type': 'siparis_durumu.update',  # Tüketici fonksiyonunu çağırmak için type belirtiyoruz
                    'firma_kod': firma_kod,  # Firma kodunu mesaja ekle
                    "message": "Sipariş durumu güncellendi!"  # Mesaj içeriği
                }
            )

            # Anasayfaya yönlendirme yap
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request,'Hatalı Bir İşlem Yaptınız Hata Kodu : SP-001')
            return redirect(request.META.get('HTTP_REFERER',messages))
    else:
        messages.error(request, 'Bu Firmada İşlem Yapmaya Yetkiniz Bulunmuyor')
        return redirect('siparis_bar_takip', firma_kod=request.user.user_frm_kod)

########
        ####### 
# SHORT URL OLUŞTUR FİRMA İÇİN
# def add_short_url(request,firma_kod,masa_num):
#     firma = get_object_or_404(Firma,firma_kod = firma_kod)
#     masa_num = get_object_or_404(Masa,masa_frm_kod=firma_kod,masa_frm=firma,masa_num=masa_num)
#     pass

def masa_detay(request, firma_kod, masa_num, kat_ad):
    firma = get_object_or_404(Firma, firma_kod=firma_kod)
    kat = get_object_or_404(Kat, kat_ad=kat_ad, kat_firma=firma)
    masa = get_object_or_404(Masa, masa_frm_kod=firma_kod, masa_firma=firma, masa_num=masa_num, masa_kat=kat)
    
    short_url = None
    try:
        short_url = ShortUrl.objects.get(url_masa_num=masa)
    except ShortUrl.DoesNotExist:
        pass  # Kısaltılmış URL bulunamadı
    
    context = {
        'firma': firma,
        'masa': masa,
        'short_url': short_url,
    }
    return render(request, 'masa_detay.html', context)
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import ShortUrl, Firma, Masa
import string
import random
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
def generate_short_url():
    letters_and_digits = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(letters_and_digits) for i in range(8))
    return short_url
def create_qr_code_image(data):
    # QR kodunu oluştur
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # QR kodunu bir ByteIO nesnesine yaz
    qr_img = qr.make_image(fill_color="black", back_color="white")
    byte_io = BytesIO()
    qr_img.save(byte_io, format='PNG')

    return ContentFile(byte_io.getvalue())
from django.core.files import File
import os
def add_short_url(request, firma_kod, masa_kat, masa_num):
    if request.method == "POST":
        print('Masa Kat', masa_kat)
        firma = get_object_or_404(Firma, firma_kod=firma_kod)
        masa = get_object_or_404(Masa, masa_frm_kod=firma_kod, masa_firma=firma, masa_kat=masa_kat, masa_num=masa_num)

        short_url = generate_short_url()

        # Eski QR kodunu kontrol et ve sil
        existing_short_url_obj = ShortUrl.objects.filter(url_masa_num=masa)
        print('Esli qr bulundu',existing_short_url_obj)
        if existing_short_url_obj.exists():
            existing_short_url_obj = existing_short_url_obj.first()
            if existing_short_url_obj.url_qr_code:
                os.remove(existing_short_url_obj.url_qr_code.path)
                existing_short_url_obj.delete()
                print('Eski qr silin isilindi')

        # Kısa URL oluşturulduktan sonra veritabanına kaydedilir
        short_url_obj = ShortUrl.objects.create(url=short_url, url_frm=firma, url_frm_kod=firma_kod,
                                                url_frm_ip=request.META['REMOTE_ADDR'],
                                                url_masa_num=masa, url_masa_kat=masa.masa_kat)

        # Resim dosyasını oluşturun
        qr_code_url = f"http://192.168.1.5:8000/siparis_ver/{short_url}"
        qr_code_image = create_qr_code_image(qr_code_url)  # create_qr_code_image fonksiyonunu tanımlamanız gerekiyor

        # QR kodu resmini ShortUrl nesnesine yükleyin
        short_url_obj.url_qr_code.save(f'qr_code_{short_url}.png', File(qr_code_image))

        # Masa nesnesine kısa URL değerini kaydedin
        masa.masa_short_url = short_url
        masa.save()
        
        # Send success message to the page
        messages.success(request, f'QR code ve kısa URL başarıyla oluşturuldu: {short_url}')
        
        # Oluşturulan kısa URL'ye göre bir QR kodu oluşturulur
        return redirect('masa_detay',firma_kod=firma_kod,masa_num=masa.masa_num,kat_ad=masa.masa_kat.kat_ad)
    else:
        return HttpResponseBadRequest("Only POST requests are allowed.")
# HIZLI MASA İŞLEMLERİ
def masa_durum_degistir(request,firma_kod,id):
    yetki = get_object_or_404(Yetki,user=request.user)
    firma = get_object_or_404(Firma,firma_kod=firma_kod)
    if not (
    (request.user.username == 'orqerr' and request.user.user_frm_kod == "-1") or 
    (request.user.user_frm_kod == "-1" and yetki.masa_guncelle) or 
    (yetki.urun_guncelle and request.user.user_frm_kod == firma.firma_kod)
    ):
        messages.add_message(request, messages.ERROR, "Bu işleme yetkiniz bulunmuyor. Hata Kodu : MGYY:001")
        return redirect(request.META.get('HTTP_REFERER'))
    if not request.method == "POST":
            messages.add_message(request, messages.ERROR, "İstek Doğru Değil")
            return redirect(request.META.get('HTTP_REFERER'))
    
    masa = get_object_or_404(Masa, id=id)
    if masa.masa_durum == False:
        masa.masa_durum = True
    else:
        masa.masa_durum = False
    print(masa.masa_durum)
    masa.save()
    
    messages.add_message(request, messages.SUCCESS, "Masa Durumu Değiştirildi.")
    return redirect(request.META.get('HTTP_REFERER'))
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
def siparis_ekranina_git(request,firma_kod):
    try:
        short_url_obj = get_object_or_404(ShortUrl, url_frm_kod=firma_kod)
    except ShortUrl.DoesNotExist:
    # Handle the case where ShortUrl does not exist for the provided firma_kod
    # For example, redirect the user to an error page or display a meaningful message
        return HttpResponse("ShortUrl matching query does not exist.")
    request.session["short_url"] = "Yönetici"
    request.session["masa_num"] = short_url_obj.url_masa_num.id
    
    firma = short_url_obj.url_frm
    kategoriler = Kategori.objects.filter(kategori_frm=firma, kategori_frm_kod=firma.firma_kod)
        
    kategorili_ürünler = {}
    for kategori in kategoriler:
        kategorili_ürünler[kategori] = Urun.objects.filter(urun_frm=firma, urun_frm_kod=firma.firma_kod, urun_kategori=kategori)

    context = {
        'firma': firma,
        'kategoriler': kategoriler,
        'kategorili_ürünler': kategorili_ürünler,
    }
    return render(request, 'siparis_ver.html', context)
def siparis_ver(request, short_url):
    request.session['user_tag'] = 'müsteri'
    if 'short_url' in request.session and request.session['short_url'] != short_url:
    # Eski kısa URL'in bağlı olduğu masa bilgisini contexte ekle
        eski_masa = Masa.objects.get(masa_short_url=request.session['short_url'])
        context = {'eski_masa': eski_masa}
        return render(request, 'error.html', context)
    
    if 'short_url' not in request.session:
        print('Kullanıcı ilk defa bağlanıyor')
    
    short_url_obj = get_object_or_404(ShortUrl, url=short_url)
    request.session['short_url'] = short_url
    masa = get_object_or_404(Masa, masa_short_url=short_url_obj)
    request.session['masa_num'] = masa.id
    request.session['masa_zamani'] = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
    firma = short_url_obj.url_frm
    kategoriler = Kategori.objects.filter(kategori_frm=firma, kategori_frm_kod=firma.firma_kod)
        
    kategorili_ürünler = {}
    for kategori in kategoriler:
        kategorili_ürünler[kategori] = Urun.objects.filter(urun_frm=firma, urun_frm_kod=firma.firma_kod, urun_kategori=kategori)

    context = {
        'firma': firma,
        'kategoriler': kategoriler,
        'kategorili_ürünler': kategorili_ürünler,
    }
    return render(request, 'siparis_ver.html', context)


    
from urllib.parse import urlencode, urlparse, parse_qs
from datetime import datetime, timedelta
def admin_dashboard(request, firma_kod):
    if not request.user.is_authenticated:
         return redirect('user_giris')

    if request.user.username == "orqerr" and request.user.user_frm_kod == "-1":
        firmalar = Firma.objects.all()
    else:
        firmalar = None

    try:
        firma = Firma.objects.get(firma_kod=firma_kod)
    except Firma.DoesNotExist:
         messages.error(request, 'Firma Bulunamadı.')
         return redirect('admin_dashboard', request.user.user_frm_kod)

    yetki = get_object_or_404(Yetki, user=request.user)

    if not (request.user.username == "orqerr" or (request.user.user_frm_kod == "-1" and yetki.firmalari_listele)) and request.user.user_frm_kod != firma_kod:
         messages.error(request, 'Firma size ait görünmüyor.')
         return redirect('admin_dashboard', request.user.user_frm_kod)

    # Retrieve total number of orders for the given firm
    toplam_siparis = Siparis.objects.filter(siparis_frm_kod=firma_kod).count()

    # Retrieve all products for the given firm
    urunler = Urun.objects.filter(urun_frm_kod=firma_kod)

    # Check if view_all parameter is present in the request
    view_all = request.GET.get('view_all')

    # Prevent view_all parameter from being added multiple times to the URL
    if view_all == 'true':
        # Show all products without pagination
        paginator = None
    else:
        # Paginate products
        paginator = Paginator(urunler, 10)  # Show 10 products per page
        page_number = request.GET.get('page')
        try:
            urunler = paginator.page(page_number)
        except PageNotAnInteger:
            urunler = paginator.page(1)
        except EmptyPage:
            urunler = paginator.page(paginator.num_pages)

    # Retrieve tables, categories, and other related data
    masalar = Masa.objects.filter(masa_frm_kod=firma_kod)
    kategoriler = Kategori.objects.filter(kategori_frm=firma)
    katlar = Kat.objects.filter(kat_frm_kod=firma_kod).order_by('id')

    # Retrieve firm users
    firma_kullanicilari = FirmaUser.objects.filter(user_frm_kod=firma_kod)

    # Remove existing view_all parameter if present
    parsed_url = urlparse(request.get_full_path())
    query_params = parse_qs(parsed_url.query)
    if 'view_all' in query_params:
        del query_params['view_all']
    base_url = parsed_url.path + '?' + '&'.join([f"{key}={value[0]}" for key, value in query_params.items()])

    kalan_gun = (datetime.combine(firma.firma_bit_tar, datetime.min.time()) - datetime.now()).days if firma.firma_bit_tar else None

    context = {
        'firmalar': firmalar,
        'masaDüzenle': MasaDüzenle(),
        'kalan_gun': kalan_gun,
        'toplam_siparis': toplam_siparis,
        'kategoriler': kategoriler,
        'urunler': urunler,
        'kategoriForm': KategoriEkle(),
        'urunForm': UrunEkle(firma=firma),
        'katlar': katlar,
        'masalar': masalar,
        'katForm': KatEkle(),
        'masaForm': MasaEkle(),
        'düzenleForm': FirmaDüzenle(),
        'firma_kullanicilari': firma_kullanicilari,
        'userform': UserEkle(),
        'firma': firma,
        'paginator': paginator,
        'view_all': view_all,
        'base_url': base_url,
    }

    return render(request, 'admin_alani/admin_dashboard.html', context)
import uuid
from django.http import Http404
from django.core.exceptions import ValidationError
## uuid_kontrolünden geçir
def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False

def user_detail(request, firma_kod, uuid4):
    # UUID'nin geçerli bir formatta olup olmadığını kontrol et
    if is_valid_uuid(uuid4) != True:
        # Hatalı UUID formatı için hata mesajı göster
        messages.error(request, "Geçersiz UUID formatı")
        return redirect('admin_dashboard', request.user.user_frm_kod)

    try:
        user = FirmaUser.objects.get(unique_id=uuid4)
    except FirmaUser.DoesNotExist:
        messages.error(request, "Kullanıcı Bulunamadı")
        return redirect('admin_dashboard', request.user.user_frm_kod)

    yetki = get_object_or_404(Yetki, user=request.user)
    
    firma = get_object_or_404(Firma, firma_kod=firma_kod)
    

    yetkiler = Yetki.objects.all()
    context = {
        'firma': firma,
        'yetkiler': yetkiler,
        'user': user,
    }
    return render(request, 'admin_alani/user_detail.html', context)
from django.core.exceptions import ObjectDoesNotExist
def yetki_ver(request, firma_kod, uuid4):
    # Kullanıcı nesnesini al
    yetki = get_object_or_404(Yetki,user=request.user)
    if not ((request.user.username == "orqerr" and request.user.user_frm_kod == "-1") or
            (request.user.user_frm_kod == "-1" and yetki.kullanici_yetkilendir) or 
            (request.user.user_frm_kod == firma_kod and yetki.kullanici_yetkilendir)):
        messages.error(request, 'Kullanıcıyı Yetkilendiremezsiniz. Hata Kodu : KYYY:001')
        return redirect(request.META.get('HTTP_REFERER'))
    user = get_object_or_404(FirmaUser, unique_id=uuid4)

    # Eğer kullanıcıya henüz bir yetki atanmamışsa, yeni bir Yetki nesnesi oluşturun
    yetki, created = Yetki.objects.get_or_create(user=user)

    # POST isteğini kontrol et
    if request.method == 'POST':
        # Formdan gelen verileri al
        #listeleme yetkileri
        firmalari_listele = request.POST.get('firmalari_listele')
        tanimlari_listele = request.POST.get('tanimlari_listele')
        ürünleri_listele = request.POST.get('ürünleri_listele')
        masalari_listele = request.POST.get('masalari_listele')
        kategorileri_listele = request.POST.get('kategorileri_listele')
        kullanicilari_listele = request.POST.get('kullanicilari_listele')

        # ekleme düzenleme yetkileri
        firma_ekle = request.POST.get('firma_ekle')
        firma_duzenle = request.POST.get('firma_duzenle')
        kullanici_ekle = request.POST.get('kullanici_ekle')
        ürün_ekle = request.POST.get('ürün_ekle')
        konum_ekle = request.POST.get('konum_ekle')
        masa_ekle = request.POST.get('masa_ekle')
        kategori_ekle = request.POST.get('kategori_ekle')
        kullanici_kayit = request.POST.get('kullanici_kayit')
        kullanici_yetkilendir = request.POST.get('kullanici_yetkilendir')
        firma_sil = request.POST.get('firma_sil')


        # Kullanıcının yetkilerini güncelle
        # listeleme yetkileri
        yetki.firmalari_listele = True if firmalari_listele == 'on' else False
        yetki.tanimlari_listele = True if tanimlari_listele == 'on' else False
        yetki.ürünleri_listele = True if ürünleri_listele == 'on' else False
        yetki.masalari_listele = True if masalari_listele == 'on' else False
        yetki.kategorileri_listele = True if kategorileri_listele == 'on' else False
        yetki.kullanicilari_listele = True if kullanicilari_listele == 'on' else False
        # ekleme düzenleme 
        yetki.firma_ekle = True if firma_ekle == 'on' else False
        yetki.ürün_ekle = True if ürün_ekle == 'on' else False
        yetki.firma_duzenle = True if firma_duzenle == 'on' else False
        yetki.kullanici_ekle = True if kullanici_ekle == 'on' else False
        yetki.konum_ekle = True if konum_ekle == 'on' else False
        yetki.masa_ekle = True if masa_ekle == 'on' else False
        yetki.kategori_ekle = True if kategori_ekle == 'on' else False
        yetki.kullanici_kayit = True if kullanici_kayit == 'on' else False
        # pasife alma
        yetki.firma_sil = True if firma_sil == 'on' else False
        yetki.kullanici_yetkilendir = True if kullanici_yetkilendir == 'on' else False
        # Değişiklikleri kaydet
        yetki.save()

        # Başarılı işlem sonrası ana sayfaya yönlendirme
        messages.error(request, "Yetki Güncellemesi Yapıldı")
        return redirect(request.META.get('HTTP_REFERER'))

    # Eğer POST isteği değilse veya başarısız bir işlem varsa ana sayfaya yönlendir
    return redirect('home_url')
from django.http import HttpResponseServerError
import logging
from datetime import date
def user_update(request, firma_kod, uuid4):
    today = date.today()
    user = get_object_or_404(FirmaUser, unique_id=uuid4)
    firma = get_object_or_404(Firma, firma_kod=firma_kod)
    yetki = get_object_or_404(Yetki,user=request.user)
    # Yetki kontrolü
    if not (
    request.user.username == "orqerr" or 
    (request.user.user_frm_kod != "-1" and yetki.kullanici_guncelle) or 
    (yetki.kullanici_guncelle and request.user.user_frm_kod == user.user_frm_kod)
    ):
        messages.error(request, 'Bu Kullanıcı için bir güncelleme yapamazsınız. Hata Kodu : KGYY:001')
        return redirect('admin_dashboard', firma_kod=request.user.user_frm_kod)

    # HTTP method kontrolü
    if request.method != "POST":
        messages.error(request, "Hatalı Bir İstekte Bulundunuz")
        return redirect(request.META.get('HTTP_REFERER'))

    # Form oluşturma ve geçerlilik kontrolü
    form = UserUpdateForm(request.POST,request.FILES, instance=user)
    if not form.is_valid():
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}")
        return redirect(request.META.get('HTTP_REFERER'))

    # Doğum tarihi kontrolü
    user_dogum_tarihi = form.cleaned_data.get("user_dogum_tarihi")
    if user_dogum_tarihi is not None and user_dogum_tarihi >= today:
        messages.error(request, "Geçerli bir doğum tarihi giriniz.")
        return redirect(request.META.get('HTTP_REFERER'))

    try:
        form.save()
        messages.success(request, "Güncelleme İşlemi Başarılı")
        return redirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        print(e)
        return HttpResponseServerError("Güncelleme işlemi sırasında bir hata oluştu. Lütfen daha sonra tekrar deneyin.")
def id_bul(request):
    yetkiler = Permission.objects.all()
    context = {
        'yetkiler':yetkiler,
    }
    return render(request,'id_bul.html',context)
def user_logout(request):
    logout(request)
    return redirect('user_giris')
def hata_bildir(request):
    pass
def y(user, permission_name):
    try:
        yetki = Yetki.objects.get(user=user)
        # İzin adını kullanarak ilgili boolean alanı alın
        permission_value = getattr(yetki, permission_name, False)
        return permission_value
    except Yetki.DoesNotExist:
        return False

def firma_durumunu_aktiflestir(request, firma_kod):
    user = request.user
    if not ((user.username == "orqerr" and user.user_frm_kod == "-1") or 
            (user.user_frm_kod == "-1" and user.yetkiler.firma_durum_degistir)):
            messages.error(request, "Bu işleme yetkiniz bulunmuyor.")
            return redirect(request.META.get('HTTP_REFERER'))
    if not request.method == "POST":
        messages.error(request, "Bu istekler kabul edilmez.")
        return redirect(request.META.get('HTTP_REFERER'))
    firma_bit_tar = request.POST.get('firma_bit_tar')
    print(firma_bit_tar)
    firma = get_object_or_404(Firma,firma_kod=firma_kod)
    firma.firma_bit_tar = firma_bit_tar
    firma.firma_durum = True
    firma.save()
    messages.success(request,f" Firma bitiş tarihi {firma.firma_bit_tar} tarihine kadar uzatıldı")
    return redirect(request.META.get('HTTP_REFERER'))
def give_all_permissions(request):
    # Kullanıcıyı al
    if request.user.username == "orqerr" and request.user.user_frm_kod == "-1":
        messages.error(request, "Bu işleme yetkiniz bulunmuyor. Bu işlemi sadece geliştirici yapabilir.")
        return redirect('admin_dashboard',request.user_frm_kod)
    else:
        user = get_object_or_404(FirmaUser, id=999999)

        # Kullanıcının Yetki modelini oluştur veya var olanı al
        yetki, created = Yetki.objects.get_or_create(user=user)

        # Tüm yetki alanlarını döngü içinde True olarak ayarla
        for field in Yetki._meta.fields:
            if field.name != 'user':  # Kullanıcı alanını atla
                setattr(yetki, field.name, True)

        # Değişiklikleri kaydet
        yetki.save()

        # İşlem başarılı olduysa bir JSON yanıtı gönder
        return JsonResponse({'message': 'Tüm yetkiler başarıyla verildi.'})
