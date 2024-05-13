from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # orqerr hızlı işlemler
    path('firma_durumunu_aktiflestir/<str:firma_kod>/', views.firma_durumunu_aktiflestir, name='firma_durumunu_aktiflestir'),
    path('', views.user_giris, name='user_giris'),
    path('id_bul', views.id_bul, name='id_bul'),
    path('api/get-user-location/', views.get_user_location, name='get_user_location'),
    path('firma_ekle', views.firma_ekle, name='firma_ekle'),
    path('firma_düzenle/<int:pk>/<str:firma_kod>/', views.firma_düzenle, name='firma_düzenle'),
    path('check_ip_address/', views.check_ip_address, name='check_ip_address'),
    path('firma_detay/<str:firma_kod>', views.firma_detay, name='firma_detay'),
    path('user_ekle/<str:firma_kod>/', views.user_ekle, name='user_ekle'),
    path('güncelleme_talep_eden_sirketler',views.company_update_requests,name="güncelleme_talep_eden_sirketler"),
    path('user_giris/', views.user_giris, name='user_giris'),
    path('user_login/', views.user_login, name='user_login'),
    path('logout/', views.logout, name='user_logout'),
    ####
        ####
            #####
    path('tum_firmalar/',views.tum_firmalar,name="tum_firmalar"),
    path('admin_dashboard/<str:firma_kod>', views.admin_dashboard, name='admin_dashboard'),
    path('user_update/<str:firma_kod>/<uuid:uuid4>/', views.user_update, name='user_update'),
    path('yetki_ver/<str:firma_kod>/<uuid:uuid4>/', views.yetki_ver, name='yetki_ver'),
    ####
        ####
            #####
    path('tum_kullanicilar',views.tum_kullanicilar,name='tum_kullanicilar'),
    path('kullanici_detay/<str:uuid4>',views.kullanici_detay,name='kullanici_detay'),
    path('excel_aktar',views.excel_aktar,name='excel_aktar'),
    path('firma_detay_redirect',views.firma_detay_redirect,name='firma_detay_redirect'),
    ####
        ####
            #####
    path('kat_ekle/<str:firma_kod>',views.kat_ekle,name='kat_ekle'),
    path('kat_düzenle/<str:firma_kod>/',views.kat_düzenle,name="kat_düzenle"),
    ####
        ####
            #####
    
    path('masa_ekle/<str:firma_kod>/',views.masa_ekle,name='masa_ekle'),
    path('masa_düzenle/<str:firma_kod>/',views.masa_düzenle,name="masa_düzenle"),
    path('masa_detay/<str:firma_kod>/<str:masa_num>/<str:kat_ad>/',views.masa_detay,name="masa_detay"),
    ####
        ####
            #####
    
    path('kategori_ekle/<str:firma_kod>/',views.kategori_ekle,name='kategori_ekle'),
    path('kategori_düzenle/<str:firma_kod>', views.kategori_düzenle, name='kategori_düzenle'),

    # path('masa_düzenle/<str:firma_kod>/<int:masa_id>',views.masa_düzenle,name="masa_düzenle")
    path('toplu_kategori_guncelle/<str:firma_kod>/', views.toplu_kategori_guncelle, name='toplu_kategori_guncelle'),
    ####
        ####
            #####
    path('urun_ekle/<str:firma_kod>',views.urun_ekle,name='urun_ekle'),
    path('urun_guncelle/<str:firma_kod>',views.urun_guncelle,name='urun_guncelle'),
    # path('ürün_düzenle/<str:firma_kod>/<int:ürün_id>',views.ürün_düzenle,name='ürün_düzenle'),
    path('toplu_urun_guncelle/<str:firma_kod>/', views.toplu_urun_guncelle, name='toplu_urun_guncelle'),
    ####
        ####
            #####
     path('siparis_ver/<str:short_url>',views.siparis_ver,name='siparis_ver'),            
     path('siparis_ver/<str:firma_kod>',views.siparis_ver,name='siparis_ver'),
     path('siparis_olustur/<str:firma_kod>', views.siparis_olustur, name='siparis_olustur'),
     path('siparis_takip/<str:firma_kod>/', views.siparis_takip, name='siparis_takip'),
     path('siparis_bar_takip/<str:firma_kod>/', views.siparis_bar_takip, name='siparis_bar_takip'),
     ####
        ####
            #####
    path('siparis_durumu_hazir/<str:firma_kod>/<int:siparis_id>/', views.siparis_durumu_hazir, name='siparis_durumu_hazir'),
    path('siparis_durumu_iptal/<str:firma_kod>/<int:siparis_id>/', views.siparis_durumu_iptal, name='siparis_durumu_iptal'),
    path('siparis_durumu_hazir_degil/<str:firma_kod>/<int:siparis_id>/', views.siparis_durumu_hazir_degil, name='siparis_durumu_hazir_degil'),
     ####
        ####
            #####
    path('add_short_url/<str:firma_kod>/<int:masa_kat>/<str:masa_num>/',views.add_short_url, name='add_short_url'),
    ####
        ####
            #####
    path('user/<str:firma_kod>/<str:uuid4>/',views.user_detail, name='user_detail'),
    ####
        #### HIZLI MASA İŞLEMLERİ
            #####
    path('masa_durum_degistir/<int:id>/<str:firma_kod>',views.masa_durum_degistir, name='masa_durum_degistir'),
    path('user_logout/',views.user_logout, name='user_logout'),
    path('hata_bildir/<str:kod>/', views.hata_bildir, name='hata_bildir'),
    path('give_all_permissions/',views.give_all_permissions,name="give_all_permissions"),
    path('siparis_ekranina_git/<str:firma_kod>',views.siparis_ekranina_git,name="siparis_ekranina_git"),
    path('güncelleme_talep_et/<str:firma_kod>',views.request_an_update,name="güncelleme_talep_et"),
     path('güncelleme_talebini_geri_al/<str:firma_kod>',views.undo_update_request,name="güncelleme_talebini_geri_al"),
    path('güncelleme_talebini_kapat/<str:firma_kod>',views.close_update_request,name="güncelleme_talebini_kapat"),
    # user işlemleri
    path('sifre_degistir/<int:user_id>',views.change_password,name="sifre_degistir"),
    # hata bildirimi
    path('hata_bildir/',views.create_error_report,name="hata_bildir"),
    path('hata_sil/<int:id>',views.delete_error_report,name="hata_sil"),
  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)