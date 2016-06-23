"""
Author: /u/Azgurath
"""

import random
import sys
from adNausFunctions import *

## Draw or Play, from command line

if sys.argv[1] == "False":
	on_the_draw = False
else:
	on_the_draw = True

## Number of games to test, from command line

N = int(sys.argv[2])

def game(draw):
	# Populate deck
	deck = ["visions", "visions", "visions", "visions", "sleight", "sleight", "sleight", "sleight", "lotus", "lotus", "lotus", "lotus", "prism", "prism", "prism", "prism", "grace", "grace", "grace", "grace", "naus", "naus", "naus", "naus", "unlife", "unlife", "unlife", "unlife", "guide", "guide", "guide", "guide", "storm", "storm"] 
	deck.extend( ["deceit", "deceit", "deceit", "deceit", "enlight", "enlight", "enlight", "enlight", "coast", "coast", "coast", "coast", "plains", "island", "mine", "mine", "mine", "mine", "shores", "shores", "shores", "shores"] )
	for x in range(60 - len(deck)):
		deck.append("dead")

	# Populate field
	field = []
	lands = []
	tapped = []

	# Populate suspend
	suspend = []

	# Populate cards on bottom
	bottom = []

	# Populate starting hand
	starting_size = 7
	decided_on_hand = False
	hand = random.sample( deck, 7 )

	# Mulligan
	# Keep if 2 or more lands...
	# VERY TEMPORARY

	while not decided_on_hand and starting_size > 0:

		#natural tron
		if "Mine" in hand and "Tower" in hand and "PP" in hand:
			have_tron = True
			decided_on_hand = True

		#guarunteed tron
		elif( two_in_hand(hand)
			and (
				( "map" in hand )
				or ( "scry" in hand and "star" in hand )
				)
			):
			have_tron = True
			decided_on_hand = True

		#2 pieces
		if starting_size <= 6 and not decided_on_hand:
			if two_in_hand(hand):
				decided_on_hand = True
			if "Tower" in hand or "Mine" in hand or "PP" in hand:
				if "map" in hand or "scry" in hand:
					decicded_on_hand = True

		#1 piece
		if starting_size <= 4 and not decided_on_hand:
			if "Tower" in hand or "Mine" in hand or "PP" in hand:
				decided_on_hand = True

		#Mull to 3
		if starting_size <= 3 and not decided_on_hand:
			decided_on_hand = True

		#Mulligan
		if not decided_on_hand:
			starting_size -= 1
			hand = random.sample( deck, starting_size )

	# Take the cards in hand from the deck

	for card in hand:
		deck.remove( card )

	# Scry if mulliganed

	scry = starting_size < 7
	scry_bottom = True
	new_card = ""
	if scry and not have_tron:
	
		new_card = random.choice( deck )
		#Have two pieces, keep map or third piece
		if two_in_hand( hand ):
			if new_card in {"map", "Tower", "Mine", "PP"} and new_card not in hand:
				scry_bottom = False
			if new_card == "scry" and "star" in hand:
				scry_bottom = False
			if new_card == "star" and "scry" in hand:
				scry_bottom = False
			if new_card == "stir" and ( "star" in hand or "forest" in hand ):
				scry_bottom = False 

		if scry_bottom:
			deck.remove( new_card )
			bottom.append( new_card )
			new_card = ""
						
	# Main loop for turns!
	turn = 0
	kill = False
	while not kill:

		# increment turn counter
		turn += 1

		# decrement suspend counter
		for card in suspend:
			if card == "bloom":
				suspend
	
		# track if we played a land	
		playedLand = False

		# draw a card

		# if it's the first card after scrying
		if (draw and turn == 1) or (not draw and turn == 2):
			if new_card == "":
				new_card = random.choice( deck )
			hand.append( new_card )
			deck.remove( new_card )

		# otherwise
		elif draw or turn != 1:
			new_card = random.choice( deck )
			hand.append( new_card )
			deck.remove( new_card )

		# Suspend lotus blooms
		for card in hand:
			is card == "bloom":
				hand.remove( card )
				suspend.append( card )
				suspend.append( 3 )

		# play a scry land
		for card in hand:
			if card in {"deceit", "enlight"} and not playedLand:
				hand.remove( card )
				tapped.append( card )
				scry( hand, field, suspend, deck, lands, tapped, 1 )
				playedLand = True

		# play check land
		if not playedLand:
			for card in hand:
				if card in {"shores", "coast"} and not playedLand:
					hand.remove( card )
					if lands.size > 2:
						tapped.append( card )
					else:
						lands.append( card )
					playedLand = True

		# play other land
		if not playedLand:
			for card in hand:
				if card in {"island", "plains", "mine"} and not playedLand:
					hand.remove( card )
					lands.append( card )
					playedLand = True

		
		

		# end turn

	return( turn, starting_size, "Karn" in hand )

turn_three_tron = 0
turn_four_tron = 0
turn_three_karn = 0
total_have_karn = 0
total_turns = 0
failed_to_tron = 0
failed_starting_size = 0
success_starting_size = 0

for i in range( N ):
	turn, starting_size, have_karn = game( on_the_draw )
	if turn == 3:
		turn_three_tron += 1

	if turn == 3 and have_karn:
		turn_three_karn += 1

	if turn <= 4:
		turn_four_tron += 1

	if have_karn:
		total_have_karn += 1

	if turn < 10:
		total_turns += turn
		success_starting_size += starting_size
	else:
		failed_to_tron += 1
		failed_starting_size += starting_size

avg_turns = total_turns / float( i - failed_to_tron )
failed_avg_size = failed_starting_size / float( failed_to_tron )
avg_size = success_starting_size / float( i - failed_to_tron )

print "Turn three tron: ", turn_three_tron / float( i ) * 100
print "Turn three Karn: ", turn_three_karn / float( i ) * 100
print "Turn three or four tron: ", turn_four_tron /  float( i ) * 100
print "Average turn tron: ", avg_turns
print "Have Karn when tron is done: ", total_have_karn / float( i ) * 100
print "Failed to get tron by tun 10: ", failed_to_tron / float( i ) * 100
print "Mulled to an average of: ", avg_size
print "When failed to get tron, mulled to: ", failed_avg_size
