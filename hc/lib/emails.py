from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send(name, to, ctx):
    ctx["SITE_ROOT"] = settings.SITE_ROOT
    html = render_to_string('emails/' + str(name) + '-body-html.html', ctx)
    subject = render_to_string('emails/' + str(name) + '-subject.html', ctx)
    text = render_to_string('emails/' + str(name) + '-body-text.html', ctx)

    send_mail(
        subject=subject.strip(),
        message=text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[to],
        html_message=html,
        fail_silently=False,
    )


def login(to, ctx):
    send("login", to, ctx)


def set_password(to, ctx):
    send("set-password", to, ctx)


def alert(to, ctx):
    send("alert", to, ctx)


def verify_email(to, ctx):
    send("verify-email", to, ctx)


def report(to, ctx):
    send("report", to, ctx)
