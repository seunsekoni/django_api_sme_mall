from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail




class Utils():
    @staticmethod
    def send_the_email(data):
        # send mail to new user

        # msg_html = render_to_string('authentication/email/welcome_mail.html', {'user': user})

        # send_mail(
        #     'Welcome To The SME MALL',
        #     '',
        #     'testing@sender',
        #     [user.email],
        #     html_message=msg_html,
        # )
        send_mail(
            data['email_subject'],
            '',
            getattr(settings, 'MAIL_FROM_ADDRESS'),
            [data['user_email']],
            html_message=data['msg_html'],
        )

    