import json
from pathlib import Path
import pygame,sys, random
from pygame.locals import *

from MatchPvsP import MatchPvsP
from Player import Player

#CONSTANTS


#COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (220,220,220)
RED = (255,0,0)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1000
BLUE = (7, 88, 230)
LIGHT_BLUE = (47, 128, 255)

def playerVsPlayerWindow(match):

	pygame.init()

	surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption("TRIQUI PvsP")
	font = pygame.font.SysFont("ocraextended", 20)
	fontWIN = pygame.font.SysFont("ocraextended", 40)

	running = True #Estado de la ventana

	rect1 = pygame.Rect((100,200), (200,200))
	rect2 = pygame.Rect((300,200), (200,200))
	rect3 = pygame.Rect((500,200), (200,200))

	rect4 = pygame.Rect((100,400), (200,200))
	rect5 = pygame.Rect((300,400), (200,200))
	rect6 = pygame.Rect((500,400), (200,200))

	rect7 = pygame.Rect((100,600), (200,200))
	rect8 = pygame.Rect((300,600), (200,200))
	rect9 = pygame.Rect((500,600), (200,200))

	rects = [rect1,rect2,rect3,rect4,rect5,rect6,rect7,rect8,rect9]
	rectsSelected = ["","","","","","","","",""]
	someoneWins = False
	winLine = None
	tie = False
	pygame.time.set_timer(pygame.USEREVENT, 100)
	counter = 0

	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN and someoneWins == False:
				for i in range(len(rects)):
					if rectsSelected[i] == "":
						collide = rects[i].collidepoint(point)
						if collide:
							if match.nextTurn == 1 and match.player1Symbol == "X" or match.nextTurn == 2 and match.player2Symbol == "X":
								rectsSelected[i] = "X"
								counter = 0
							elif match.nextTurn == 1 and match.player1Symbol == "O" or match.nextTurn == 2 and match.player2Symbol == "O":
								rectsSelected[i] = "O"
								counter = 0
							match.nextTurn = 1 if match.nextTurn == 2 else 2
							winner = match.verifyIfWinner(rectsSelected)
							if winner != None:
								winLine = winner[1]
								if winner == ("-", 0):
									tie = True
								elif winner[0] == "X":
									someoneWins = True
									if match.player1Symbol == "X":
										match.lastWin = "player1"
										match.player1Score += 1
										match.player1.totalPoints += 100
										match.player1.totalWins += 1
										match.player2.totalPoints += 20
										match.player2.totalLoses += 1
										match.player1.saveData(True)
										match.player2.saveData(False)
									else:
										match.player2Score += 1
										match.lastWin = "player2"
										match.player2.totalPoints += 100
										match.player2.totalWins += 1
										match.player1.totalPoints += 20
										match.player1.totalLoses += 1
										match.player1.saveData(False)
										match.player2.saveData(True)
								elif winner[0] == "O":
									someoneWins = True
									if match.player1Symbol == "O":
										match.lastWin = "player1"
										match.player1Score += 1
										match.player1.totalPoints += 100
										match.player1.totalWins += 1
										match.player2.totalPoints += 20
										match.player2.totalLoses += 1
										match.player1.saveData(True)
										match.player2.saveData(False)
									else:
										match.lastWin = "player2"
										match.player2Score += 1
										match.player2.totalPoints += 100
										match.player2.totalWins += 1
										match.player1.totalPoints += 20
										match.player1.totalLoses += 1
										match.player1.saveData(False)
										match.player2.saveData(True)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN and (someoneWins == True or tie == True):		
					someoneWins = False
					rectsSelected = ["","","","","","","","",""]
					counter = 0
					tie = False
			if event.type == pygame.USEREVENT:
				counter += 0.100
		surface.fill(WHITE)
		point = pygame.mouse.get_pos()


		#PAINT BOARD
		pygame.draw.line(surface, BLACK, (100, 400), (700, 400), 2)
		pygame.draw.line(surface, BLACK, (100, 600), (700, 600), 2)
		pygame.draw.line(surface, BLACK, (300, 200), (300, 800), 2)
		pygame.draw.line(surface, BLACK, (500, 200), (500, 800), 2)

		#PAINT NAMES & SCORE
		name1AndScore = font.render(match.player1Symbol + " - " + match.player1.name + ": " + str(match.player1Score), True, BLACK)
		name2AndScore = font.render(match.player2Symbol + " - " + match.player2.name + ": " + str(match.player2Score), True, BLACK)
		score = font.render("Puntuación", True, BLACK)
		surface.blit(score, (50,0))
		surface.blit(name1AndScore, (50,50))
		surface.blit(name2AndScore, (50,100))
		
		#NOONE WINS
		if someoneWins == False and tie == False:
			if match.nextTurn == 1 and match.player1Symbol == "X" or match.nextTurn == 2 and match.player2Symbol == "X":
				for i in range(len(rects)):
					if rectsSelected[i] == "":
						collide = rects[i].collidepoint(point)
						if collide:
							pygame.draw.line(surface, GREY, (rects[i].left + 10, rects[i].top + 10), (rects[i].left + rects[i].width - 10, rects[i].top + rects[i]. height - 10), width=5)
							pygame.draw.line(surface, GREY, (rects[i].left + 10, rects[i].top + rects[i].height - 10), (rects[i].left + rects[i].width - 10, rects[i].top + 10), width=5)

			if match.nextTurn == 1 and match.player1Symbol == "O" or match.nextTurn == 2 and match.player2Symbol == "O":
				for i in range(len(rects)):
					if rectsSelected[i] == "":
						collide = rects[i].collidepoint(point)
						if collide:
							pygame.draw.circle(surface, GREY, (rects[i].left + rects[i].width/2, rects[i].top + rects[i].height/2), rects[i].width/2 - 10, width=5)

			
			turnName = match.player1.name if match.nextTurn == 1 else match.player2.name
			if counter > 10:
				turnMessage = font.render("Turno de " + turnName + "  " + str(format(counter, ".1f")), True, RED)
			else:
				turnMessage = font.render("Turno de " + turnName + "  " + str(format(counter, ".1f")), True, BLACK)
			turnMessage_rect = turnMessage.get_rect(center=(SCREEN_WIDTH/2, 850))
			surface.blit(turnMessage, turnMessage_rect)

		#GAME SELECTIONS
		for i in range(len(rectsSelected)):
			if rectsSelected[i] == "X":
				pygame.draw.line(surface, BLACK, (rects[i].left + 10, rects[i].top + 10), (rects[i].left + rects[i].width - 10, rects[i].top + rects[i]. height - 10), width=5)
				pygame.draw.line(surface, BLACK, (rects[i].left + 10, rects[i].top + rects[i].height - 10), (rects[i].left + rects[i].width - 10, rects[i].top + 10), width=5)
			elif rectsSelected[i] == "O":
				pygame.draw.circle(surface, BLACK, (rects[i].left + rects[i].width/2, rects[i].top + rects[i].height/2), rects[i].width/2 - 10, width=5)

		if tie == True:
			tieMessage = fontWIN.render("EMPATE", True, RED)
			tieMessage_rect = tieMessage.get_rect(center=(SCREEN_WIDTH/2, 850))
			surface.blit(tieMessage, tieMessage_rect)
			continueMessage = font.render("PRESIONE ENTER PARA JUGAR OTRA VEZ", True, BLACK)
			continueMessage_rect = continueMessage.get_rect(center=(SCREEN_WIDTH/2, 950))
			surface.blit(continueMessage, continueMessage_rect)

		#PAINT IF SOMEONE WINS THE GAME
		if someoneWins == True:
			winnerName = match.player1.name if match.lastWin == "player1" else match.player2.name
			winnerMessage = fontWIN.render(winnerName + " GANO", True, BLACK)
			winnerMessage_rect = winnerMessage.get_rect(center=(SCREEN_WIDTH/2, 850))
			surface.blit(winnerMessage, winnerMessage_rect)
			continueMessage = font.render("PRESIONE ENTER PARA JUGAR OTRA VEZ", True, BLACK)
			continueMessage_rect = continueMessage.get_rect(center=(SCREEN_WIDTH/2, 950))
			surface.blit(continueMessage, continueMessage_rect)

			startRect = None
			endRect = None
			if winLine == 1:
				startRect = rect1
				endRect = rect3
			elif winLine == 2:
				startRect = rect4
				endRect = rect6
			elif winLine == 3:
				startRect = rect7
				endRect = rect9
			elif winLine == 4:
				startRect = rect1
				endRect = rect7
			elif winLine == 5:
				startRect = rect2
				endRect = rect8
			elif winLine == 6:
				startRect = rect3
				endRect = rect9
			elif winLine == 7:
				startRect = rect1
				endRect = rect9
			elif winLine == 8:
				startRect = rect3
				endRect = rect7
			pygame.draw.line(surface, RED, (startRect.left + startRect.width/2, startRect.top + startRect.height/2), (endRect.left + endRect.width/2, endRect.top + endRect.height/2), width=10)

		button("Inicio", 20, 950, 100, 30, BLUE, LIGHT_BLUE,20, surface, initWindow)

		pygame.display.update()

