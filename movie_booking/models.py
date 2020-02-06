from django.db import models, transaction


class Screen(models.Model):
	name = models.CharField(max_length=255, unique=True)

	@classmethod
	def create(cls, screen_info):
		screen_name = screen_info['name']
		seat_info = screen_info['seatInfo']

		with transaction.atomic():
			screen = cls.objects.create(name=screen_name)
			for row_code in seat_info:
				row = screen.add_row(row_code)
				row.add_seats(count=seat_info[row_code]['seat_count'], aisle_seats=seat_info[row_code]['aisle_seats'])
			return screen

	def add_row(self, row_code):
		return Row.objects.create(screen=self, code=row_code)

	@property
	def row_count(self):
		return self.rows.all().count()

	@property
	def seat_count(self):
		return Seat.objects.all(row__screen=self)

	def get_seats(self, **kwargs):
		seats = Seat.objects.select_related('row').filter(row__screen=self, **kwargs)

		seat_info = {}
		for seat in seats:
			seat_info[seat.row.code] = seat_info.get(seat.row.code) or []
			seat_info[seat.row.code].append(seat.code)
		return seat_info


class Row(models.Model):
	code = models.CharField(max_length=2)
	screen = models.ForeignKey(Screen, related_name='rows', on_delete=models.CASCADE)

	class Meta:
		unique_together = ('code', 'screen')

	@property
	def seat_count(self):
		return self.seats.all().count()

	@property
	def booked_seats(self):
		return self.seats.filter(booked_on__isnull=False).values_list('code', flat=True)

	@property
	def available_seats(self):
		return self.seats.filter(booked_on__isnull=True).values_list('code', flat=True)

	@property
	def aisle_seats(self):
		return self.seats.filter(is_aisle=True).values_list('code', flat=True)

	def add_seats(self, count, aisle_seats):
		aisle_seats = aisle_seats or []
		for i in range(1, count + 1):
			Seat.objects.create(row=self, code=i, is_aisle=i in aisle_seats)



class Seat(models.Model):
	code = models.IntegerField()
	row = models.ForeignKey(Row, related_name='seats', on_delete=models.CASCADE)
	booked_on = models.DateTimeField(null=True)
	is_aisle = models.BooleanField(default=False)

	class Meta:
		unique_together = ('row', 'code')


def init_data():
	for i in range(0, 10):
		screen = Screen.objects.create(name='inox' + str(i))
		screen.add_rows(['A', 'B', 'C', 'D', 'E', 'F'])
		for row in screen.rows.all():
			row.add_seats(12, aisle_codes=[4, 5, 8, 9])