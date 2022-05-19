from rest_framework.routers import DefaultRouter

from app import (
    viewsets
)

api_urlpatterns = []

ticket_router = DefaultRouter()

ticket_router.register(
    r'^api/ticket',
    viewsets.TicketViewSet,
    basename="ticket"
)

api_urlpatterns += ticket_router.urls
pack_router = DefaultRouter()

pack_router.register(
    r'^api/pack',
    viewsets.PackViewSet,
    basename="pack"
)

api_urlpatterns += pack_router.urls
imagepack_router = DefaultRouter()

imagepack_router.register(
    r'^api/imagepack',
    viewsets.ImagePackViewSet,
    basename="imagepack"
)

api_urlpatterns += imagepack_router.urls
thread_router = DefaultRouter()

thread_router.register(
    r'^api/thread',
    viewsets.ThreadViewSet,
    basename="thread"
)

api_urlpatterns += thread_router.urls
