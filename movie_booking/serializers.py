from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from movie_booking.models import Row, Seat, Screen


class RowInfoSerializer(serializers.ModelSerializer):
	numberOfSeats = serializers.IntegerField(source='seat_count')
	aisleSeats = serializers.ListField(child=serializers.IntegerField(), source='aisle_seats')

	class Meta:
		model = Row
		fields = ('numberOfSeats', 'aisleSeats')


class ScreenSerializer(serializers.ModelSerializer):
	seatInfo = serializers.DictField(child=RowInfoSerializer(), write_only=True)

	def validate_seatInfo(self, seatInfo):
		for row_code in seatInfo:
			if len(row_code) > 2:
				raise ValidationError("Row code cannot be greater than 2")
		return seatInfo

	def to_representation(self, instance):
		ret = super().to_representation(instance)
		seatInfo = {}
		for row in instance.rows.all():
			seatInfo[row.code] = RowInfoSerializer(row).data
		ret['seatInfo'] = seatInfo
		return ret

	class Meta:
		model = Screen
		fields = ('name', 'seatInfo')


class ScreenRowSeatsSerializer(serializers.Serializer):
	seats = serializers.DictField(
		child=serializers.ListField(child=serializers.IntegerField())
	)

	def check_seat_status(self, seat, row_code):
		raise NotImplementedError("Should be implemented by child class.")

	def validate_seats(self, seats):
		screen = self.context.get('screen')

		error_messages = []
		for row_code in seats:
			try:
				row = screen.rows.get(code=row_code)
				for seat_code in seats[row_code]:
					try:
						seat = row.seats.get(code=seat_code)
						self.check_seat_status(seat, row_code)
					except ValidationError as e:
						error_messages.append(''.join(e.detail))
					except Seat.DoesNotExist:
						error_messages.append("Seat {0} is not a valid seat of row {1}".format(seat_code, row_code))

			except Row.DoesNotExist:
				error_messages.append("Row {0} is not a valid row of screen {1}".format(row_code, screen.name))

		if error_messages:
			raise ValidationError('\n'.join(error_messages))
		return seats


class BookSeatsSerializer(ScreenRowSeatsSerializer):
	def check_seat_status(self, seat, row_code):
		if seat.booked_on:
			raise ValidationError("Seat {0} of row {1} is already reserved".format(seat.code, row_code))
		return seat


class CancelSeatsSerializer(ScreenRowSeatsSerializer):
	def check_seat_status(self, seat, row_code):
		if not seat.booked_on:
			raise ValidationError("Seat {0} of row {1} is not reserved yet".format(seat.code, row_code))
		return seat
