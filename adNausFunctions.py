# Functions for adNaus

import random

def scry( field, hand, suspend, deck, bottom, num ):

	# Pick two cards from the deck
	card1 = random.choice( deck )
	deck.remove( card1 )
	if num == 2:
		try:
			card2 = random.choice( deck )
		except IndexError:
			card2 = ""
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

	# Put cards kept back in the deck
	if scryCard1 != "":
		deck.append( scryCard1 )
	if scryCard2 != "":
		deck.append( scryCard2 )

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

	keptCard = ""
	botCard = ""

	# Take a combo piece we don't have
	if "naus" in {card1, card2}  and "naus" not in hand:
		keptCard = "naus"
		if card1 == "naus":
			botCard = card2
		else:
			botCard = card1

	if "grace" in {card1, card2} and "grace" not in hand and "unlife" not in set(field) & set(hand):
		if keptCard == "":
			keptCard = "grace"
			if card1 == "grace":
				botCard = card2
			else:
				botCard = card1

	if "unlife" in {card1, card2} and "grace" not in hand and "unlife" not in set(field) & set(hand):
		if keptCard == "":
			keptCard = "unlife"
			if card1 == "unlife":
				botCard = card2
			else:
				botCard = card1

	if "spoils" in {card1, card2} and "naus" not in hand and "spoils" not in hand:
		if keptCard == "":
			keptCard = "spoils"
			if card1 == "spoils":
				botCard = card2
			else:
				botCard = card1

	# Take mana if we need it
	if "bloom" in {card1, card2} and "bloom" not in hand and "bloom" not in suspend:
		if "prism" not in set(hand) & set(field) or len( lands ) + len( tapped ) < 2:
			if keptCard == "":
				keptCard = "bloom"
				if card1 == "bloom":
					botCard = card2
				else:
					botCard = card1

	if "prism" in {card1, card2} and "bloom" not in hand and "bloom" not in suspend:
		if "prism" not in set(hand) & set(field):
			if keptCard == "":
				keptCard = "prism"
				if card1 == "prism":
					botCard = card2
				else:
					botCard = card1

	# Take dig
	if "visions" in {card1, card2}:
		if keptCard == "":
			keptCard = "visions"
			if card1 == "visions":
				botCard = card2
			else:
				botCard = card1

	if "sleight" in {card1, card2}:
		if keptCard == "":
			keptCard = "sleight"
			if card1 == "sleight":
				botCard = card2
			else:
				botCard = card1

	# If still haven't found anything, take anything other than storm
	if keptCard == "":
		if card1 == "storm":
			keptCard = card2
			botCard = card1
		if card2 == "storm":
			keptCard = card1
			botCard = card2

	if keptCard == "":
		keptCard = card1
		botCard = card2

	# Put kept card in hand, bottom card on bottom of deck
	hand.append( keptCard )
	bottom.append( botCard )
