from django import forms

from mailings.models import Message, Client, MailingSettings


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class MailingSettingsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingSettings
        fields = '__all__'


class MailingSettingsManagerForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingSettings
        fields = ('status',)





