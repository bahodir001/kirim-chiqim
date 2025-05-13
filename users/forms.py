from django import forms

class VerifyForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        label='Tasdiqlash kodingiz:',
        widget=forms.TextInput(attrs={
            'placeholder': '123456',
            'class': 'form-input'
        })
    )
    password = forms.CharField(
        label='Parol:',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Yangi parol',
            'class': 'form-input'
        })
    )
    first_name = forms.CharField(
        label='Ism:',
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ismingiz',
            'class': 'form-input'
        })
    )
    last_name = forms.CharField(
        label='Familiya:',
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Familiyangiz',
            'class': 'form-input'
        })
    )
    phone_number = forms.CharField(
        label='Telefon:',
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': '998901234567',
            'class': 'form-input'
        })
    )
    card_number = forms.CharField(
        label='Karta raqami:',
        max_length=30,
        widget=forms.TextInput(attrs={
            'placeholder': '8600 xxxx xxxx xxxx',
            'class': 'form-input'
        })
    )

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if not code.isdigit() or len(code) != 6:
            raise forms.ValidationError("Faqat 6 xonali raqam kiriting!")
        return code