def playerVsBotWindow(match):

	pygame.init()

	surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption("TRIQUI PvBot")
	font = pygame.font.SysFont("ocraextended", 20)
	fontWIN = pygame.font.SysFont("ocraextended", 40)

	running = True #Estado de la ventana

	rect1 = pygame.Rect((100,200), (200,200))
	rect2 = pygame.Rect((300,200), (200,200))
	rect3 = pygame.Rect((500,200), (200,200))

	rect4 = pygame.Rect((100,400), (200,200))
	rect5 = pygame.Rect((300,400), (200,200))
	rect6 = pygame.Rect((500,400), (200,200))

	rect7 = pygame.Rect((100,600), (200,200))
	rect8 = pygame.Rect((300,600), (200,200))
	rect9 = pygame.Rect((500,600), (200,200))

	rects = [rect1,rect2,rect3,rect4,rect5,rect6,rect7,rect8,rect9]
	rectsSelected = ["","","","","","","","",""]
	someoneWins = False
	winLine = None
	tie = False
	pygame.time.set_timer(pygame.USEREVENT, 100)
	counter = 0

	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN and someoneWins == False:
				for i in range(len(rects)):
					if rectsSelected[i] == "":
						collide = rects[i].collidepoint(point)
						if collide:
							if match.nextTurn == 1 and match.player1Symbol == "X":
								rectsSelected[i] = "X"
								counter = 0
							elif match.nextTurn == 1 and match.player1Symbol == "O":
								rectsSelected[i] = "O"
								counter = 0
							match.nextTurn = 1 if match.nextTurn == 2 else 2
							winner = match.verifyIfWinner(rectsSelected)
							if winner != None:
								winLine = winner[1]
								if winner == ("-", 0):
									tie = True
								elif winner[0] == "X":
									someoneWins = True
									if match.player1Symbol == "X":
										match.lastWin = "player1"
										match.player1Score += 1
										match.player1.totalPoints += 30
										match.player1.totalWins += 1
										match.player2.totalPoints += 20
										match.player2.totalLoses += 1
										match.player1.saveData(True, True)
									else:
										match.player2Score += 1
										match.lastWin = "player2"
										match.player2.totalPoints += 30
										match.player2.totalWins += 1
										match.player1.totalPoints -= 20
										match.player1.totalLoses += 1
										match.player1.saveData(False, True)
								elif winner[0] == "O":
									someoneWins = True
									if match.player1Symbol == "O":
										match.lastWin = "player1"
										match.player1Score += 1
										match.player1.totalPoints += 30
										match.player1.totalWins += 1
										match.player2.totalPoints += 20
										match.player2.totalLoses += 1
										match.player1.saveData(True, True)
									else:
										match.lastWin = "player2"
										match.player2Score += 1
										match.player2.totalPoints += 30
										match.player2.totalWins += 1
										match.player1.totalPoints -= 20
										match.player1.totalLoses += 1
										match.player1.saveData(False, True)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN and (someoneWins == True or tie == True):		
					someoneWins = False
					rectsSelected = ["","","","","","","","",""]
					counter = 0
					tie = False
			if event.type == pygame.USEREVENT:
				counter += 0.100
		
		#BOT MOVEMENT
		if someoneWins == False and tie == False:
			if (match.nextTurn == 1 and match.player1.name == "Bot Triqui") or (match.nextTurn == 2 and match.player2.name == "Bot Triqui") :
				played = False
				while not played:
					num = random.randint(0, 8)
					if rectsSelected[num] == "":
						if match.nextTurn == 1:
							rectsSelected[num] = match.player1Symbol
							played = True
							match.nextTurn = 2
						else:
							rectsSelected[num] = match.player2Symbol
							played = True
							match.nextTurn = 1
				winner = match.verifyIfWinner(rectsSelected)
				if winner != None:
					winLine = winner[1]
					if winner == ("-", 0):
						tie = True
					elif winner[0] == "X":
						someoneWins = True
						if match.player1Symbol == "X":
							match.lastWin = "player1"
							match.player1Score += 1
							match.player1.totalPoints += 30
							match.player1.totalWins += 1
							match.player2.totalPoints += 20
							match.player2.totalLoses += 1
							match.player1.saveData(True, True)
						else:
							match.player2Score += 1
							match.lastWin = "player2"
							match.player2.totalPoints += 30
							match.player2.totalWins += 1
							match.player1.totalPoints -= 20
							match.player1.totalLoses += 1
							match.player1.saveData(False, True)
					elif winner[0] == "O":
						someoneWins = True
						if match.player1Symbol == "O":
							match.lastWin = "player1"
							match.player1Score += 1
							match.player1.totalPoints += 30
							match.player1.totalWins += 1
							match.player2.totalPoints += 20
							match.player2.totalLoses += 1
							match.player1.saveData(True, True)
						else:
							match.lastWin = "player2"
							match.player2Score += 1
							match.player2.totalPoints += 30
							match.player2.totalWins += 1
							match.player1.totalPoints -= 20
							match.player1.totalLoses += 1
							match.player1.saveData(False, True)
		
		surface.fill(WHITE)
		point = pygame.mouse.get_pos()


		#PAINT BOARD
		pygame.draw.line(surface, BLACK, (100, 400), (700, 400), 2)
		pygame.draw.line(surface, BLACK, (100, 600), (700, 600), 2)
		pygame.draw.line(surface, BLACK, (300, 200), (300, 800), 2)
		pygame.draw.line(surface, BLACK, (500, 200), (500, 800), 2)

		#PAINT NAMES & SCORE
		name1AndScore = font.render(match.player1Symbol + " - " + match.player1.name + ": " + str(match.player1Score), True, BLACK)
		name2AndScore = font.render(match.player2Symbol + " - " + match.player2.name + ": " + str(match.player2Score), True, BLACK)
		score = font.render("Puntuación", True, BLACK)
		surface.blit(score, (50,0))
		surface.blit(name1AndScore, (50,50))
		surface.blit(name2AndScore, (50,100))
		
		#NOONE WINS
		if someoneWins == False and tie == False:
			if match.nextTurn == 1 and match.player1Symbol == "X" or match.nextTurn == 2 and match.player2Symbol == "X":
				for i in range(len(rects)):
					if rectsSelected[i] == "":
						collide = rects[i].collidepoint(point)
						if collide:
							pygame.draw.line(surface, GREY, (rects[i].left + 10, rects[i].top + 10), (rects[i].left + rects[i].width - 10, rects[i].top + rects[i]. height - 10), width=5)
							pygame.draw.line(surface, GREY, (rects[i].left + 10, rects[i].top + rects[i].height - 10), (rects[i].left + rects[i].width - 10, rects[i].top + 10), width=5)

			if match.nextTurn == 1 and match.player1Symbol == "O" or match.nextTurn == 2 and match.player2Symbol == "O":
				for i in range(len(rects)):
					if rectsSelected[i] == "":
						collide = rects[i].collidepoint(point)
						if collide:
							pygame.draw.circle(surface, GREY, (rects[i].left + rects[i].width/2, rects[i].top + rects[i].height/2), rects[i].width/2 - 10, width=5)

			
			turnName = match.player1.name if match.nextTurn == 1 else match.player2.name
			if counter > 10:
				turnMessage = font.render("Turno de " + turnName + "  " + str(format(counter, ".1f")), True, RED)
			else:
				turnMessage = font.render("Turno de " + turnName + "  " + str(format(counter, ".1f")), True, BLACK)
			turnMessage_rect = turnMessage.get_rect(center=(SCREEN_WIDTH/2, 850))
			surface.blit(turnMessage, turnMessage_rect)

		#GAME SELECTIONS
		for i in range(len(rectsSelected)):
			if rectsSelected[i] == "X":
				pygame.draw.line(surface, BLACK, (rects[i].left + 10, rects[i].top + 10), (rects[i].left + rects[i].width - 10, rects[i].top + rects[i]. height - 10), width=5)
				pygame.draw.line(surface, BLACK, (rects[i].left + 10, rects[i].top + rects[i].height - 10), (rects[i].left + rects[i].width - 10, rects[i].top + 10), width=5)
			elif rectsSelected[i] == "O":
				pygame.draw.circle(surface, BLACK, (rects[i].left + rects[i].width/2, rects[i].top + rects[i].height/2), rects[i].width/2 - 10, width=5)

		if tie == True:
			tieMessage = fontWIN.render("EMPATE", True, RED)
			tieMessage_rect = tieMessage.get_rect(center=(SCREEN_WIDTH/2, 850))
			surface.blit(tieMessage, tieMessage_rect)
			continueMessage = font.render("PRESIONE ENTER PARA JUGAR OTRA VEZ", True, BLACK)
			continueMessage_rect = continueMessage.get_rect(center=(SCREEN_WIDTH/2, 950))
			surface.blit(continueMessage, continueMessage_rect)

		#PAINT IF SOMEONE WINS THE GAME
		if someoneWins == True:
			winnerName = match.player1.name if match.lastWin == "player1" else match.player2.name
			winnerMessage = fontWIN.render(winnerName + " GANO", True, BLACK)
			winnerMessage_rect = winnerMessage.get_rect(center=(SCREEN_WIDTH/2, 850))
			surface.blit(winnerMessage, winnerMessage_rect)
			continueMessage = font.render("PRESIONE ENTER PARA JUGAR OTRA VEZ", True, BLACK)
			continueMessage_rect = continueMessage.get_rect(center=(SCREEN_WIDTH/2, 950))
			surface.blit(continueMessage, continueMessage_rect)

			startRect = None
			endRect = None
			if winLine == 1:
				startRect = rect1
				endRect = rect3
			elif winLine == 2:
				startRect = rect4
				endRect = rect6
			elif winLine == 3:
				startRect = rect7
				endRect = rect9
			elif winLine == 4:
				startRect = rect1
				endRect = rect7
			elif winLine == 5:
				startRect = rect2
				endRect = rect8
			elif winLine == 6:
				startRect = rect3
				endRect = rect9
			elif winLine == 7:
				startRect = rect1
				endRect = rect9
			elif winLine == 8:
				startRect = rect3
				endRect = rect7
			pygame.draw.line(surface, RED, (startRect.left + startRect.width/2, startRect.top + startRect.height/2), (endRect.left + endRect.width/2, endRect.top + endRect.height/2), width=10)

		button("Inicio", 20, 950, 100, 30, BLUE, LIGHT_BLUE,20, surface, initWindow)

		pygame.display.update()

