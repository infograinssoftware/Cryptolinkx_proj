from django.urls import path
from .views import Index, ExchangeView, P2pView, STFView, FundsView, AccountView

urlpatterns = [
    path('', Index.as_view(), name = 'index'),
    path('exchange/', ExchangeView.as_view(), name = 'exchange'),
    path('exchange/<str:pair_name>', ExchangeView.as_view(), name = 'exchange'),
    path('p2p/', P2pView.as_view(), name = 'ptop'),
    path('stf/', STFView.as_view(), name = 'stf'),
    path('funds/', FundsView.as_view(), name = 'funds'),
    path('account/', AccountView.as_view(), name = 'account'),
]
            