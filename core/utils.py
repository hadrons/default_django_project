#coding: utf-8
import plivo
from django.conf import settings
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from django.template import Context
from django.core.mail import EmailMessage


from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SendEmail(object):

    def __init__(self, title, message, template, users):
        self.title = title
        self.message = message
        self.template = template
        self.users = users

    def get_content(self):
        content = get_template(self.template).render(Context({'message': self.message}))
        return mark_safe(content)

    def send(self):
        email = EmailMessage(self.title, self.get_content() ,'contato@contato.com', to=self.users)
        email.content_subtype = 'html'
        email.send()

    def run(self):
        self.send()
        # email = SendEmail('Texto', 'Mensagem!', 'template_email.html', [user.email])
        # email.run()

class SendSms(object):

    def __init__(self, message, number):
        self.message = message
        self.number = number

    def send_single_sms(self):

        p = plivo.RestAPI(settings.PLIVO_AUTH_ID, settings.PLIVO_AUTH_TOKEN)

        params = {
            'src': '123123',
            'dst' : self.number,
            'text' : self.message,
            'method': 'POST'
        }

        p.send_message(params)

        # sms = SendSms("Confirme seu cadastro com o código "+ str(user.code) +".", user.cellular)
        # sms.send_single_sms()