def initWindow():
	pygame.init()

	surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption("Inicio")
	fontBig = pygame.font.SysFont("ocraextended", 60)
	fontSmall = pygame.font.SysFont("timesnewroman", 20)
	running = True #Estado de la ventana

	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
				pygame.quit()
				sys.exit()

		surface.fill(WHITE)

		gameNameMessage = fontBig.render("TRIQUI", True, BLACK)
		gameNameMessage_rect = gameNameMessage.get_rect(center=(SCREEN_WIDTH/2, 50))
		surface.blit(gameNameMessage, gameNameMessage_rect)

		footerMessage = fontSmall.render("Hecho por Juan Pablo Castaño Tinoco", True, BLACK)
		surface.blit(footerMessage, (10,970))

		button("Jugador vs Jugador", 200, 200, 400, 100, BLUE, LIGHT_BLUE,30, surface, action=choseNameWindow)
		button("Jugador vs Bot", 200, 400, 400, 100, BLUE, LIGHT_BLUE,30, surface, action=choseNamePvsBotWindow)
		button("Puntuaciones", 200, 600, 400, 100, BLUE, LIGHT_BLUE,30, surface, action=scoreWindow)

		pygame.display.update()

def choseNameWindow():
	pygame.init()

	surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption("PvsP")
	fontBig = pygame.font.SysFont("ocraextended", 60)
	fontMedium = pygame.font.SysFont("ocraextended", 40)
	fontSmall = pygame.font.SysFont("ocraextended", 20)
	running = True #Estado de la ventana
	input_box1 = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 - 200, 100, 50)
	input_box2 = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 100, 100, 50)
	color_inactive = (193, 193, 193)
	color_active = BLACK
	color1 = color_inactive
	color2 = color_inactive
	active1 = False
	active2 = False
	text1 = 'Player 1'
	text2 = 'Player 2'
	name1 = ""
	name2 = ""

	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if active1:
					if event.key == pygame.K_BACKSPACE:
						text1 = text1[:-1]
					elif len(text1) < 9:
						text1 += event.unicode
				if active2:
					if event.key == pygame.K_BACKSPACE:
						text2 = text2[:-1]
					elif len(text2) < 9:
						text2 += event.unicode
			if event.type == pygame.MOUSEBUTTONDOWN:
				# If the user clicked on the input_box rect.
				if input_box1.collidepoint(event.pos):
					# Toggle the active variable.
					active1 = not active1
					if text1 == 'Player 1':
						text1=''
				else:
					active1 = False
				# Change the current color of the input box.
				color1 = color_active if active1 else color_inactive

				if input_box2.collidepoint(event.pos):
					# Toggle the active variable.
					active2 = not active2
					if text2 == 'Player 2':
						text2=''
				else:
					active2 = False
				# Change the current color of the input box.
				color2 = color_active if active2 else color_inactive

		surface.fill(WHITE)

		gameNameMessage = fontBig.render("TRIQUI", True, BLACK)
		gameNameMessage_rect = gameNameMessage.get_rect(center=(SCREEN_WIDTH/2, 50))
		surface.blit(gameNameMessage, gameNameMessage_rect)

		name1Message = fontSmall.render("Nombre jugador 1", True, BLACK)
		surface.blit(name1Message, (SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 - 230))

		name1Message = fontSmall.render("Nombre jugador 2", True, BLACK)
		surface.blit(name1Message, (SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 70))

		# Render the current text.
		txt_surface1 = fontMedium.render(text1, True, color1)
		# Resize the box if the text is too long.
		width1 = max(200, txt_surface1.get_width()+10)
		input_box1.w = width1
		# Blit the text.
		surface.blit(txt_surface1, (input_box1.x+5, input_box1.y+5))
		# Blit the input_box rect.
		pygame.draw.rect(surface, color1, input_box1, 2)

		# Render the current text.
		txt_surface2 = fontMedium.render(text2, True, color2)
		# Resize the box if the text is too long.
		width2 = max(200, txt_surface2.get_width() + 10)
		input_box2.w = width2
		# Blit the text.
		surface.blit(txt_surface2, (input_box2.x + 5, input_box2.y + 5))
		# Blit the input_box rect.
		pygame.draw.rect(surface, color2, input_box2, 2)

		name1 = text1 if text1 != '' else "Player 1"
		name2 = text2 if text2 != '' else "Player 2"
		player1 = Player(name1)
		player2 = Player(name2)
		match = MatchPvsP(player1,player2)
		button("JUGAR", 300, 800, 200, 50, BLUE, LIGHT_BLUE,30, surface, playerVsPlayerWindow, match)
		button("Inicio", 20, 950, 100, 30, BLUE, LIGHT_BLUE,20, surface, initWindow)

		pygame.display.update()

