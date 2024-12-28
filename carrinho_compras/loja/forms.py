from django import forms

class PesquisaForm(forms.Form):
    termo = forms.CharField(label='Pesquisar', max_length=100)
