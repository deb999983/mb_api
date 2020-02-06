import coreapi
from django.db import transaction
from django.utils import timezone
from django_filters.filterset import filterset_factory
from rest_framework.exceptions import ValidationError
from rest_framework.generics import UpdateAPIView, RetrieveAPIView, ListCreateAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema

from movie_booking.models import Seat, Screen
from movie_booking.serializers import BookSeatsSerializer, ScreenSerializer, CancelSeatsSerializer, \
	ScreenRowSeatsSerializer


class ModelViewMixin:
	model_class = None

	def get_queryset(self):
		if not self.model_class:
			raise NotImplementedError("Subclass must provide a model class.")
		return self.model_class.objects.all()


class ScreenViewMixin:
	model_class = Screen
	lookup_url_kwarg = 'screen_name'
	lookup_field = 'name'

	def get_serializer_context(self):
		if not self.kwargs:
			return

		context = super().get_serializer_context()
		context['screen'] = self.get_object()
		return context

	def get_response_serializer_class(self):
		return self.serializer_class

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data, partial=False)
		serializer.is_valid(raise_exception=True)
		screen = self.perform_create(serializer)
		return Response(self.get_response_serializer_class()(screen).data)


class BaseBookingView(ScreenViewMixin, ModelViewMixin, CreateAPIView):

	def get_response_serializer_class(self):
		return ScreenSerializer

	def get_reservation_kwargs(self):
		raise NotImplementedError("Should be implemented by subclass")

	def perform_create(self, serializer):
		row_seat_info = serializer.validated_data['seats']
		screen = serializer.context['screen']

		with transaction.atomic():
			for row_code in row_seat_info:
				Seat.objects.filter(
					code__in=row_seat_info[row_code], row__code=row_code, row__screen=screen
				).update(**self.get_reservation_kwargs())
		return screen


class BookSeatView(BaseBookingView):
	serializer_class = BookSeatsSerializer
	model_class = Screen

	def get_reservation_kwargs(self):
		return {"booked_on": timezone.now()}


class CancelSeatView(BaseBookingView):
	serializer_class = CancelSeatsSerializer

	def get_reservation_kwargs(self):
		return {"booked_on": None}


class ScreenListView(ScreenViewMixin, ModelViewMixin, ListCreateAPIView):
	serializer_class = ScreenSerializer
	filter_class = filterset_factory(Screen, fields=('name',))
	ordering = 'name'

	def perform_create(self, serializer):
		return Screen.create(serializer.validated_data)


class ScreenDetailView(ScreenViewMixin, ModelViewMixin, RetrieveAPIView):
	serializer_class = ScreenSerializer


class ScreenSeatsView(ScreenViewMixin, ModelViewMixin, RetrieveAPIView):
	serializer_class = ScreenRowSeatsSerializer

	class Schema(AutoSchema):
		def get_serializer_fields(self, path, method):
			return [
				coreapi.Field(name='status', location='query'),
			]

	schema = Schema()

	def retrieve(self, request, *args, **kwargs):
		screen = self.get_object()
		serializer = self.get_serializer(screen)

		status = self.request.query_params.get('status')
		if not status:
			return Response(self.serializer_class({"seats": screen.get_seats()}).data)

		if status == 'reserved':
			return Response(self.serializer_class({"seats": screen.get_seats(booked_on__isnull=False)}).data)
		elif status == 'unreserved':
			return Response(self.serializer_class({"seats": screen.get_seats(booked_on__isnull=True)}).data)
		else:
			raise ValidationError("Invalid status, status can be either ot these two options [{0}, {1}]".format(
				'reserved', 'unreserved')
			)
