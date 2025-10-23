import pygame
from box import Box
from cursors import uparrow_bm
from tkinter import Tk

# region Variables
FPS = 120

PRINT = False
SHOW_MOUSE_POS = False
SHOW_FPS = False

black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 25)
grey = (125, 125, 125)
light_grey = (200, 200, 200)
light_green = (173, 247, 193)
light_red = (242, 136, 136)
blue = (28, 2, 227)

# Finding monitor size
temproot = Tk()
temproot.withdraw()
resolution_x, resolution_y = temproot.winfo_screenwidth(), temproot.winfo_screenheight()

print(resolution_x, resolution_y)

screensize = resolution_y - 300
menu_size = resolution_y - screensize - 150 # choose (should be static?)
edge_buffer = 16 # choose
boxes_per_row = 8 # choose

box_buffer = None # calculated
box_size = None # calculated
mapsize = None # calculated

# endregion

# region Helper functions
def renderText(msg, font, fontsize, color, bgcolor, x, y, alignmentType, scrn):
    font = pygame.font.SysFont(font, fontsize, bold=True)
    helptext = font.render(msg, True, color, bgcolor)
    helptextrect = helptext.get_rect()
    match alignmentType:
        case "topleft":
            helptextrect.topleft = (x, y)
        case "topright":
            helptextrect.topright = (x, y)
        case "center":
            helptextrect.center = (x, y)
        case "bottomleft":
            helptextrect.bottomleft = (x, y)
        case "bottomright":
            helptextrect.bottomright = (x, y)
    scrn.blit(helptext, helptextrect)

def createScreenText(mouse_x, mouse_y, background, clock):
    if SHOW_MOUSE_POS:
        mousepostext = str(mouse_x) + ", " + str(mouse_y)
        mousepostextx, mousepostexty = (0, 0)
        renderText(mousepostext, "arial", 40, black, None, mousepostextx, mousepostexty, "topleft", background)

    if SHOW_FPS:
        fpstext = "fps: " + str(int(clock.get_fps()))
        fpstextx, fpstexty = (mapsize-edge_buffer, 0)
        renderText(fpstext, "arial", 28, black, None, fpstextx, fpstexty, "topright", background)
    pass

def drawPlacementRect(background, rect, color, alpha):
    rect_surf = pygame.Surface(pygame.Rect(rect).size)
    rect_surf.set_alpha(alpha)
    pygame.draw.rect(rect_surf, color, rect_surf.get_rect())
    background.blit(rect_surf, rect)

def makeAndDrawPlacementBox(valid_x, valid_y, mouse_x, mouse_y, all_objects):
    for vx in valid_x:
        closest_x = vx
        if vx > mouse_x - box_size:
            break

    for vy in valid_y:
        closest_y = vy
        if vy > mouse_y - box_size:
            break

    placement_box = pygame.Rect(closest_x, closest_y, box_size, box_size)
    all_objects["placementbox"] = placement_box
    all_objects["ActiveObjects"].append(placement_box)

    return placement_box

def addBox(valid_x, valid_y, mouse_x, mouse_y, all_objects):
    for vx in valid_x:
        closest_x = vx
        if vx > mouse_x - box_size:
            break

    for vy in valid_y:
        closest_y = vy
        if vy > mouse_y - box_size:
            break

    box = Box(1, closest_x, closest_y, box_size)
    if PRINT:
        print(box)

    all_objects["Boxes"].append(box)
    all_objects["ActiveObjects"].append(box)

    return box

def calculateMap(size, bpr, eb):
    eb_adj_size = size-(2*eb)

    notround = True
    bb_guess = 1
    while notround:
        boxsize_guess = (eb_adj_size-((bpr+1)*(bb_guess)))/bpr
        if boxsize_guess % 1 == 0:
            break
        bb_guess += 1
    
    return (int(eb_adj_size), int(bb_guess), int(boxsize_guess))

def getValidX(validx):
    x_iter = box_buffer
    
    limit = mapsize - 2*(box_buffer)
    
    while x_iter < limit:
        validx.append(x_iter)
        x_iter += box_size + box_buffer
    
def getValidY(validy):
    y_iter = box_buffer
    
    limit = mapsize - 2*(box_buffer)
    
    while y_iter < limit:
        validy.append(y_iter)
        y_iter += box_size + box_buffer

