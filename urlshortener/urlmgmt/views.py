from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import URL
from . import services
import shortuuid
from django.conf import settings


def index(request):
    context = {}
    return render(request, 'urlmgmt/index.html', context)


def shorten_url(request):
    url = request.POST.get("httpurl", '')
    context = {}
    if not (url == ''):
        try:
            url_object = URL.objects.filter(http_url=url)
            if url_object:
                url_object = URL.objects.get(http_url=url)
                print("Existing URL object found", url_object.created, type(url_object.created))
                if services.is_valid_url(url_object.created):
                    print("URL object not expired")
                    pass
                else:
                    print("Object is expired, extending expiry time")
                    import datetime
                    url_object.created = datetime.datetime.now()
                    url_object.save()
            else:
                print("Create new URL object")
                url_object = URL.objects.create(
                    short_url=settings.SITE_URL + "/" + shortuuid.ShortUUID().random(length=6),
                    http_url=url
                )

            context['short_url'] = url_object.short_url
            context['http_url'] = url_object.http_url
            print("context:", context)

        except Exception as ex:
            context['error'] = ex
    else:
        context['error'] = "URL input is not supplied"
    return render(request, 'urlmgmt/index.html', context)


def redirect_url(request, url=None):
    try:
        print("url : ", url)
        short_url = settings.SITE_URL + "/" + url
        print("Short url : ", short_url)
        url_object = URL.objects.get(short_url=short_url)
        print("http url:", url_object.http_url)

    except Exception as e:
        context = {'error': e}
        return render(request, 'urlmgmt/index.html', context)

    if services.is_valid_url(url_object.created):

        url_object.visitor_count += 1
        url_object.save()
        return redirect(url_object.http_url)
    else:
        context = {'error': 'Short URL does not valid'}
        return render(request, 'urlmgmt/index.html', context)
