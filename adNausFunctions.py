# Functions for adNaus

import random

def scry( field, hand, suspend, deck, bottom, num ):

	print "HELLO THERE WOULD YOU LIKE TO BE IN THE FUNCTION?"

	# Pick two cards from the deck
	card1 = random.choice( deck )
	deck.remove( card1 )
	if num == 2:
		card2 = random.choice( deck )
		deck.remove( card2 )
	else:
		card2 = ""

	# The two cards chosen
	scryCard1 = ""
	scryCard2 = ""

	# Take a combo piece we don't have
	if "naus" in {card1, card2}  and "naus" not in hand:
		scryCard1 = "naus"

	if "grace" in {card1, card2} and "grace" not in hand and "unlife" not in set(field) & set(hand):
		if scryCard1 == "":
			scryCard1 = "grace"
		else:
			scryCard2 = "grace"

	if "unlife" in {card1, card2} and "grace" not in hand and "unlife" not in set(field) & set(hand):
		if scryCard1 == "":
			scryCard1 = "unlife"
		elif scryCard2 == "":
			scryCard2 = "unlife"

	if "spoils" in {card1, card2} and "naus" not in hand and "spoils" not in hand:
		if scryCard1 == "":
			scryCard1 = "spoils"
		elif scryCard2 == "":
			scryCard2 = "spoils"

	# Take mana if we need it
	if "bloom" in {card1, card2} and "bloom" not in hand and "bloom" not in suspend:
		if "prism" not in set(hand) & set(field) or len( lands ) + len( tapped ) < 2:
			if scryCard1 == "":
				scryCard1 = "bloom"
			elif scryCard2 == "":
				scryCard2 = "bloom"

	if "prism" in {card1, card2} and "bloom" not in hand and "bloom" not in suspend:
		if "prism" not in set(hand) & set(field):
			if scryCard1 == "":
				scryCard1 = "prism"
			elif scryCard2 == "":
				scryCard2 = "prism"

	# Take dig
	if "visions" in {card1, card2}:
		if scryCard1 == "":
			scryCard1 = "visions"
		elif scryCard2 == "":
			scryCard2 = "visions"

	if "sleight" in {card1, card2}:
		if scryCard1 == "":
			scryCard1 = "sleight"
		elif scryCard2 == "":
			scryCard2 = "sleight"

	# But cards not kept on the bottom
	if scryCard1 != card1:
		bottom.append( card1 )
	if scryCard2 != card2:
		bottom.append( card2 )

	return( scryCard1, scryCard2 )

def castSleight( field, hand, suspend, deck, bottom ):
	
	# Take two cards
	card1 = random.choice( deck )
	deck.remove( card1 )
	card2 = random.choice( deck )
	deck.remove( card2 )

	
