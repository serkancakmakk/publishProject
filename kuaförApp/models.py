import errno
from django.db import models
import random
import string

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
# Create your models here.
class Firma(models.Model):
    firma_kod = models.CharField(max_length=6, unique=True)  # random 8-10 karakter
    firma_adi = models.CharField(max_length=255, null=False, blank=False)
    firma_adres=models.CharField(max_length=255)
    firma_telefon=models.CharField(max_length=255)
    firma_telefon2=models.CharField(max_length=255,null=True,blank=True)
    firma_sehir=models.CharField(max_length=255)
    firma_ilce=models.CharField(max_length=255)
    firma_ünvan = models.CharField(max_length=255, null=False, blank=False)
    firma_dis_ip = models.CharField(max_length=255, null=False, blank=False)  # unique=True
    firma_durum = models.BooleanField(default=True)  # 1 açık 0 kapalı
    firma_bas_tar = models.DateTimeField(null=False, blank=False)
    firma_bit_tar = models.DateTimeField(null=False, blank=False)
    firma_create_user = models.CharField(max_length=255, null=True, blank=True)
    firma_create_time = models.DateTimeField(auto_now_add=True)
    price_in_use = models.BooleanField(default=False)
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission
import uuid
from django.utils.timezone import now
def user_image_path(instance, filename):
    # instance içinden firma_kodunu ve user_adi_soyadi bilgisini alalım
    firma_kod = instance.user_frm_kod  # Firma kodunu almak için firma_kod'a erişiyoruz
    user_adi_soyadi = f"{instance.user_adi}_{instance.user_soyad}"
    
    # media klasörünün içinde 'user_images' adında bir klasör oluşturalım
    upload_dir = os.path.join('user_images', firma_kod)
    
    # Eğer firma_koduna ait klasör yoksa, oluşturalım
    if not os.path.exists(upload_dir):
        try:
            os.makedirs(upload_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    # Dosya adını ve uzantısını oluşturalım
    timestamp = now().strftime('%Y%m%d_%H%M%S')
    _, ext = os.path.splitext(filename)
    new_filename = f"{user_adi_soyadi}_{timestamp}{ext}"

    # Dosya yolu olarak upload_dir içine yeni dosya adıyla dönelim
    return os.path.join(upload_dir, new_filename)
class UpdateRequest(models.Model):
    req_company_code = models.CharField(max_length=10)
    req_user = models.CharField(max_length=255)
    company_code = models.BooleanField(default=False)
    company_name = models.BooleanField(default=False)
    company_address = models.BooleanField(default=False)
    company_phone = models.BooleanField(default=False)
    company_city = models.BooleanField(default=False)
    company_district = models.BooleanField(default=False)
    company_title = models.BooleanField(default=False)
    company_external_ip = models.BooleanField(default=False)
    company_status = models.BooleanField(default=False)
    company_agreement_expiry_date = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class FirmaUser(AbstractUser):
    user_firma = models.ManyToManyField(Firma, related_name='firma_users')
    user_frm_kod = models.CharField(max_length=255, null=True)
    user_image = models.ImageField(upload_to=user_image_path, blank=True, null=True)
    user_adi = models.CharField(max_length=255,null=True,blank=True)
    user_soyad = models.CharField(max_length=255,null=True,blank=True)
    user_telefon = models.CharField(max_length=255,null=True,blank=True)
    user_adres = models.CharField(max_length=255,null=True,blank=True)
    GENDER_CHOICES = (
        ('E', 'Erkek'),
        ('K', 'Kadın'),
        ('B', 'Belirtilmedi'),
    )
    
    # Choices listesini kullanarak cinsiyet alanı tanımlama
    user_cinsiyet = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True, null=True,default="Belirtilmedi")
    user_dogum_tarihi = models.DateField(null=True,blank=True)
    user_email = models.EmailField(null=True,blank=True)
    user_durum = models.BooleanField(default=True)
    user_kayit_user = models.CharField(max_length=255, null=True, blank=True)
    user_kayit_zaman = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(Group, related_name='firma_users')
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Özel kullanıcı kimliği
    username = models.CharField(max_length=30)
    user_tag = models.CharField(max_length=30,null=True,blank=True)
    USERNAME_FIELD = 'unique_id'
    def __str__(self):
        return self.username
