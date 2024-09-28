class LagStop:
	def __init__(self, start_stop, end_stop):
		self.start_stop = self.format_stop(start_stop)
		self.end_stop = self.format_stop(end_stop)

	def format_stop(self, stop):
		if stop[13] != 'bobtail':
			if stop[21] == 'ready for pickup' or stop[21] == 'loading in progress...' or stop[21] == 'Live':
				formatted_stop = self.create_formatted_stop(stop, 27, 25)
			elif stop[21] == '--':
				formatted_stop = self.create_formatted_stop(stop, 25, 25)
			else:
				formatted_stop = self.create_formatted_stop(stop, 26, 26)
		else:
			formatted_stop = self.create_formatted_stop(stop, 27, 27)
		return formatted_stop

	def create_formatted_stop(self, stop, schedule_idx, address_idx):
		return {
			'Schedule': stop[schedule_idx],
			'Address': f"{stop[2]}\n{stop[4]}\n{stop[6]}"
		}

	def __str__(self):
		return f"""
📍{self.start_stop['Address']}
⏰{self.start_stop['Schedule']}

📍{self.end_stop['Address']}
⏰{self.end_stop['Schedule']}
——————————————"""


class Trip:
	def __init__(self, text):
		self.assign_driver_index = text.index('Assign driver')
		self.text = text
		self.stops = []
		self.sample = []
		self.trip = []
		self.update = []
		self.lags = []
		self.message = ''
		self.parse_text()

	def parse_text(self):
		if not self.text:
			print("name list is empty")
			return

		stops = [n for i, n in zip(self.text, range(len(self.text))) if len(i) == 1]
		if stops:
			for i in range(len(stops) - 1):
				self.sample.append(self.text[stops[i]:stops[i + 1]])
			self.sample.append(self.text[stops[-1]:])

		self.update, self.trip = self.sample[:3], self.sample[3:]

		max_stops = max(int(i[0]) for i in self.trip)
		for i in range(max_stops):
			self.lags.append(self.trip[2 + i * 4: 4 + i * 4])

	def build_message(self):
		for lag in self.lags[:-1]:
			lag_stop = LagStop(lag[0], lag[1])
			self.message += str(lag_stop)

		self.message = f'Load ID: {self.text[1]}\n——————————————' + self.message
		self.message += f'\nMiles: {self.text[self.assign_driver_index-13]}\nRate: {self.text[self.assign_driver_index-4]} \n{self.text[self.assign_driver_index-2]}'
		return self.message


if __name__ == '__main__':
	text = ("""
T-1117NS9CG

Spot

Starts in

4h 6m

1

LGB7 Rialto, California 92376

Sat, Sep 28, 09:15 PDT

3

MIT2 SHAFTER, California 93263

Sun, Sep 29, 12:11 PDT
653 mi

1d 3h
53' Trailer

P

Drop

$1 195,55

$1.83/mi

Assign driver
O. Demediuk
1141R4FJH

1

LGB7

2

OAK5

404 mi

10h 1m

53' Trailer

Drop

$153,42

Assign driver
O. Demediuk
Stop

Equipment

Arrival

Departure

1

LGB7

1660 N. Linden Avenue

Rialto, California 92376

Tractor ID

--


53' Trailer

Trailer ID

AZNG GV2502657

Preloaded

--

Sch.

28 Sep, 09:15 PDT

Report delay

--

Sch.

28 Sep, 10:00 PDT

Report delay

Pick-up instructions

2

OAK5

38811 Cherry St

NEWARK, CALIFORNIA 94560

Tractor ID

--


53' Trailer

Trailer ID

GV2502657

Drop

--

Sch.

28 Sep, 18:45 PDT

Report delay

--

Sch.

28 Sep, 19:16 PDT

Drop-off instructions

113BVM9PB

2

OAK5

3

MIT2

250 mi

18h 26m

53' Trailer

Drop

$94,83

Assign driver
O. Demediuk
Stop

Equipment

Arrival

Departure

2

OAK5

38811 Cherry St

NEWARK, CALIFORNIA 94560

Tractor ID

--


53' Trailer

Trailer ID

--


Preloaded

--

Sch.

28 Sep, 18:45 PDT

Report delay

--

Sch.

28 Sep, 19:16 PDT

Report delay

Pick-up instructions

3

MIT2

5408 Express Avenue

SHAFTER, California 93263

Tractor ID

--


53' Trailer

Trailer ID

--


Drop

--

Sch.

29 Sep, 12:11 PDT

Report delay

--

Sch.

29 Sep, 13:11 PDT
""").split(sep='\n')
	trip = Trip(text)
	trip.build_message()
	print(trip.message)
	# print(text.index('558 mi'))
	# print(text.index('Assign driver'))