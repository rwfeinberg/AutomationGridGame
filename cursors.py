import pygame

uparrow = (
  "           xx           ",
  "          x..x          ",
  "         x....x         ",
  "        x......x        ",
  "       x........x       ",
  "      x..........x      ",
  "     x............x     ",
  "    x..............x    ",
  "   x................x   ",
  "  x..................x  ",
  " x....................x ",
  "xxxxxxxx........xxxxxxxx",
  "       x........x       ",
  "       x........x       ",
  "       x........x       ",
  "       x........x       ",
  "       x........x       ",
  "       x........x       ",
  "       x........x       ",
  "       x........x       ",
  "       x........x       ",
  "       xxxxxxxxxx       ",
  "                        ",
  "                        ")

uparrow_bm = pygame.cursors.Cursor(
    (24, 24), (0, 0), *pygame.cursors.compile(uparrow, black='x', white='.')
)