def choseNamePvsBotWindow():
	pygame.init()

	surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption("PvsBot")
	fontBig = pygame.font.SysFont("ocraextended", 60)
	fontMedium = pygame.font.SysFont("ocraextended", 40)
	fontSmall = pygame.font.SysFont("ocraextended", 20)
	running = True #Estado de la ventana
	input_box1 = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 - 200, 100, 50)
	color_inactive = (193, 193, 193)
	color_active = BLACK
	color1 = color_inactive
	active1 = False
	text1 = 'Player 1'
	name1 = ""

	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if active1:
					if event.key == pygame.K_BACKSPACE:
						text1 = text1[:-1]
					elif len(text1) < 9:
						text1 += event.unicode
			if event.type == pygame.MOUSEBUTTONDOWN:
				# If the user clicked on the input_box rect.
				if input_box1.collidepoint(event.pos):
					# Toggle the active variable.
					active1 = not active1
					if text1 == 'Player 1':
						text1=''
				else:
					active1 = False
				# Change the current color of the input box.
				color1 = color_active if active1 else color_inactive

		surface.fill(WHITE)

		gameNameMessage = fontBig.render("TRIQUI", True, BLACK)
		gameNameMessage_rect = gameNameMessage.get_rect(center=(SCREEN_WIDTH/2, 50))
		surface.blit(gameNameMessage, gameNameMessage_rect)

		name1Message = fontSmall.render("Nombre jugador", True, BLACK)
		surface.blit(name1Message, (SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 - 230))

		# Render the current text.
		txt_surface1 = fontMedium.render(text1, True, color1)
		# Resize the box if the text is too long.
		width1 = max(200, txt_surface1.get_width()+10)
		input_box1.w = width1
		# Blit the text.
		surface.blit(txt_surface1, (input_box1.x+5, input_box1.y+5))
		# Blit the input_box rect.
		pygame.draw.rect(surface, color1, input_box1, 2)

		name1 = text1 if text1 != '' else "Player 1"
		name2 = "Bot Triqui"
		player1 = Player(name1)
		player2 = Player(name2)
		match = MatchPvsP(player1,player2)
		button("JUGAR", 300, 800, 200, 50, BLUE, LIGHT_BLUE,30, surface, playerVsBotWindow, match)
		button("Inicio", 20, 950, 100, 30, BLUE, LIGHT_BLUE,20, surface, initWindow)

		pygame.display.update()

