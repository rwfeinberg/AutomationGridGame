import pygame
from box import Box
from cursors import uparrow_bm
from tkinter import Tk
from button import Button

# region Variables
FPS = 120

BOX_UPDATE_TIME = 1000 # in ms

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

screensize = resolution_y - 500
menu_size = resolution_y - screensize - 400 # choose (should be static?)
top_size = 80
edge_buffer = 16 # choose
boxes_per_row = 8 # choose

x_offset = edge_buffer # from left, adjust if necessary
y_offset = edge_buffer + top_size # from top, adjust if necessary

box_buffer = None # calculated
box_size = None # calculated
mapsize = None # calculated

# endregion



# region Helper functions
def renderText(msg, font, fontsize, color, bgcolor, x, y, alignmentType, scrn):
    font = pygame.font.Font(font, fontsize)
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
        renderText(mousepostext, "arial.ttf", 40, black, None, mousepostextx, mousepostexty, "topleft", background)

    if SHOW_FPS:
        fpstext = "fps: " + str(int(clock.get_fps()))
        fpstextx, fpstexty = (mapsize-edge_buffer, 0)
        renderText(fpstext, "arial.ttf", 28, black, None, fpstextx, fpstexty, "topright", background)

def drawPlacementRect(background, rect, color, alpha):
    placement_surf = pygame.Surface(rect.size)
    placement_surf.set_alpha(alpha)
    placement_surf.fill(color)
    background.blit(placement_surf, rect)

def makePlacementBox(valid_x, valid_y, mouse_x, mouse_y, all_objects):
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

def buttonFunction():
    print("Click")

# endregion
        
mapsize, box_buffer, box_size = calculateMap(screensize, boxes_per_row, edge_buffer)

def main():
    # region Initialization
    pygame.init()

    screen = pygame.display.set_mode((screensize, top_size + screensize + menu_size))
    screen.fill(white)
    pygame.display.set_caption("Automation")  
    clock = pygame.time.Clock()

    # Make background
    background = pygame.Surface((mapsize, mapsize)).convert()
    background.fill(light_grey)

    # Initial blit
    screen.blit(background, (x_offset, y_offset))
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
        "Buttons": []
    }


    # Initialize game variables
    placeMode = True

    # Events
    box_update_event = pygame.USEREVENT + 1
    pygame.time.set_timer(box_update_event, BOX_UPDATE_TIME)

    # Make buttons
    testButton = Button(edge_buffer, mapsize+edge_buffer+y_offset, (200, 75), buttonFunction, "Test", 36, [grey, black], hold=False)
    all_objects["Buttons"].append(testButton)

    # Set Score
    score = 0

    # endregion

    # Event loop
    while True:
        # Initial things
        clock.tick(FPS)
        background.fill(light_grey)

        # Set game states
        placement_state = 1 # 0 = Box Collision, 1 = Open Square, -1 = Out of Bounds

        # region --- LOGIC ---

        mouse_x = pygame.mouse.get_pos()[0] - x_offset
        mouse_y = pygame.mouse.get_pos()[1] - y_offset

        # If out of bounds, remove placementbox
        if (mouse_x < 0) or (mouse_x > mapsize) or (mouse_y < 0) or (mouse_y > mapsize):
            placement_state = -1
            if "placementbox" in all_objects:
                all_objects.pop("placementbox")
        
        # If in bounds, make placementBox
        if not placement_state == -1:
            makePlacementBox(valid_x, valid_y, mouse_x, mouse_y, all_objects)

        # Check if placement box is over a box
        if "placementbox" in all_objects:
            for box in all_objects["Boxes"]:
                if box.rect.colliderect(all_objects["placementbox"]):
                    placement_state = 0
                    break
        
        # Update cursor
        if placeMode:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        else:
            if placement_state == 0:
                pygame.mouse.set_cursor(uparrow_bm)
            elif placement_state == -1:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)

        # Process buttons
        for button in all_objects["Buttons"]:
            button.update()
        
        # endregion
            
        # region --- HANDLE EVENTS --- 
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            # Read key presses
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_m:
                    if placeMode:
                        placeMode = False
                    else:
                        placeMode = True

            # Update boxes event
            elif event.type == box_update_event:
                # Update Boxes
                for box in all_objects["Boxes"]:
                    box_add = box.update()
                    score += box_add

            

            left_click, middle_click, right_click = pygame.mouse.get_pressed(num_buttons=3)

            # region In Placement mode
            if placeMode:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # No action if both clicks simultaneously
                    if left_click and right_click:
                        continue

                    # Left click = Place box
                    if left_click:
                        if placement_state == 1:
                            addBox(valid_x, valid_y, mouse_x, mouse_y, all_objects)

                    # Right click = Delete box
                    elif right_click:
                        if (placement_state == 0) and all_objects["Boxes"]:
                            collide_box = all_objects["placementbox"].collideobjects(all_objects["Boxes"])
                            all_objects["Boxes"].remove(collide_box)

            # endregion
                            
            # region In "M" mode    
            else:
                if left_click and right_click:
                        continue
                # Left click = upgrade box
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if left_click:
                        if (placement_state == 0) and all_objects["Boxes"]:
                            collide_box = all_objects["placementbox"].collideobjects(all_objects["Boxes"])
                            collide_box.upgrade(background, grey)
            
            # endregion
                            
        # endregion

        # region --- CREATE VISUAL OBJECTS ---

        screen.fill(white)

        # Draw current boxes
        for box in all_objects["Boxes"]:
            box.draw(background, grey)

        # Draw buttons
        for button in all_objects["Buttons"]:
            button.draw(screen)

        # Draw placement box
        if "placementbox" in all_objects:
            if placeMode:
                placement_box_color = light_green if placement_state else light_red
                drawPlacementRect(background, all_objects["placementbox"], placement_box_color, 128)
            else:
                placement_box_color = blue
                drawPlacementRect(background, all_objects["placementbox"], placement_box_color, 128)

        # Draw text
        createScreenText(mouse_x, mouse_y, background, clock)

        renderText(f"Score: {score}", "Futura Bold.otf", 40, black, None, screensize//2, 20, "center", screen)

        # endregion

        # --- RENDER ---
        screen.blit(background, (x_offset, y_offset))
        pygame.display.flip()
       

if __name__ == '__main__': main()