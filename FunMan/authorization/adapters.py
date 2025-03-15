from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_login_redirect_url(self, request):
        return '/authorization/change-password/'
    
    