from django.conf.urls import include, url

urlpatterns = [
    url(r'^graphql/', include('djrere.graphql.urls')),
    url(r'^frontpage/', include('djrere.frontpage.urls')),
    url(r'^$', 'djrere.frontpage.views.home')
]
