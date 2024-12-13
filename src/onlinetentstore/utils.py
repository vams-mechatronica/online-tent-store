from hashids import Hashids
from django.conf import settings
from django.core.mail import send_mail


hashids = Hashids(settings.HASHIDS_SALT, min_length=8)

welcome_user_email = """Dear Customer,
We are thrilled to welcome you to VamsCentral, your one-stop destination for an unparalleled online shopping experience! 🛍️
At VamsCentral, we are committed to making your shopping journey enjoyable, convenient, and rewarding. As a valued member of our growing family, you'll discover a world of benefits:
✨ Wide Selection: Explore a vast collection of products ranging from fashion, electronics, home essentials, and much more. With thousands of options at your fingertips, you're sure to find exactly what you need.
🚚 Speedy Delivery: Our dedicated team ensures swift and secure deliveries right to your doorstep, so you can enjoy your purchases without delay.
🛡️ Secure Shopping: Your security is our top priority. Rest assured that your personal information is protected with state-of-the-art security measures.
💎 Exclusive Offers: Be the first to know about our latest promotions, discounts, and exclusive deals. Don't miss out on incredible savings!
🤝 Dedicated Support: Our friendly and knowledgeable support team is here to assist you with any questions or concerns. We're just a message away.
🌟 Personalized Experience: Tailored recommendations and personalized offers await you, ensuring that your shopping experience is uniquely yours.
To kickstart your journey with us, we're delighted to offer you a special [Discount/Welcome Gift]. Simply use the code [CODE] at checkout to redeem your welcome gift.
Ready to start shopping? Visit www.vamscentral.com today and explore the world of endless possibilities.
Thank you for choosing VamsCentral. We can't wait to accompany you on your shopping adventures!
Happy Shopping!
Warm regards,
Anand S.
Founder, VAMSCentral
"""

user_added = """
"""


def h_encode(id):

    return hashids.encode(id)


def h_decode(h):
    z = hashids.decode(h)
    if z:
        return z[0]


class HashIdConverter:
    regex = '[a-zA-Z0-9]{8,}'

    def to_python(self, value):
        return h_decode(value)

    def to_url(self, value):
        return h_encode(value)

class FloatConverter:
    regex = '[\d\.\d]+'
    # regex = '[0-9]'

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return '{}'.format(value)

class RomanNumeralConverter:
    regex = '[MDCLXVImdclxvi]+'

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return '{}'.format(value)


# def send_welcome_email(maildata):
#     # Send email to admin
#     try:
#         # Send email to customer
#         email_data = UserRegisteredEmails.objects.get(category='New Registration')
#         sender = str(email_data.sender)
#         subject = str(email_data.subject).replace('_customername_',maildata.get('customername'))
#         body = str(email_data.body).replace('_customername_',maildata.get('customername'))
#         to = [maildata.get('useremail')]

#         send_mail(subject,"",sender,to,fail_silently=False, auth_user=None, auth_password=None,connection=None, html_message=body)


#         # send email to admin

#         email_data_admin = UserRegisteredEmails.objects.get(category='New Registration to admin')
#         sender_admin = str(email_data_admin.sender)
#         subject_admin = str(email_data_admin.subject)
#         body_admin = str(email_data_admin.body).replace('_fullname_',maildata.get('customername')).replace('_usermobile_',maildata.get('usermobile')).replace('_useremail_',maildata.get('useremail'))
#         to_admin = sender_admin

#         send_mail(subject_admin,"",sender_admin,to_admin,fail_silently=False, auth_user=None, auth_password=None,connection=None, html_message=body_admin)




#         return True
#     except:
#         return False


# @shared_task
# def send_email_task(maildata):
#     send_welcome_email(maildata)