# endregion
        
mapsize, box_buffer, box_size = calculateMap(screensize, boxes_per_row, edge_buffer)

def main():
    # region Initialization
    pygame.init()

    screen = pygame.display.set_mode((screensize, screensize + menu_size))
    screen.fill(white)
    pygame.display.set_caption("Automation")  
    clock = pygame.time.Clock()

    # Make background
    background = pygame.Surface((mapsize, mapsize)).convert()
    background.fill(light_grey)

    # Initial blit
    screen.blit(background, (edge_buffer, edge_buffer))
    pygame.display.flip()

    # Create snap-to-grid ; defined by topleft of box
    valid_x = []
    valid_y = []

    getValidX(valid_x)
    getValidY(valid_y)
    
    # sanity check for map creation
    if not (len(valid_x) == len(valid_y)) or not(len(valid_x) == boxes_per_row):
        print("MAP ERROR")

    all_objects = {
        "Boxes": [],
        "ActiveObjects": [],
    }


    # Initialize game variables
    placeMode = True

    # endregion

    # Event loop
    while True:
        # Initial things
        clock.tick(FPS)
        background.fill(light_grey)

        # Set game states
        can_place_box = 1 # 0 = False, 1 = True, -1 = Out of Bounds

        # region --- LOGIC ---

        mouse_x = pygame.mouse.get_pos()[0] - edge_buffer
        mouse_y = pygame.mouse.get_pos()[1] - edge_buffer

        # Check placement box position
        if "placementbox" in all_objects:
            placementx = all_objects["placementbox"].x
            placementy = all_objects["placementbox"].y
            if placementx < 0 or placementx > (mapsize-box_size) or placementy < 0 or placementy > (mapsize-box_size):
                can_place_box = -1

        # Check if placement is colliding with a box
        for box in all_objects["Boxes"]:
            if box.rect.colliderect(all_objects["placementbox"]):
                can_place_box = 0
                break
        
        # endregion
            
        # region --- HANDLE EVENTS --- 
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_m:
                    if placeMode:
                        placeMode = False
                    else:
                        placeMode = True

            left_click, middle_click, right_click = pygame.mouse.get_pressed(num_buttons=3)

            # region In Placement mode
            if placeMode:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # No action if both clicks simultaneously
                    if left_click and right_click:
                        continue

                    # Left click = Place box
                    if left_click:
                        if can_place_box == 1:
                            addBox(valid_x, valid_y, mouse_x, mouse_y, all_objects)

                    # Right click = Delete box
                    elif right_click:
                        if (can_place_box == 0) and all_objects["Boxes"]:
                            collide_box = all_objects["placementbox"].collideobjects(all_objects["Boxes"])
                            all_objects["Boxes"].remove(collide_box)

            # endregion
                            
            # region In "M" mode    
            else:
                # Left click = upgrade box
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if left_click:
                        if (can_place_box == 0) and all_objects["Boxes"]:
                            collide_box = all_objects["placementbox"].collideobjects(all_objects["Boxes"])
                            collide_box.upgrade(background, grey)
            
            # endregion
                            
        # endregion

        # region --- CREATE VISUAL OBJECTS ---
        
        # Update cursor
        if placeMode:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        else:
            if can_place_box == 0:
                pygame.mouse.set_cursor(uparrow_bm)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)


        # Draw current boxes
        for box in all_objects["Boxes"]:
            box.draw(background, grey)

        # Draw placement box
        if placeMode:
            placement_box = makeAndDrawPlacementBox(valid_x, valid_y, mouse_x, mouse_y, all_objects)
            placement_box_color = light_green if can_place_box else light_red
            drawPlacementRect(background, placement_box, placement_box_color, 128)
        else:
            placement_box = makeAndDrawPlacementBox(valid_x, valid_y, mouse_x, mouse_y, all_objects)
            placement_box_color = blue
            drawPlacementRect(background, placement_box, placement_box_color, 128)

        # Draw text
        createScreenText(mouse_x, mouse_y, background, clock)

        # endregion

        # --- RENDER ---
        screen.blit(background, (edge_buffer, edge_buffer))
        pygame.display.flip()
       

if __name__ == '__main__': main()