import random
import pygame
import sys
from pygame.locals import *

# Constants
FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 50
GAPSIZE = 10
BOARDWIDTH = 4
BOARDHEIGHT = 4
XMARGIN = (WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) // 2
YMARGIN = (WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) // 2

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
LIGHTBLUE = (173, 216, 230)
BGCOLOR = (60, 60, 100)
BOXCOLOR = (255, 255, 255)
HIGHLIGHTCOLOR = (255, 0, 0)

# Define card types (simple shapes for the game)
CARD_IMAGES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

# Initialize Pygame
pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Memory Puzzle Game')

# Game variables
first_card = None
second_card = None
cards = []

# Initialize the game
def initialize_game():
    global first_card, second_card, cards
    random.shuffle(CARD_IMAGES)
    cards = [CARD_IMAGES[i % len(CARD_IMAGES)] for i in range(BOARDWIDTH * BOARDHEIGHT)]
    random.shuffle(cards)
    first_card = None
    second_card = None

# Draws the board
def draw_board():
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            left, top = left_top_coords(x, y)
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            if revealed[x][y]:
                draw_card(x, y)
            else:
                draw_cover(x, y)

# Gets the pixel coordinates of a box on the board
def left_top_coords(boxx, boxy):
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return left, top

# Draw a card on the board
def draw_card(boxx, boxy):
    left, top = left_top_coords(boxx, boxy)
    font = pygame.font.Font(None, 40)
    text = font.render(cards[boxx + BOARDWIDTH * boxy], True, BLUE)
    text_rect = text.get_rect(center=(left + BOXSIZE // 2, top + BOXSIZE // 2))
    DISPLAYSURF.blit(text, text_rect)

# Draw the cover of the card (when it's not revealed)
def draw_cover(boxx, boxy):
    left, top = left_top_coords(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, LIGHTBLUE, (left, top, BOXSIZE, BOXSIZE))

# Handle user clicks
def handle_click(x, y):
    global first_card, second_card
    cardx, cardy = get_card_at_pixel(x, y)
    if cardx is None or cardy is None or revealed[cardx][cardy]:
        return
    revealed[cardx][cardy] = True
    if first_card is None:
        first_card = (cardx, cardy)
    elif second_card is None:
        second_card = (cardx, cardy)
        check_match()

# Gets the card at the pixel coordinates
def get_card_at_pixel(x, y):
    for cardx in range(BOARDWIDTH):
        for cardy in range(BOARDHEIGHT):
            left, top = left_top_coords(cardx, cardy)
            card_rect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if card_rect.collidepoint(x, y):
                return cardx, cardy
    return None, None

# Check if the two selected cards match
def check_match():
    global first_card, second_card
    x1, y1 = first_card
    x2, y2 = second_card
    if cards[x1 + BOARDWIDTH * y1] != cards[x2 + BOARDWIDTH * y2]:
        pygame.time.wait(500)
        revealed[x1][y1] = False
        revealed[x2][y2] = False
    first_card = None
    second_card = None

# Check if the game is won
def check_win():
    return all(revealed[x][y] for x in range(BOARDWIDTH) for y in range(BOARDHEIGHT))

# Main function to run the game
def main():
    global revealed
    revealed = [[False] * BOARDHEIGHT for _ in range(BOARDWIDTH)]

    initialize_game()
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        draw_board()

        if check_win():
            print("You won!")
            pygame.time.wait(1000)
            initialize_game()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                x, y = event.pos
                handle_click(x, y)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()
