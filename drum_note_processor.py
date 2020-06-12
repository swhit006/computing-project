import midi
PPQ = 480 # Pulse per quarter note
event_per_bar = 16 # to quantise.
min_ppq = PPQ / (event_per_bar/4)

drum_conversion = {
					37:38, 40:38, # 37: side stick, 40: snare rim/electric snare - 38: acou snare
					58:43, # 58: floor tom (rim)/vibraslap - 43: high floor tom 
					47:45, # 47: tom 2 (rim)/low-mid tom - 45: low tom 
					50:48, # 50: tom 1 (rim)/high tom - 48: hi mid tom
					44:42, 22:42, #  44: pedal HH, 22: closed HH (edge) - 42: closed HH
					57:49, 55:49, 52:49, # 57: crash 2 (bow)/crash 2, 55: crash 1 (edge)/splash, 52: crash 2 (edge)/china cymbal - 49: Crash cymbal
					59:51, 53:51, # 59: ride (edge)/ride 2, 53: ride bell - 51: ride cymbal
				}

				# k, sn,cHH,oHH,HFtom,ltm,HMtm,Rde,Crash
allowed_pitch = [36, 38, 42, 46, 43, 45, 48, 51, 49]

pitch_to_midipitch = {36:midi.C_3,  # for logic 'SoCal' drum mapping
						38:midi.D_3, 
						39:midi.Eb_3,
						41:midi.F_3,
						42:midi.Gb_3,
                        43:midi.G_3,
						45:midi.A_3,
						46:midi.Bb_3,
						48:midi.C_4,
						49:midi.Db_4,
						51:midi.Eb_4
						}

class Note:
	def __init__(self, pitch, c_tick):
		self.pitch = pitch
		self.c_tick = c_tick # cumulated_tick of a midi note

	def add_index(self, idx):
		'''index --> 16-th note-based index starts from 0'''
		self.idx = idx

class Note_List():
	def __init__(self):
		''''''
		self.notes = []
		self.quantised = False
		self.max_idx = None

	def add_note(self, note):
		'''note: instance of Note class'''
		self.notes.append(note)

	def quantise(self, minimum_ppq):
		'''
		e.g. if minimum_ppq=120, quantise by 16-th note.
		
		'''
		if not self.quantised:
			for note in self.notes:
				note.c_tick = (int((note.c_tick+minimum_ppq/2)/minimum_ppq))* minimum_ppq # quantise
				note.add_index(int(note.c_tick/minimum_ppq))

			self.max_idx = note.idx
			if (self.max_idx + 1) % event_per_bar != 0:
				self.max_idx += event_per_bar - ((self.max_idx + 1) % event_per_bar) # make sure it has a FULL bar at the end.
			self.quantised = True

		return

	def simplify_drums(self):

		for note in self.notes:
			if note.pitch in drum_conversion: # ignore those not included in the key
				note.pitch = drum_conversion[note.pitch]
		
		self.notes = [note for note in self.notes if note.pitch in allowed_pitch]	
				
		return
	
	def return_as_text(self):
		''''''
		length = self.max_idx + 1 # of events in the track.
		event_track = []
		for note_idx in range(length):
			event_track.append(['0']*len(allowed_pitch))
			
		num_bars = length/event_per_bar

		for note in self.notes:
			pitch_here = note.pitch
			note_add_pitch_index = allowed_pitch.index(pitch_here) # 0-8
			event_track[note.idx][note_add_pitch_index] = '1'
			
		event_text_temp = ['0b'+''.join(e) for e in event_track] # encoding to binary
		
		event_text = []

		for bar_idx in range(int(num_bars)):
			event_from = bar_idx * event_per_bar
			event_to = event_from + event_per_bar
			event_text = event_text + event_text_temp[event_from:event_to]
			event_text.append('BAR ')

		return ' '.join(event_text)
    