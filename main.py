from classes import *
from euchre_engine import EuchEngine, GameState

pygame.init()
x_bound = 1024
y_bound = 768
bounds = (x_bound, y_bound)
window = pygame.display.set_mode(bounds)
pygame.display.set_caption("EchurePy")

gameEngine = EuchEngine()

cardBack = pygame.image.load('cards/BACK.png')
cardBack = pygame.transform.scale(cardBack, (int(85.8), int(120)))

def renderGame(window):
  black = (0,0,0)
  white = (255,255,255)
  window.fill((53,101,77))
  font = pygame.font.SysFont("georgia", 20, True)

  player_turn = font.render(f"{gameEngine.currentPlayer.name}'s turn", True, white)
  window.blit(player_turn,(100 ,100))

  white_score = font.render(f"White's Score: {gameEngine.white_points}", True, white)
  black_score = font.render(f"Black's Score: {gameEngine.black_points}", True, black)
  window.blit(black_score, (100,125))
  window.blit(white_score, (100,150))
  
  names = [player.name for player in gameEngine.players]
  p0name = font.render(f"Player 0: {names[0]}", True, white)
  window.blit(p0name, (x_bound/2 - 80, 595))
  p1name = font.render(f"Player 1: {names[1]}", True, black)
  window.blit(p1name, (45, y_bound/2 -30))
  p2name = font.render(f"Player 2: {names[2]}", True, white)
  window.blit(p2name, (x_bound/2 - 80, 150))
  p3name = font.render(f"Player 3: {names[3]}", True, black)
  window.blit(p3name, (785, y_bound/2 -30))


  player0_cards_xcord = x_bound/2 -140
  player0_cards_ycord = 620
  for card in gameEngine.player0.hand:
    if card:
      window.blit(card.images, (player0_cards_xcord,player0_cards_ycord))
      player0_cards_xcord  += 50

  player1_cards_xcord = 10
  player1_cards_ycord = y_bound/2
  for card in gameEngine.player1.hand:
    if card:
      window.blit(card.images, (player1_cards_xcord, player1_cards_ycord))
      player1_cards_xcord += 50
  
  player2_cards_xcord = x_bound/2 -140
  player2_cards_ycord = 25
  for card in gameEngine.player2.hand:
    if card:
      window.blit(card.images, (player2_cards_xcord, player2_cards_ycord))
      player2_cards_xcord += 50
  
  player3_cards_xcord = 730
  player3_cards_ycord = y_bound/2
  for card in gameEngine.player3.hand:
    if card:
      window.blit(card.images, (player3_cards_xcord, player3_cards_ycord))
      player3_cards_xcord += 50


  kitty = gameEngine.deck.deck_cards[0]
  if kitty:
    window.blit(kitty.images, (785, 125))
    deck_name = font.render("Deck", True, white)
    window.blit(deck_name, (800, 100))
  
  pile_card_xcord = x_bound/2 - 80
  for card in gameEngine.pile.cards:
    if card:
      window.blit(card.images, (pile_card_xcord, y_bound/2))
      pile_card_xcord += 10

  
  if gameEngine.state == GameState.NOT_PLAYING:
    if gameEngine.white_points > gameEngine.black_points:
      text_end = font.render("Game Over, White wins, close the tab and press play to start a new game", True, white)
      window.fill((0,0,0))
    else:
      text_end = font.render("Game over, Black wins, close the tab and press play to start a new game", True, black)
      window.fill((255,255,255))
    window.blit(text_end, (x_bound -885, y_bound/2))

  
run = True
while run:
  key = None
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    if event.type == pygame.KEYDOWN:
      key = event.key


  gameEngine.play_game(key)
  renderGame(window)
  pygame.display.update()
