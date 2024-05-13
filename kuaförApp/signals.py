import os
import qrcode
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Masa, Yetki

def generate_qr_code(firma_kod, masa_kat, masa_num):
    data = f"{firma_kod}-{masa_kat}-{masa_num}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Firma klasörünü oluştur
    firm_folder = os.path.join('media', 'qr_codes', f'{firma_kod}')
    os.makedirs(firm_folder, exist_ok=True)

    img_path = os.path.join(firm_folder, f'{firma_kod}-{masa_kat}-{masa_num}.png')
    
    img.save(img_path)
    return img_path

@receiver(post_save, sender=Masa)
def create_qr_code(sender, instance, created, **kwargs):
    if created:
        qr_code_filename = f'{instance.masa_firma.firma_kod}-{instance.masa_kat}-{instance.masa_num}.png'
        generate_qr_code(
            instance.masa_firma.firma_kod,
            instance.masa_kat,
            instance.masa_num
        )
        instance.qr_code = qr_code_filename
        instance.save()
from django.db.models.signals import pre_migrate
from django.dispatch import receiver
from django.contrib.auth.management import create_permissions
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Permission
from django.apps import apps
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
@receiver(post_migrate)
def cleanup_and_add_permissions(sender, **kwargs):
    with transaction.atomic():
        # Mevcut izinleri sil
        Permission.objects.all().delete()
from django.db.models.signals import pre_save
@receiver(post_save, sender=Yetki)
def assign_permissions_to_specific_user(sender, instance, created, **kwargs):
    print('assign_permissiona geldi')
    if created and instance.user_id == 999999:
        # Eğer yeni bir Yetki öğesi oluşturulduysa ve kullanıcı ID'si 999999 ise,
        # bu öğeyi belirli kullanıcıya atayın.
        for field in Yetki._meta.fields:
            if field.name != 'user':  # Kullanıcı alanını atla
                setattr(instance, field.name, True)
        instance.save()