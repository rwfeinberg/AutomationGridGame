import pygame

thickarrow_strings = (
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

thickarrow_bm = pygame.cursors.Cursor(
    (24, 24), (0, 0), *pygame.cursors.compile(thickarrow_strings, black='x', white='.')
)