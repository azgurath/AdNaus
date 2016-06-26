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
	deck = ["grace", "naus", "unlife", "guide", "visions", "sleight", "bloom", "prism", "coast", "shores", "mine", "deceit"]
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

	# Populate top two cards
	scryCard1 = ""
	scryCard2 = ""

	# Populate starting hand
	startingSize = 7
	decidedOnHand = False
	hand = random.sample( deck, 7 )

	# Mulligan
	# Keep if 2 or more lands...
	# VERY TEMPORARY

	while not decidedOnHand and startingSize > 0:

		handStrength = 0.0
		handStrength += (7 - startingSize)
		if "naus" in hand:
			handStrength += 1
		if "grace" in hand or "unlife" in hand:
			handStrength += 1
		if "bloom" in hand or "prism" in hand:
			handStrength += 1
		if "naus" not in hand or( "grace" not in hand and "unlife" not in hand ):
			if "spoils" in hand:
				handStrength += 0.5
		if "visions" in hand:
			handStrength += 0.5
		if "sleight" in hand:
			handStrength += 0.5

		if handStrength >= 3:
			decidedOnHand = True

		if not decidedOnHand:
			startingSize -= 1
			hand = random.sample( deck, startingSize )

	# Take the cards in hand from the deck

	for card in hand:
		deck.remove( card )

	# Scry if mulliganed

	if startingSize < 7:
		scryCard1, scryCard2 = scry( field, hand, suspend, deck, bottom, 1 )
	newCard = scryCard1

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

		if turn != 1 or draw:
			# make sure we draw what's been scryed	
			if scryCard1 == "":
				newCard = random.choice( deck )
			else:
				newCard = scryCard1
				scryCard1 = scryCard2
				scryCard2 = ""
			hand.append( newCard )
			deck.remove( newCard )


		# play a scry land
		for card in hand:
			if card in {"deceit", "enlight"} and not playedLand:
				hand.remove( card )
				tapped.append( card )
				scryCard1, scryCard2 = scry( field, hand, suspend, deck, bottom, 1 )
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

		# see if we won
		mana = 0
		for card in field:
			if card == "bloom":
				mana += 3
			if "prism" in card:
				mana += card[1]
		mana += len( lands )

		if "naus" in hand:
			if "unlife" in field and mana >= 4:
				if "guide" in hand or mana >= 5:
					kill = True
			if "grace" in hand and mana >= 5:
				if "guide" in hand or mana >= 6:
					kill = True

		if "spoils" in hand:
			if "unlife" in field and mana >= 6:
				kill = True
			if "grace" in hand and mana >= 7:
				kill = True

		# play sleight of hand if possible
		for land in lands:
			if land in {"shores", "deceit", "enlight", "coast", "island", "mine"} and "sleight" in hand:
				lands.remove( land )
				tapped.append( land )
				hand.remove( "sleight" )
				castSleight( field, hand, suspend, deck, bottom )
		
		# play serum visions if possible
		for land in lands:
			if land in {"shores", "deciet", "enlight", "coast", "island", "mine"} and "visions" in hand:
				lands.remove( land )
				tapped.append( land )
				hand.remove( "visions" )
				# Draw a card
				if scryCard1 != "":
					newCard = scryCard1
					scryCard1 = scryCard2
					scryCard2 = "";
				else:
					newCard = random.choice( deck )
				print newCard
				print deck
				hand.append( newCard )
				deck.remove( newCard )
				# Scry 2
				scryCard1, scryCard2 = scry( field, hand, suspend, deck, bottom, 2 )

		# play pentad prism if possible if mana is needed
		if mana < 6 and len(suspend) == 0:
			if len( lands ) >= 2 and "prism" in hand:
				tapped.append( lands[0] )
				tapped.append( lands[1] )
				del lands[:2]	
				hand.remove( "prism" )
				field.append( ("prism", 2) )

		# play phyrexian unlife if possible
		if len( lands ) >= 3 and "unlife" in hand:
			canCast = False
			for land in {"plains", "coast", "enlight", "mine"}:
				if land in lands and not canCast:
					canCast = True
					tapped.append( land )
					lands.remove( land )
			if canCast:
				tapped.append( lands[0] )
				tapped.append( lands[1] )
				del lands[:2]
				hand.remove( "unlife" )
				field.append( "unlife" )

		# Suspend lotus blooms
		for card in hand:
			if card == "bloom":
				hand.remove( card )
				suspend.append( [card,3] )

		# end turn

		if len(deck) < 10:
			print "Almost dead to cards..."
			kill = True
	return( turn, startingSize, len(lands) + len(tapped) )

killTurn = 0

for i in range( N ):
	turn, startingSize, landsNum = game( on_the_draw )
	killTurn += turn

killTurn = killTurn / float( N )
print "Average kill on turn: ", killTurn

