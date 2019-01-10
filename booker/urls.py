from django.urls import path

from . import views
from . import ajax

urlpatterns = [
    path('', views.landing, name='landing'),
    path('bookables', views.bookables, name='bookables'),
    path('booking', views.booking, name='booking'),
    path('ta', views.as_ta, name="as-ta"),
    path('ta/manual-pull', views.manual_pull, name="manual-pull"),
    path('ta/roster-upload', views.roster_upload, name="roster-upload"),
    path('ajax/all-bookables', ajax.all_bookables, name='all-bookables'),
    path('ajax/book', ajax.book, name='book'),
    path('ajax/release-booking', ajax.release_booking, name='release-booking'),
    path('ajax/bookings', ajax.bookings, name='bookings'),
    path('ajax/booked', ajax.booked, name='booked'),
]
