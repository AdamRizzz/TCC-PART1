from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Skripsi
from .models import ChatMessage

class SignUpForm(UserCreationForm):
    ROLE_CHOICES = (
        ('student', 'Mahasiswa'),
        ('lecturer', 'Dosen'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('role',)

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')
        if role == 'student':
            user.is_student = True
        elif role == 'lecturer':
            user.is_lecturer = True
        if commit:
            user.save()
        return user

class SkripsiForm(forms.ModelForm):
    class Meta:
        model = Skripsi
        fields = ['judul', 'deskripsi', 'lecturer']
        labels = {
            'lecturer': 'Pilih Dosen Pembimbing'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter dropdown hanya menampilkan user yang merupakan Dosen
        self.fields['lecturer'].queryset = User.objects.filter(is_lecturer=True)
        # Styling Bootstrap
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            
class MessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Tulis pesan bimbingan di sini...'
            }),
        }