class Yetki(models.Model):
    # Kullanıcıya özel izinler
    user = models.OneToOneField(FirmaUser, on_delete=models.CASCADE, related_name='yetkiler')
    firma_ekle = models.BooleanField(default=False)
    firma_duzenle = models.BooleanField(default=False)
    #
    kullanici_ekle= models.BooleanField(default=False)
    ürün_ekle= models.BooleanField(default=False)
    konum_ekle= models.BooleanField(default=False)
    masa_ekle= models.BooleanField(default=False)
    kategori_ekle= models.BooleanField(default=False)
    #
    firmalari_listele = models.BooleanField(default=False)
    tanimlari_listele= models.BooleanField(default=False)
    ürünleri_listele= models.BooleanField(default=False)
    masalari_listele= models.BooleanField(default=False)
    kategorileri_listele= models.BooleanField(default=False)
    ürünleri_listele= models.BooleanField(default=False)
    kullanicilari_listele = models.BooleanField(default=False)
    kullanici_güncelle = models.BooleanField(default=False)
    #
    #düzenleme
    masa_guncelle = models.BooleanField(default=False)
    konum_güncelle = models.BooleanField(default=False)
    kullanici_guncelle = models.BooleanField(default=False)
    urun_guncelle = models.BooleanField(default=False)
    kullanici_kayit= models.BooleanField(default=False)
    firma_sil = models.BooleanField(default=False)
    parametre_degistir = models.BooleanField(default=False)
    # yetkilendir
    kullanici_yetkilendir = models.BooleanField(default=False)
    # güncelleme ve destek taleplerini gör
    guncelleme_talepleri = models.BooleanField(default=False)
    hata_talepleri = models.BooleanField(default=False)
    firma_durum_degistir = models.BooleanField(default=False)
    deneme_yetki = models.BooleanField(default=False)
    deneme_yetki1 = models.BooleanField(default=False)
    deneme_yetki2 = models.BooleanField(default=False)
    deneme_yetki3 = models.BooleanField(default=False)
    deneme_yetki4 = models.BooleanField(default=False)
    deneme_yetki5 = models.BooleanField(default=False)
    deneme_yetki6 = models.BooleanField(default=False)
    deneme_yetki7 = models.BooleanField(default=False)
    deneme_yetki8 = models.BooleanField(default=False)
    def assign_permissions_to_specific_user(self):
        # Eğer Yetki öğesi yeni oluşturulduysa ve kullanıcı ID'si 999999 ise,
        # belirli kullanıcıya yetkileri atar.
        print('çalıştır')
        user = get_object_or_404(FirmaUser, id=999999)

        # Kullanıcının Yetki modelini oluştur veya var olanı al
        yetki, created = Yetki.objects.get_or_create(user=user)

        # Tüm yetki alanlarını döngü içinde True olarak ayarla
        for field in Yetki._meta.fields:
            if field.name != 'user':  # Kullanıcı alanını atla
                setattr(yetki, field.name, True)

        # Değişiklikleri kaydet
        yetki.save()
class Kat(models.Model):
    kat_firma = models.ForeignKey(Firma, on_delete=models.CASCADE)
    kat_frm_kod = models.CharField(max_length=20)
    kat_ad = models.CharField(max_length=20)
    kat_durum = models.BooleanField(default=True)
    kat_kayit_tar = models.DateTimeField(auto_now_add=True)
    kat_kayit_user = models.CharField(max_length=50)
    def __str__(self):
        return self.kat_ad
class Masa(models.Model):
    masa_firma = models.ForeignKey(Firma, on_delete=models.CASCADE)
    masa_frm_kod = models.CharField(max_length=20)
    masa_num = models.CharField(max_length=20)
    masa_kat = models.ForeignKey(Kat,on_delete=models.CASCADE)
    masa_durum = models.BooleanField(default=True)
    masa_kayit_tar = models.DateTimeField(auto_now_add=True)
    masa_kayit_user = models.CharField(max_length=50)
    masa_short_url = models.CharField(unique=True,null=True,blank=True)
    def __str__(self):
        return self.masa_num
