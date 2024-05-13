from django.contrib.auth.backends import BaseBackend

class CustomAuthBackend(BaseBackend):
    def has_perm(self, user, perm, obj=None):
        # Kullanıcı yetki kontrolü burada yapılabilir
        # Kendi yetenek mantığınıza göre burayı doldurun
        return False  # Varsayılan olarak yetki yok
