from django.conf.urls import url

from movie_booking import views

urlpatterns = [
	url(r'^$', views.ScreenListView.as_view(), name='screen-list'),
	url(r'^(?P<screen_name>\w+)/$', views.ScreenDetailView.as_view(), name='screen-detail'),
	url(r'^(?P<screen_name>\w+)/reserve/$', views.BookSeatView.as_view(), name='book-seat-view'),
	url(r'^(?P<screen_name>\w+)/cancel/$', views.CancelSeatView.as_view(), name='cancel-seat-view'),
	url(r'^(?P<screen_name>\w+)/seats/$', views.ScreenSeatsView.as_view(), name='screen-seats-view'),
]