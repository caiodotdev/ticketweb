from django.urls import path, include

from app import conf
from app.urls_api import api_urlpatterns
from app.views.pack import DeleteAllPack, get_packs
from app.views.ticket import run_thread, DeleteAll

urlpatterns = []

urlpatterns += [
    path('', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls'))
]

from app.views import ticket

urlpatterns += [
    # ticket
    path(
        'ticket/',
        ticket.List.as_view(),
        name=conf.TICKET_LIST_URL_NAME
    ),
    path(
        'ticket/create/',
        ticket.Create.as_view(),
        name=conf.TICKET_CREATE_URL_NAME
    ),
    path(
        'ticket/<int:pk>/',
        ticket.Detail.as_view(),
        name=conf.TICKET_DETAIL_URL_NAME
    ),
    path(
        'ticket/<int:pk>/update/',
        ticket.Update.as_view(),
        name=conf.TICKET_UPDATE_URL_NAME
    ),
    path(
        'ticket/<int:pk>/delete/',
        ticket.Delete.as_view(),
        name=conf.TICKET_DELETE_URL_NAME
    ),
    path(
        'ticket/list/json/',
        ticket.TicketListJson.as_view(),
        name=conf.TICKET_LIST_JSON_URL_NAME
    ),
    path('run-thread', run_thread, name='run_thread'),
    path('delete-all', DeleteAll.as_view(), name='delete_all')
]


from app.views import pack

urlpatterns += [
    # pack
    path(
        '',
        pack.List.as_view(),
        name=conf.PACK_LIST_URL_NAME
    ),
    path(
        'pack/create/',
        pack.Create.as_view(),
        name=conf.PACK_CREATE_URL_NAME
    ),
    path(
        'pack/<int:pk>/',
        pack.Detail.as_view(),
        name=conf.PACK_DETAIL_URL_NAME
    ),
    path(
        'pack/<int:pk>/update/',
        pack.Update.as_view(),
        name=conf.PACK_UPDATE_URL_NAME
    ),
    path(
        'pack/<int:pk>/delete/',
        pack.Delete.as_view(),
        name=conf.PACK_DELETE_URL_NAME
    ),
    path(
        'pack/list/json/',
        pack.PackListJson.as_view(),
        name=conf.PACK_LIST_JSON_URL_NAME
    ),
    path('get-packs', get_packs, name='get_packs'),
    path('delete-all-packs', DeleteAllPack.as_view(), name='delete_all_packs')
]
from app.views import image_pack

urlpatterns += [
    # image_pack
    path(
        'imagepack/',
        image_pack.List.as_view(),
        name=conf.IMAGEPACK_LIST_URL_NAME
    ),
    path(
        'imagepack/create/',
        image_pack.Create.as_view(),
        name=conf.IMAGEPACK_CREATE_URL_NAME
    ),
    path(
        'imagepack/<int:pk>/',
        image_pack.Detail.as_view(),
        name=conf.IMAGEPACK_DETAIL_URL_NAME
    ),
    path(
        'imagepack/<int:pk>/update/',
        image_pack.Update.as_view(),
        name=conf.IMAGEPACK_UPDATE_URL_NAME
    ),
    path(
        'imagepack/<int:pk>/delete/',
        image_pack.Delete.as_view(),
        name=conf.IMAGEPACK_DELETE_URL_NAME
    ),
    path(
        'imagepack/list/json/',
        image_pack.ImagePackListJson.as_view(),
        name=conf.IMAGEPACK_LIST_JSON_URL_NAME
    )
]

urlpatterns += api_urlpatterns
from app.views import thread
urlpatterns += [
    # thread
    path(
        'thread/',
        thread.List.as_view(),
        name=conf.THREAD_LIST_URL_NAME
    ),
    path(
        'thread/create/',
        thread.Create.as_view(),
        name=conf.THREAD_CREATE_URL_NAME
    ),
    path(
        'thread/<int:pk>/',
        thread.Detail.as_view(),
        name=conf.THREAD_DETAIL_URL_NAME
    ),
    path(
        'thread/<int:pk>/update/',
        thread.Update.as_view(),
        name=conf.THREAD_UPDATE_URL_NAME
    ),
    path(
        'thread/<int:pk>/delete/',
        thread.Delete.as_view(),
        name=conf.THREAD_DELETE_URL_NAME
    ),
    path(
        'thread/list/json/',
        thread.ThreadListJson.as_view(),
        name=conf.THREAD_LIST_JSON_URL_NAME
    )
]

