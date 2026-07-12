from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.contrib import admin
from django.http import HttpResponse
from django.urls import re_path
from django.views.static import serve

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from core.sitemaps import WagtailPageSitemap
from search import views as search_views
from schedule import views as schedule_views

sitemaps = {
    "pages": WagtailPageSitemap,
}

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("schedule/", schedule_views.schedule_view, name="schedule"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path(
        "robots.txt",
        lambda request: HttpResponse(
            f"User-agent: *\nDisallow: /admin/\nDisallow: /django-admin/\nSitemap: https://{request.get_host()}/sitemap.xml\n",
            content_type="text/plain",
        ),
        name="robots_txt",
    ),
]

urlpatterns += [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()

    try:
        import debug_toolbar  # noqa: F401
        urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
    except ImportError:
        pass