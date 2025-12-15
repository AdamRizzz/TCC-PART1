from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, SkripsiForm
from .models import Skripsi
from .forms import SignUpForm, SkripsiForm, MessageForm # Tambahkan MessageForm
from .models import Skripsi, ChatMessage # Tambahkan ChatMessage

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    # Logika Dashboard Mahasiswa
    if request.user.is_student:
        try:
            skripsi = Skripsi.objects.get(student=request.user)
            return render(request, 'dashboard_student.html', {'skripsi': skripsi})
        except Skripsi.DoesNotExist:
            # Jika belum mengajukan, tampilkan form
            if request.method == 'POST':
                form = SkripsiForm(request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.student = request.user
                    obj.save()
                    return redirect('dashboard')
            else:
                form = SkripsiForm()
            return render(request, 'dashboard_student.html', {'form': form, 'skripsi': None})

    # Logika Dashboard Dosen
    elif request.user.is_lecturer:
        # Lihat semua request yang masuk ke dosen ini
        requests = Skripsi.objects.filter(lecturer=request.user).order_by('-created_at')
        return render(request, 'dashboard_lecturer.html', {'requests': requests})
    
    return render(request, 'home.html') # Fallback

@login_required
def update_status(request, skripsi_id, action):
    # Hanya dosen yang bisa akses
    if not request.user.is_lecturer:
        return redirect('dashboard')
        
    skripsi = get_object_or_404(Skripsi, id=skripsi_id, lecturer=request.user)
    
    if action == 'approve':
        skripsi.status = 'approved'
    elif action == 'reject':
        skripsi.status = 'rejected'
    
    skripsi.save()
    return redirect('dashboard')

@login_required
def chat_room(request, skripsi_id):
    # Ambil data skripsi
    skripsi = get_object_or_404(Skripsi, id=skripsi_id)

    # KEAMANAN: Pastikan yang mengakses hanya Mahasiswa ybs atau Dosen Pembimbingnya
    if request.user != skripsi.student and request.user != skripsi.lecturer:
        return redirect('dashboard')

    # Proses Input Pesan Baru
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.skripsi = skripsi
            chat.sender = request.user
            chat.save()
            return redirect('chat_room', skripsi_id=skripsi.id)
    else:
        form = MessageForm()

    # Ambil semua pesan urut dari yang terlama ke terbaru
    messages = skripsi.messages.all().order_by('created_at')

    return render(request, 'chat_room.html', {
        'skripsi': skripsi,
        'messages': messages,
        'form': form
    })