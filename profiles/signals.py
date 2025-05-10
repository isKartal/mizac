from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import social_account_added, social_account_updated

@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    """
    Kullanıcı ilk kez kayıt olduğunda tetiklenir
    """
    # Burada kullanıcı için başlangıç ayarları yapabilirsiniz
    pass

@receiver(social_account_added)
def social_account_added_(request, sociallogin, **kwargs):
    """
    Sosyal hesap eklendiğinde tetiklenir
    """
    pass