def kategori_resim_yolu(instance, dosya_adı):
    klasor_adi = f"{instance.kategori_frm_kod}_{instance.kategori_frm_kod}"
    return os.path.join('product_images', klasor_adi, dosya_adı)
class Kategori(models.Model):
    kategori_frm_kod = models.CharField(max_length=20)
    kategori_frm = models.ForeignKey(Firma, on_delete=models.CASCADE)
    kategori_kod = models.CharField(max_length=20)
    kategori_ad  = models.CharField(max_length=20)
    kategori_image = models.ImageField(upload_to=kategori_resim_yolu, null=True, blank=True)
    kategori_durum  = models.BooleanField(default=True)
    kategori_kayit_user = models.CharField(max_length=20)
    kategori_kayit_zaman = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.kategori_ad
import os
from django.conf import settings
def urun_resim_yolu(instance, dosya_adı):
    klasor_adi = f"{instance.urun_frm_kod}_{instance.urun_frm_kod}"
    return os.path.join('product_images', klasor_adi, dosya_adı)

class Urun(models.Model):
    urun_frm_kod = models.CharField(max_length=20)
    urun_frm  = models.ForeignKey(Firma, on_delete=models.CASCADE)
    urun_ad = models.CharField(max_length=255)
    urun_kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    urun_durum = models.BooleanField(default=True)
    urun_img = models.ImageField(upload_to=urun_resim_yolu, null=True, blank=True)
    urun_fiyat = models.IntegerField(null=True,blank=True)
    urun_kayit_user = models.CharField(max_length=20)
    urun_kayit_zaman = models.DateTimeField(auto_now_add=True)
class Siparis(models.Model):
    siparis_frm_kod = models.CharField(max_length=20)
    siparis_frm = models.ForeignKey(Firma, on_delete=models.CASCADE)
    siparis_fis_num = models.IntegerField()
    siparis_tar = models.DateTimeField(auto_now_add=True)
    siparis_sıra_num = models.IntegerField(null=True, blank=True)
    SIPARIS_DURUM_CHOICES = (
        (1, 'Bekleyen'),
        (2, 'Hazırlandı'),
        (3, 'Tamamlandı'),
        (8, 'İptal Edilip Silindi'),
        (9, 'İptal Edildi'),
    )
    siparis_durum = models.IntegerField(choices=SIPARIS_DURUM_CHOICES, default=0)
    siparis_kayıt_zaman = models.DateTimeField(auto_now_add=True)
    siparis_hazir_zaman = models.DateTimeField(null=True, blank=True)
    siparis_masa = models.CharField(max_length=50)

class SiparisUrun(models.Model):
    siparis = models.ForeignKey(Siparis, on_delete=models.CASCADE, related_name='siparis_urunleri')
    urun = models.ForeignKey(Urun, on_delete=models.CASCADE)
    miktar = models.IntegerField()
    def __str__(self):
        return f"{self.urun} - Miktar: {self.miktar}"
def get_media_path(instance, filename):
    # Örneğin, 'media/firma_kodu/masa_numarasi/konum' olarak dosya yolu oluştur
    return os.path.join('media', str(instance.url_frm.firma_kod), str(instance.url_masa_num.masa_num), instance.url_masa_kat.kat_ad, filename)
class ShortUrl(models.Model):
    url = models.CharField(max_length=20)
    url_frm = models.ForeignKey(Firma,to_field='firma_kod',on_delete=models.CASCADE)
    url_frm_kod = models.CharField(max_length=6)
    url_frm_ip = models.CharField(max_length=25)
    url_masa_num = models.ForeignKey(Masa, on_delete=models.CASCADE)
    url_masa_kat = models.ForeignKey(Kat,on_delete=models.CASCADE)
    url_durum = models.BooleanField(default=1)
    url_qr_code = models.ImageField(upload_to=get_media_path)
    def __str__(self):
        return self.url
class ErrorReport(models.Model):
    error_code = models.CharField(max_length=15)
