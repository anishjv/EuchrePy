from enum import Enum
from classes import EuchreDeck, Player, Pile
import pygame

class GameState(Enum):
  PLAYING = 0
  NOT_PLAYING = 1

class EuchEngine:
  player0 = None
  player1 = None
  player2 = None
  player3 = None
  pile = None
  state = None
  ties = 0
  currentPlayer = None


  def __init__(self):
      self.deck = EuchreDeck()
      self.deck.shuffle()
      self.player0 = Player(input("Player 0, enter name: "), pygame.K_p, pygame.K_t)
      self.player1 = Player(input("Player 1, enter name: "), pygame.K_p, pygame.K_t)
      self.player2 = Player(input("Player 2, enter name: "), pygame.K_p, pygame.K_t)
      self.player3 = Player(input("Player 3, enter name: "), pygame.K_p, pygame.K_t)
      self.player0.tricks_won = 0
      self.player1.tricks_won = 0
      self.player2.tricks_won = 0
      self.player3.tricks_won = 0
      self.players = [self.player0, self.player1, self.player2, self.player3]
      self.pile = Pile()
      self.game_deal()
      self.currentPlayer = self.player1
      self.move_counter = 0
      self.trump_suit = None
      self.trump_caller = None
      self.trick_winner = self.player0
      self.white_points = 0
      self.black_points = 0
      self.ties = 0
      self.state = GameState.PLAYING


  def game_deal(self):
    for player in self.players:
      for _ in range(3):
        player.hand.append(self.deck.deck_cards.pop(0))
      for _ in range(2):
        player.hand.append(self.deck.deck_cards.pop(0))


  def switchPlayer(self):
    if self.currentPlayer == self.player1:
      self.currentPlayer = self.player2
      self.move_counter += 1
    elif self.currentPlayer == self.player2:
      self.currentPlayer = self.player3
      self.move_counter += 1
    elif self.currentPlayer == self.player3:
      self.currentPlayer = self.player0
      self.move_counter += 1
    else:
      self.currentPlayer = self.player1
      self.move_counter += 1
   

  def clear_move_counter(self):
    self.move_counter = 0

  
  def win_trick(self):
    #finds the highest valued card
    pile_values = []
    for card in self.pile.cards:
      pile_values.append(card.value)
    highest_card_index = pile_values.index(max(pile_values))
    highest_card = self.pile.cards[highest_card_index]

    #checks for duplicates
    duplicate = 0
    pile_values.pop(highest_card_index)
    for value in pile_values:
      if value == highest_card.value:
        duplicate += 1
    
    if duplicate != 0:
        print("Checking for duplicates")
        self.trick_winner = None
        self.ties +=1

    # Decides winner if there are no duplicates
    elif duplicate == 0:
      if self.trick_winner == None:
        if highest_card == self.pile.cards[0]:
          self.player0.tricks_won += 1
          self.trick_winner = self.player0
      
      elif self.trick_winner != None:
        if highest_card == self.pile.cards[0]:
          self.trick_winner.tricks_won += 1
      
        elif self.trick_winner == self.player0:
          if highest_card == self.pile.cards[1]:
            self.player1.tricks_won += 1
            self.trick_winner = self.player1
          if highest_card == self.pile.cards[2]:
            self.player2.tricks_won +=1
            self.trick_winner = self.player2
        
        elif self.trick_winner == self.player1:
          if highest_card == self.pile.cards[1]:
            self.player2.tricks_won += 1
            self.trick_winner = self.player2
          if highest_card == self.pile.cards[2]:
            self.player3.tricks_won +=1
            self.trick_winner = self.player3
        
        elif self.trick_winner == self.player2:
          if highest_card == self.pile.cards[1]:
            self.player3.tricks_won += 1
            self.trick_winner = self.player3
          if highest_card == self.pile.cards[2]:
            self.player0.tricks_won +=1
            self.trick_winner = self.player0

        elif self.trick_winner == self.player3:
          if highest_card == self.pile.cards[1]:
            self.player0.tricks_won += 1
            self.trick_winner = self.player0
          if highest_card == self.pile.cards[2]:
            self.player1.tricks_won +=1
            self.trick_winner = self.player1
          

        elif highest_card == self.pile.cards[3]:
          self.currentPlayer.tricks_won +=1 
          self.trick_winner = self.currentPlayer


  def pick_kitty(self):
    while True:
      yes_no_pick = input("Would you like to pick-up the kitty? (Yes/No) ")
      if yes_no_pick == "Yes":
        self.player0.hand.pop(int(input("Enter index of the card that you'd like to replace: ")))
        self.player0.hand.append(self.deck.deck_cards[0])
        self.deck.deck_cards.pop(0)
        break
      if yes_no_pick == "No":
        break
      else:
        pass
    

  def call_trump(self):
    if self.move_counter <= 3:
      while True:
        self.trump_suit = self.currentPlayer.select_trump()
        if self.trump_suit == self.deck.deck_cards[0].suit:
          print(f"Trump called: {self.trump_suit}")
          break
        else:
          pass   
    else: 
      self.trump_suit = self.currentPlayer.select_trump()
      print(f"Trump called: {self.trump_suit}")
      
  
  def reorder_ranks(self):
    for player in self.players:
      for card in player.hand:

        if card.suit == self.trump_suit and card.value != 2:
          card.value += 6
        if card.suit == self.trump_suit and card.value == 2:
          card.value += 15
        
        if self.trump_suit == 0:
          if card.value == 2 and card.suit == 1:
            card.value += 14
        elif self.trump_suit == 1:
          if card.value == 2 and card.suit == 0:
            card.value += 14
        elif self.trump_suit == 2:
          if card.value == 2 and card.suit == 3:
            card.value += 14
        elif self.trump_suit == 3:
          if card.value == 2 and card.suit == 2:
            card.value += 14
        else:
          pass

  
  def reset_ranks(self):
    for card in self.deck.deck_cards:
      if card.value == 17:
        card.value = card.value - 15
      elif 5 < card.value < 12:
        card.value = card.value - 6
      elif card.value == 16:
        card.value = card.value - 14
  

  def play_game(self, key):
    card_check = True
    
    # If any team has ten points, stop the game
    if self.white_points == 10 or self.black_points == 10:
      self.state = GameState.NOT_PLAYING
    
    #If the pile has 4 cards, check who won the trick
    elif len(self.pile.cards) == 4 and (self.player0.tricks_won + self.player1.tricks_won + self.player2.tricks_won + self.player3.tricks_won + self.ties) < 4:
      print("Checking to see who won the trick...")
      self.win_trick()
      for card in self.pile.cards:
        self.deck.deck_cards.append(card)
      self.pile.clear()
      if self.trick_winner:
        self.currentPlayer = self.trick_winner
        print(f"{self.trick_winner.name} won the trick!")
      else:
        self.currentPlayer = self.player0
        print("It was a tie!")
      
    #If the pile has 4 cards and 4 tricks have been won, check who won the trick, then check who won the round
    elif (self.player0.tricks_won + self.player1.tricks_won + self.player2.tricks_won + self.player3.tricks_won + self.ties) >= 4 and len(self.pile.cards) == 4:
      print("Checking to see who won the round...")
      self.win_trick()
      for card in self.pile.cards:
        self.deck.deck_cards.append(card)
      self.pile.clear()
      self.clear_move_counter()

      white_team = [self.player0, self.player2]
      black_team = [self.player1, self.player3]
      if self.trump_caller in white_team:
        if self.player0.tricks_won + self.player2.tricks_won in [3,4]:
          self.white_points += 1
        if self.player0.tricks_won + self.player2.tricks_won == 5:
          self.white_points += 2
        if self.player1.tricks_won + self.player3.tricks_won in [3,4]:
          self.black_points += 2
        if self.player1.tricks_won + self.player3.tricks_won == 5:
          self.black_points += 4
      elif self.trump_caller in black_team:
        if self.player1.tricks_won + self.player3.tricks_won in [3,4]:
          self.black_points += 1
        if self.player1.tricks_won + self.player3.tricks_won == 5:
          self.black_points += 2
        if self.player0.tricks_won + self.player2.tricks_won in [3,4]:
          self.white_points += 2
        if self.player0.tricks_won + self.player2.tricks_won == 5:
          self.white_points += 4
      
      self.deck.shuffle()
      self.game_deal()
      self.reset_ranks()
      if self.trick_winner:
        self.currentPlayer = self.trick_winner
      else:
        self.currentPlayer = self.player0
      self.player0.tricks_won = 0
      self.player1.tricks_won = 0
      self.player2.tricks_won = 0
      self.player3.tricks_won = 0
      self.trump_suit = None
     

    #If we aren't checking who won a trick, or round, and no team has ten points, check for a player to pass
    elif key == self.currentPlayer.passKey and self.trump_suit == None:
      self.switchPlayer()
      self.white_points = 10

    #If we aren't checking who won a trick, or round, if no team has ten points and no-one is passing, check if they are calling trump
    elif key == self.currentPlayer.calltKey and self.move_counter <= 7:
      self.call_trump()
      self.trump_caller = self.currentPlayer
      self.pick_kitty()
      self.reorder_ranks()
      self.currentPlayer = self.player0
  
    #If no other event is occuring, the player must be playing, ask them what card they want to play
    elif len(self.pile.cards) < 5 and self.trump_suit != None:
      while True:
        index_to_play = self.currentPlayer.play()
        if len(self.pile.cards) == 0:
          self.pile.add(self.currentPlayer.hand[index_to_play])
          self.currentPlayer.hand.pop(index_to_play)
          break
          
        elif self.currentPlayer.hand[index_to_play].suit == self.pile.cards[0].suit:
          self.pile.add(self.currentPlayer.hand[index_to_play])
          self.currentPlayer.hand.pop(index_to_play)
          break
        
        
        elif self.currentPlayer.hand[index_to_play].suit != self.pile.cards[0].suit:
          card_check = False
          for card in self.currentPlayer.hand:
            if card.suit == self.pile.cards[0].suit:
              card_check = True
              pass

        if card_check == False:
          self.pile.add(self.currentPlayer.hand[index_to_play])
          self.currentPlayer.hand.pop(index_to_play)
          break
      self.switchPlayer()             







    