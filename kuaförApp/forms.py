from django import forms

from .models import Firma,FirmaUser, Kat, Kategori, Masa, Urun,UpdateRequest


class FirmaEkle(forms.ModelForm):
    class Meta:
        model = Firma
        fields = ['firma_adi', 'firma_ünvan', 'firma_adres', 'firma_telefon', 'firma_telefon2', 'firma_sehir', 'firma_ilce', 'firma_dis_ip', 'firma_durum', 'firma_bas_tar', 'firma_bit_tar', 'firma_create_user']
        widgets = {
            'firma_bas_tar': forms.DateInput(attrs={'type': 'date'}),
            'firma_bit_tar': forms.DateInput(attrs={'type': 'date'}),
        }
class FirmaDüzenle(forms.ModelForm):
    class Meta:
        model = Firma
        fields = ['firma_adi', 'firma_ünvan', 'firma_adres','firma_telefon','firma_telefon2','firma_sehir','firma_ilce','firma_dis_ip','firma_durum','firma_bit_tar','price_in_use']
###
        ####
                ####
class UserEkle(forms.ModelForm):
    class Meta:
        model = FirmaUser
        fields = ['user_adi', 'user_soyad', 'user_durum','username', 'password']
###
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = FirmaUser
        fields = ['user_adi','username','user_soyad', 'user_telefon', 'user_adres', 'user_cinsiyet', 'user_dogum_tarihi', 'user_email', 'user_durum','user_image']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['user_cinsiyet'].widget = forms.Select(choices=FirmaUser.GENDER_CHOICES)

    def clean_user_cinsiyet(self):
        user_cinsiyet = self.cleaned_data.get('user_cinsiyet')
        if user_cinsiyet not in ['E', 'K', 'B']:
            raise forms.ValidationError("Geçerli bir cinsiyet seçin.")
        return user_cinsiyet
    ####
        ####
class KatEkle(forms.ModelForm):
    class Meta:
        model = Kat
        fields = ['kat_ad','kat_durum']
class KatGüncelle(forms.ModelForm):
    class Meta:
        model = Kat
        fields = ['kat_ad','kat_durum']
class MasaEkle(forms.ModelForm):
    class Meta:
        model = Masa
        fields = ['masa_num', 'masa_kat', 'masa_durum']
class MasaDüzenle(forms.ModelForm):
    class Meta:
        model = Masa
        fields = ['masa_num', 'masa_kat', 'masa_durum']
class UrunEkle(forms.ModelForm):
    # class Meta:
    #     model = Urun=
    def __init__(self, *args, **kwargs):
        firma = kwargs.pop('firma', None)
        super().__init__(*args, **kwargs)
        if firma:
            self.fields['urun_kategori'].queryset = Kategori.objects.filter(kategori_frm=firma)

    class Meta:
        model = Urun
        fields = ['urun_ad', 'urun_kategori', 'urun_fiyat','urun_img']

class KategoriEkle(forms.ModelForm):
    class Meta:
        model = Kategori
        fields = ['kategori_kod','kategori_ad','kategori_durum','kategori_image']


class UpdateRequestForm(forms.ModelForm):
    class Meta:
        model = UpdateRequest
        fields = [
            'company_code',
            'company_name',
            'company_address',
            'company_phone',
            'company_city',
            'company_district',
            'company_title',
            'company_external_ip',
            'company_status',
            'company_agreement_expiry_date',
        ]
        labels = {
            # 'req_company_code': 'Güncelleme Talep Ettiğiniz Firma',
            # 'req_user': 'Talep Eden Kullanıcı',
            'company_code': 'Şirket Kodu',
            'company_name': 'Şirket Adı',
            'company_address': 'Şirket Adresi',
            'company_phone': 'Şirket Telefonu',
            'company_city': 'Şirket Şehir',
            'company_district': 'Şirket İlçe',
            'company_title': 'Şirket Ünvan',
            'company_external_ip': 'Şirket Dış IP',
            'company_status': 'Şirket Durumu',
            'company_agreement_expiry_date': 'Şirket Anlaşma Bitiş Tarihi',
        }
        widgets = {
            # 'req_company_code': forms.TextInput(attrs={'class': 'form-control'}),
            # 'req_user': forms.TextInput(attrs={'class': 'form-control'}),
            'company_code': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'company_name': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'company_address': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'company_phone': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'company_city': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'company_district': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'company_title': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'company_external_ip': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'company_status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'company_agreement_expiry_date': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }