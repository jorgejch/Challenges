'''
Solution for the LastFM code challenge.
*Author: Jorge Haddad
*Last edit: 06/10/12
*Time spent projecting: 1 hour.
*Time implementing 1st draft: 3 hours.
*Time spent refactoring and commenting: 1-2 hours.

*Usage:
# python ./fans_lists.py < foo
'''

import sys
import random

class Main:
	'''
	Main class. Contains the start() static method. Entry point for the program.
	'''
	
	@staticmethod
	def start():
		'''
		Contains the main algorithm of the program.
		1. Reads STDIN, and splits each line into an artist's name list.
		2. Iterates through the list creating Artist objects when pertinent, 
		and adding the "fans" (fan_id) to the Artist objects.
		3. Compares the fans sets (fans_set) of each pertinent pair of Artists,
		outputing those that have 50 or more common fans.
		'''
		fan_id = 0

		for line in sys.stdin:
			artists_names_list = line.strip().split(',')
			fan_id += 1

			for artist_name_str in artists_names_list:
				artist_obj = Artist.artists_dict[artist_name_str] if (artist_name_str in Artist.artists_dict) else Artist(artist_name_str)
				artist_obj.add_fan(fan_id)

		while True:	
			try:
				artist_obj = Artist.artists_dict.popitem()[1]
			except KeyError:
				break

			if artist_obj.get_fans_count() < 50: 
				continue	#Skips unnecessary comparisons.

			for other_artist_obj in iter(Artist.artists_dict.values()):
				if other_artist_obj.get_fans_count() < 50:
					continue	#Skips unnecessary comparisons.
				count = artist_obj.count_fan_intersection(other_artist_obj)	 
				if count >= 50:
					print(artist_obj.get_name() + "," + other_artist_obj.get_name())

class Artist:
	'''
	An instance of the Artist class keeps a record of the artist's
	fans, and is able to return the number of common fans it has with
	another artist (instance).
	'''

	#Class atribute (static variable) with a reference
	# to a dict meant to contain all instatiated artists. 
	#The key is an artist object's name, and the
	# value is a reference to the artist object.
	artists_dict = dict() 

	def __init__(self, name_str_arg):
		'''
		Initialises and instantiates the name, quantity of fans,
		and set of fans. Also, includes the artist on the static
		artists dict.
		'''
		self.name_str = name_str_arg 
		self.fans_qnt_int = 0
		self.fans_set = set()
		Artist.artists_dict[self.name_str] = self

	def add_fan(self, fan_id_arg):
		'''
		Adds a fan to the fans set, and increments the fans quatity
		counter.
		'''
		self.fans_set.add(fan_id_arg)
		self.fans_qnt_int += 1
		
	def count_fan_intersection(self, other_artist_obj_arg):
		'''
		Returns the count of common fans between self and another
		artist obj.
		'''
		counter = 0		
		
		(fans_set, other_fans_set) = (other_artist_obj_arg.fans_set, self.fans_set) if len(other_artist_obj_arg.fans_set) < len(self.fans_set) else (self.fans_set, other_artist_obj_arg.fans_set)

		for fan_id_int in fans_set:
			if fan_id_int in other_fans_set:
				counter += 1
			if counter == 50:
				break

		return counter

	def get_fans_count(self):
		'''
		The Get Function for the artists fans quantity.
		'''
		return self.fans_qnt_int

	def get_name(self):
		'''
		The Get Function for the the artists name local str.
		'''
		return self.name_str

if __name__ == "__main__":
	main_class = Main()
	main_class.start()
