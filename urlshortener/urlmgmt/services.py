import random, string, json
from .models import URL
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from urlmgmt.serializers import ShortURLSerializer
from django.utils import timezone
from django.conf import settings
import shortuuid


def get_short_code():
    """"
        return random short code if not exist in URL model
    """
    length = 6
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    # if the randomly generated short_id is used then generate next
    while True:
        short_id = ''.join(random.choice(char) for _ in range(length))
        try:
            url_obj = URL.objects.get(short_url=short_id)
        except:
            return short_id


class ShortUrlAPIView(APIView):

    def get(self, request):
        url_objects = URL.objects.all()
        serializer = ShortURLSerializer(url_objects, many=True)
        return Response(serializer.data)


    def post(self, request):
        try:
            url = request.POST.get('url')
        except Exception as ex:
            return JsonResponse({'error': ex}, status=400)

        try:
            url_object = URL.objects.filter(http_url=url)
            if url_object:
                url_object = URL.objects.get(http_url=url)
                print("Existing URL object found", url_object.created, type(url_object.created))
                if is_valid_url(url_object.created):
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

        except Exception as ex:
            return JsonResponse({'error': ex}, status=500)

        serializer = ShortURLSerializer(url_object)
        return Response(serializer.data)
    

def is_valid_url(created):
    print("Created: ", str(created))
    print("Current Time: ", timezone.now())
    diff = timezone.now() - created
    print("Difference:", diff)
    print("Days:", diff.days)
    print("Seconds:", diff.seconds)
    if diff.days <= settings.URL_EXPIRY_DAYS:
        return True
    else:
        return False
