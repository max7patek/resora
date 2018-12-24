from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('ta', views.as_ta, name="as-ta"),
    path('ajax/all-bookables', views.all_bookables, name='all-bookables'),
    path('ajax/book', views.book, name='book'),
    path('ajax/release-booking', views.release_booking, name='release-booking'),
    path('ajax/bookings', views.bookings, name='bookings'),
]
