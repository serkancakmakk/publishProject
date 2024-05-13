from django.conf import settings
from django.contrib.auth.models import Permission

from .models import Yetki
def user_permissions(request):
    print("Context processor çalıştı.")  # Context processor'ın çalıştığını kontrol etmek için print satırı
    # Kullanıcı anonim ise, boş bir yetkiler sözlüğü döndür
    if request.user.is_anonymous:
        return {'yetkiler': {}}

    # Kullanıcının özel izinlerini al
    try:
        yetkiler = request.user.yetkiler
    except Yetki.DoesNotExist:
        # Kullanıcıya özel izinler henüz tanımlanmamışsa
        yetkiler = None

    # Kullanıcının özel izinlerini içeren bir sözlük döndür
    if yetkiler:
        yetki_dict = {
            'firma_ekle': yetkiler.firma_ekle,
            'firma_duzenle': yetkiler.firma_duzenle,
            'kullanici_ekle': yetkiler.kullanici_ekle,
            'ürün_ekle': yetkiler.ürün_ekle,
            'konum_ekle': yetkiler.konum_ekle,
            'masa_ekle': yetkiler.masa_ekle,
            'kategori_ekle': yetkiler.kategori_ekle,
            'firmalari_listele': yetkiler.firmalari_listele,
            'tanimlari_listele': yetkiler.tanimlari_listele,
            'ürünleri_listele': yetkiler.ürünleri_listele,
            'masalari_listele': yetkiler.masalari_listele,
            'kategorileri_listele': yetkiler.kategorileri_listele,
            'kullanicilari_listele': yetkiler.kullanicilari_listele,
            'kullanici_guncelle':yetkiler.kullanici_guncelle,
            'masa_guncelle':yetkiler.masa_guncelle,
            'urun_guncelle':yetkiler.urun_guncelle,
            'kullanici_yetkilendir':yetkiler.kullanici_yetkilendir,
            'kullanici_kayit': yetkiler.kullanici_kayit,
            'guncelleme_talepleri':yetkiler.guncelleme_talepleri,
            'hata_talepleri':yetkiler.hata_talepleri,
            'firma_durum_degistir':yetkiler.firma_durum_degistir,
        }
    else:
        yetki_dict = {}
    # orqerr kullanıcısı için tüm yetkileri True olarak ayarla
    if request.user.username == 'orqerr':
        yetki_dict = {key: True for key in yetki_dict}

    print("Kullanıcı yetkileri:", yetki_dict)  # Kullanıcı yetkilerini kontrol etmek için print satırı
    return {'yetkiler': yetki_dict}

from django.utils import timezone

def check_first_time_connection(request):
    masa_baglanma_zamani = request.session.get('masa_zamani')  # Oturumdan masa bağlanma zamanını al
    if masa_baglanma_zamani is None:  # Eğer masa bağlanma zamanı yoksa
        print('Kullanıcı ilk defa bağlanıyor')
        request.session['masa_zamani'] = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
        return {}
    else:
        print('Kullanıcı daha önce masaya bağlanmış')
        return {}
def clear_inactive_sessions(request):
    masa_baglanma_zamani = request.session.get('masa_zamani')  # Oturumdan masa bağlanma zamanını al
    print('cp den gelen zaman',masa_baglanma_zamani)
    if 'masa_zamani' in request.session:  # 'masa_zamani' anahtarının varlığını kontrol et
        masa_baglanma_zamani = timezone.make_aware(timezone.datetime.strptime(masa_baglanma_zamani, "%Y-%m-%d %H:%M:%S"))
        simdi = timezone.now()
        if (simdi - masa_baglanma_zamani) >= timezone.timedelta(minutes=3):
            print((simdi - masa_baglanma_zamani) >= timezone.timedelta(minutes=3))
            del request.session['masa_zamani']  # 3 dakikadan fazla süredir masa bağlanma zamanı yoksa oturumdan sil
            if 'short_url' in request.session:  # 'short_url' anahtarının varlığını kontrol et
                del request.session['short_url']
            print('masa_zamani_silindi')

def custom_context_processor(request):
    clear_inactive_sessions(request)  # Her istekte masa bağlanma zamanlarını kontrol et
    return {}  # Diğer context processor'lar gibi boş bir sözlük döndür bu context processorum herhangi bir işlem yapılırken sayfaya bağlanmamı engelliyor
