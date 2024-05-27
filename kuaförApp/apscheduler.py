# apscheduler.py veya tasks.py

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Siparis, UpdateRequest
def tamamlanmamis_siparisleri_kontrol_et(firma_kod):
    now = timezone.now()
    five_minutes_ago = now - timezone.timedelta(minutes=5)
    tamamlanmamis_siparisler = Siparis.objects.filter(siparis_hazir_zaman__lte=five_minutes_ago, siparis_frm_kod=firma_kod, siparis_durum=2)
    
    for siparis in tamamlanmamis_siparisler:
        # Siparişin durumunu tamamlandı olarak güncelle
        siparis.siparis_durum = 9
        siparis.save()
def iptal_siparisleri_kontrol_et(firma_kod):
    now = timezone.now()
    five_minutes_ago = now - timezone.timedelta(seconds=10)
    iptal_edilen_siparisler = Siparis.objects.filter(siparis_hazir_zaman__lte=five_minutes_ago, siparis_frm_kod=firma_kod, siparis_durum=9)
    
    for siparis in iptal_edilen_siparisler:
        # Siparişin durumunu tamamlandı olarak güncelle
        siparis.siparis_durum = 8
        siparis.save()

def schedule_task(firma_kod):
    print('schedule_task çalıştı')
    scheduler = BackgroundScheduler()
    scheduler.add_job(tamamlanmamis_siparisleri_kontrol_et, 'interval', minutes=1, args=[firma_kod])
    scheduler.add_job(iptal_siparisleri_kontrol_et, 'interval', minutes=1, args=[firma_kod])


    scheduler.start()
    print('SCHEDULER BAŞLADI')
def delete_expired_update_requests_task():
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_expired_update_requests, 'cron', minute='*/5')

    scheduler.start()
    print('SCHEDULER BAŞLADI')
def delete_expired_update_requests():
    print('Scheduler Çalıştı')
    thirty_seconds_ago = timezone.now() - timezone.timedelta(seconds=30)
    expired_update_requests = UpdateRequest.objects.filter(created_at__lte=thirty_seconds_ago, is_active=False)
    expired_update_requests.delete()
