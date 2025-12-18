from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # Import model User custom Anda

# 1. Daftarkan Custom User agar muncul di Admin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_student', 'is_lecturer')}), # Tambahkan field role
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_student', 'is_lecturer')}),
    )
    list_display = ['username', 'email', 'is_student', 'is_lecturer', 'is_staff']

# 2. Daftarkan Model Lainnya (Contoh)
# Hapus tanda pagar (#) di bawah jika modelnya sudah ada di models.py Anda
# from .models import Mahasiswa, Dosen, PengajuanJudul

# admin.site.register(Mahasiswa)
# admin.site.register(Dosen)
# admin.site.register(PengajuanJudul)
