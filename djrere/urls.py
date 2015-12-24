from django.conf.urls import include, url

urlpatterns = [
    url(r'^frontpage/', include('djrere.frontpage.urls')),
    url(r'^$', 'djrere.frontpage.views.home')
]
