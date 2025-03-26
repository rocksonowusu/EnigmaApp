from django.urls import path
from .views import EnigmaEncryptView,EnigmaDecryptView,EncryptionHistoryView

urlpatterns = [
    path('encrypt/', EnigmaEncryptView.as_view(), name='encrypt'),
    path('decrypt/', EnigmaDecryptView.as_view(), name='decrypt'),
    path('history/', EncryptionHistoryView.as_view(), name='history'),
]
