from django import forms
from .models import Denuncia


class DenunciaForm(forms.ModelForm):

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Seu e-mail'
        })
    )

    class Meta:
        model = Denuncia
        fields = [
            'tipo',
            'empresa',
            'descricao',
            'anonima',
            'nome',
            'email',
        ]

        widgets = {
            'descricao': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Descreva detalhadamente o ocorrido...'
            }),
            'empresa': forms.TextInput(attrs={
                'placeholder': 'Nome da empresa envolvida'
            }),
            'nome': forms.TextInput(attrs={
                'placeholder': 'Seu nome'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        anonima = cleaned_data.get('anonima')
        nome = cleaned_data.get('nome')
        email = cleaned_data.get('email')

        if not anonima:
            if not nome:
                self.add_error('nome', 'Informe seu nome.')

            if not email:
                self.add_error('email', 'Informe seu e-mail.')

        else:
            cleaned_data['nome'] = ''
            cleaned_data['email'] = ''

        return cleaned_data