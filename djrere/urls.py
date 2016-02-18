from django.conf.urls import include, url

from .frontpage import views as frontpage_views

urlpatterns = [
    url(r'^graphql/', include('djrere.graphql.urls', namespace='graphql')),
    url(r'^frontpage/', include('djrere.frontpage.urls')),
    url(r'^blog/', include('djrere.blog.urls')),
    url(r'^$', frontpage_views.home)
]
