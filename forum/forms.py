from django import forms
from .models import *
from django.utils import timezone
from django.forms import ModelForm, Textarea, TextInput
from ckeditor.widgets import CKEditorWidget
from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class TopicoForm(ModelForm):
    class Meta:
        model = Topico
        fields = '__all__'
        exclude = ['data_postagem']
        widgets = {
            'texto': CKEditorWidget()
        }
        
class RespostaForm(ModelForm):
    class Meta:
        model = Resposta
        fields = '__all__'
        exclude = ['data_postagem']
        widgets = {
            'texto': CKEditorWidget()
        }

# class DiscussaoForm(ModelForm):
#     class Meta:
#         model = Discussao
#         exclude = ['__all__']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'username', 'password', 'first_name', 'last_name', 'email']

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        if avatar:
            try:
                w, h = get_image_dimensions(avatar)

                #verifica a resolucao da imagem
                max_width = 800
                max_height = 600
                if w > max_width or h > max_height:
                    
                    raise ValidationError(_('A imagem deve ser no máximo 800x600'), code='invalid')

                #valida o formato da imagem
                main, sub = avatar.content_type.split('/')
                if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                    raise ValidationError(_('A imagem deve ser JPEG, GIF ou PNG.'), code='invalid')

                #valida o tamanho da imagem
                if len(avatar) > (40 * 1024):
                    raise ValidationError(_('A imagem não pode ser maior que 40k.'), code='invalid')

            except AttributeError:
                pass

            return avatar

    def clean_username(self):
        username = self.cleaned_data['username']
        #verifica se o usuario já existe
        if User.objects.filter(username=username).exists():
            raise ValidationError(_("Nome de usuário em uso, escolha outro!"), code='invalid')

        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        #verifica se o email já foi usado
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("Este email já está associado à uma conta."), code='invalid')
