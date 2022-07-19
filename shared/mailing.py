from shared.email_utility import SendEmail


def email_verify_request(to_email, verify_link):
    """
    Function to send email for verify email.
    """

    context = {
        'verify_link': verify_link
    }

    msg = SendEmail()
    msg.send(
        [to_email],
        'Verify Email',
        'emails/verify_email_request.html',
        context
    )


def password_reset_request(to_email, code):
    """
    Function to send email for password reset request.
    """

    context = {
        'code': code
    }

    msg = SendEmail()
    msg.send(
        [to_email],
        'Reset Password',
        'emails/password_reset_request.html',
        context
    )


def referral_request(to_email):
    """
    Function to send email for referrals request.
    """

    context = {
        'link': 'https://www.technoarchsoftwares.com/goals/'
    }

    msg = SendEmail()
    msg.send(
        to_email,
        'Referral request received',
        'emails/referral_request.html',
        context
    )


def contact_us(to_email, message, email, name):
    """
    Function to send email for referrals request.
    """

    context = {
        'message': message,
        'name': name,
        'email': email
    }

    msg = SendEmail()
    msg.send(
        to_email,
        '{} Contacted You'.format(name),
        'emails/contact_us.html',
        context
    )