def scoreWindow():
	pygame.init()

	surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption("Puntuaciones")
	fontBig = pygame.font.SysFont("ocraextended", 60)
	fontMedium = pygame.font.SysFont("ocraextended", 40)
	fontSmall = pygame.font.SysFont("timesnewroman", 20)
	running = True #Estado de la ventana

	path = Path("data/playersData.json")
	topScores = []
	if path.exists():
		with open(path) as fp:
			data = json.load(fp)
			data.sort(key= lambda x:x["totalPoints"], reverse=True)
			for i in range(len(data)):
				if i < 10:
					topScores.append(data[i])
	else:
		with open(path, 'w') as f:
			json.dump([], f, ensure_ascii=False,indent=4)

	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
				pygame.quit()
				sys.exit()

		surface.fill(WHITE)

		gameNameMessage = fontBig.render("TOP PUNTUACIONES", True, BLACK)
		gameNameMessage_rect = gameNameMessage.get_rect(center=(SCREEN_WIDTH/2, 50))
		surface.blit(gameNameMessage, gameNameMessage_rect)

		nameHeader = fontMedium.render("NOMBRE", True, BLACK)
		scoreHeader = fontMedium.render("PUNTUACIÓN", True, BLACK)
		surface.blit(nameHeader, (100, 150))
		surface.blit(scoreHeader, (450, 150))

		for i in range(len(topScores)):
			playerName = fontSmall.render(topScores[i]["name"], True, BLACK)
			playerScore = fontSmall.render(str(topScores[i]["totalPoints"]), True, BLACK)
			surface.blit(playerName, (100, 200 + (i*50)))
			surface.blit(playerScore, (560, 200 + (i*50)))

		button("Inicio", 20, 950, 100, 30, BLUE, LIGHT_BLUE,20, surface, initWindow)

		pygame.display.update()

