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
	deck = ["grace", "naus", "unlife", "guide", "visions", "hand", "bloom", "prism", "coast", "shores", "mine", "deceit"]
	for i in range(2):
		deck.extend( deck )
	deck.extend( ["island", "plains", "englight", "enlight", "storm", "storm", "pact", "pact", "pact", "spoils", "spoils", "spoils"] )

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
	startingSize = 7
	decidedOnHand = False
	hand = random.sample( deck, 7 )

	# Mulligan
	# Keep if 2 or more lands...
	# VERY TEMPORARY

	while not decidedOnHand and startingSize > 0:
	
		decidedOnHand = True

	# Take the cards in hand from the deck

	for card in hand:
		deck.remove( card )

	# Scry if mulliganed

	scry = startingSize < 7
	scry_bottom = True
	newCard = ""
	if scry and not have_tron:
	
		newCard = random.choice( deck )

		if scry_bottom:
			deck.remove( newCard )
			bottom.append( newCard )
			newCard = ""
						
	# Main loop for turns!
	turn = 0
	kill = False
	while not kill:

		# increment turn counter
		turn += 1

		# untap lands
		lands.extend( tapped )
		tapped = []

		# decrement suspend counter, play suspended cards at 0 counters
		for card in suspend:
			if "bloom" in card:
				card[1] -= 1
				if card[1] == 0:
					field.append( card[0] )
					suspend.remove(card)
	
		# track if we played a land	
		playedLand = False

		# draw a card

		# if it's the first card after scrying
		if (draw and turn == 1) or (not draw and turn == 2):
			if newCard == "":
				newCard = random.choice( deck )
			hand.append( newCard )
			deck.remove( newCard )

		# otherwise
		elif draw or turn != 1:
			newCard = random.choice( deck )
			hand.append( newCard )
			deck.remove( newCard )

		# Suspend lotus blooms
		for card in hand:
			if card == "bloom":
				hand.remove( card )
				suspend.append( [card,3] )

		# play a scry land
		for card in hand:
			if card in {"deceit", "enlight"} and not playedLand:
				hand.remove( card )
				tapped.append( card )
				# scry( hand, field, suspend, deck, lands, tapped, 1 )
				playedLand = True

		# play check land
		if not playedLand:
			for card in hand:
				if card in {"shores", "coast"} and not playedLand:
					hand.remove( card )
					if len( lands ) > 2:
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

		kill =  len( lands ) > 3

		# end turn

	return( turn, startingSize, "Karn" in hand )

for i in range( N ):
	turn, startingSize, have_karn = game( on_the_draw )
	print "It took this many turns: ", turn

