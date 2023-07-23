import random
import pygame

class Card(object):              
  def __init__(self, value, suit):
      self.value = value
      self.suit = suit
      self.images = pygame.image.load("cards/" + str(self.suit) + '-' + str(self.value) + '.svg')
      self.images = pygame.transform.scale(self.images, (int(85.8), int(120)))
      self.showing = True

  def __repr__(self):
      value_name = ""
      suit_name = ""
      if self.showing:
          if self.value == 0:
              value_name = "Nine"
          elif self.value == 1:
              value_name = "Ten"
          elif self.value == 2:
              value_name = "Jack"
          elif self.value == 3:
              value_name = "Queen"
          elif self.value == 4:
              value_name = "King"
          elif self.value == 5:
              value_name = "Ace"
          elif self.value > 5:
             value_name = "Trump"
          
          if self.suit == 0:
              suit_name = "Diamonds"
          elif self.suit == 1:
              suit_name = "Hearts"
          elif self.suit == 2:
              suit_name = "Clubs"
          elif self.suit == 3:
              suit_name = "Spades"
          return f"{value_name} of {suit_name}"
      else:
          return "[CARD]"

class EuchreDeck(list):
  def __init__(self):
       super().__init__()
       suits = list(range(4))
       values = list(range(6))
       self.deck_cards = []
       for j in suits:
          for i in values:
             self.deck_cards.append(Card(i, j))
      
                     
  def shuffle(self):
      random.shuffle(self.deck_cards)

  def peek(self):
    if (len(self.deck_cards) > 0):
      return self.deck_cards[0]
    else:
      return None


class Pile():
  def __init__(self):
    self.cards = []

  def add(self, card):
    self.cards.append(card)

  def clear(self):
    self.cards = []

  def peek(self):
    if (len(self.cards) > 0):
      return self.cards[-1]
    else:
      return None


class Player(object):
  hand = None
  playKey = None
  name = None
  tricks_won = 0

  def __init__(self, name, passKey, calltKey):
    self.hand = []
    self.name = name
    self.passKey = passKey
    self.calltKey = calltKey
    self.tricks_won = 0

  def play(self):
    while True:
      try:
        card_select = int(input("What card would you like to play? "))
        if card_select in range(0, len(self.hand)):
         return card_select
        else:
          pass
      except (ValueError, UnboundLocalError):
         pass
      
       
  def select_trump(self):
    while True:
      try:
        suit_int = int(input("Enter 0 for Diamonds, 1 for Hearts, 2 for Clubs, or 3 for Spades: "))
        if suit_int in [0,1,2,3]:
          return suit_int
        else:
          pass
      except (ValueError, UnboundLocalError):
         pass