def button(msg,x,y,w,h,ic,ac, fontSize, gameDisplay, action=None, parameter=None):

	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if x+w > mouse[0] > x and y+h > mouse[1] > y:
		AAfilledRoundedRect(gameDisplay, (x,y,w,h), ac, 0.25)


		if click[0] == 1 and action != None:
			if parameter != None:
				action(parameter)
			else:
				action()
	else:
		AAfilledRoundedRect(gameDisplay, (x,y,w,h), ic, 0.25)

	smallText = pygame.font.SysFont("ocraextended", fontSize)
	textSurf, textRect = text_objects(msg, smallText)
	textRect.center = ( (x+(w/2)), (y+(h/2)) )
	gameDisplay.blit(textSurf, textRect)

def text_objects(text, font):
    textSurface = font.render(text, True, (255, 255, 255))
    return textSurface, textSurface.get_rect()

def AAfilledRoundedRect(surface,rect,color,radius=0.4):

    """
    AAfilledRoundedRect(surface,rect,color,radius=0.4)
    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """

    rect         = Rect(rect)
    color        = Color(*color)
    alpha        = color.a
    color.a      = 0
    pos          = rect.topleft
    rect.topleft = 0,0
    rectangle    = pygame.Surface(rect.size,SRCALPHA)

    circle       = pygame.Surface([min(rect.size)*3]*2,SRCALPHA)
    pygame.draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
    circle       = pygame.transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

    radius              = rectangle.blit(circle,(0,0))
    radius.bottomright  = rect.bottomright
    rectangle.blit(circle,radius)
    radius.topright     = rect.topright
    rectangle.blit(circle,radius)
    radius.bottomleft   = rect.bottomleft
    rectangle.blit(circle,radius)

    rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
    rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

    rectangle.fill(color,special_flags=BLEND_RGBA_MAX)
    rectangle.fill((255,255,255,alpha),special_flags=BLEND_RGBA_MIN)

    return surface.blit(rectangle,pos)


if __name__ == "__main__":
	initWindow()