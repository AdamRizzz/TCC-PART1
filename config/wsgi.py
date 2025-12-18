import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

# --- TAMBAHAN: AUTO CREATE SUPERUSER ---
# Kode ini berjalan setiap kali server Railway dinyalakan
try:
    from django.contrib.auth import get_user_model
    User = get_user_model() # Menggunakan core.User (Custom User Anda)
    
    username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL")

    if username and password:
        if not User.objects.filter(username=username).exists():
            print(f"Mencoba membuat superuser otomatis: {username}")
            User.objects.create_superuser(
                username=username, 
                email=email, 
                password=password
            )
            print(">>> SUKSES: Superuser berhasil dibuat otomatis!")
        else:
            print(">>> INFO: Superuser sudah ada, melewati pembuatan.")
            
            # OPSIONAL: Paksa update password user yang sudah ada (jika lupa)
            # user = User.objects.get(username=username)
            # user.set_password(password)
            # user.save()
            # print(">>> INFO: Password superuser di-reset ke nilai ENV.")

except Exception as e:
    print(f">>> ERROR saat auto-create superuser: {e}")
    pass
# ---------------------------------------