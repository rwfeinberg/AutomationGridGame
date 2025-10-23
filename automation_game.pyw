import pygame
from box import Box

# Variables
FPS = 120

PRINT = False

black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 25)
grey = (125, 125, 125)
light_grey = (200, 200, 200)
light_green = (173, 247, 193)
light_red = (242, 136, 136)

screensize = 800 # choose
edge_buffer = 16 # choose
boxes_per_row = 8 # choose

box_buffer = None # calculated
box_size = None # calculated
mapsize = None # calculated

# Helper functions
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
    # mousepostext = str(mouse_x) + ", " + str(mouse_y)
    # mousepostextx, mousepostexty = (0, 0)
    # renderText(mousepostext, "arial", 40, black, None, mousepostextx, mousepostexty, "topleft", background)

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
    
mapsize, box_buffer, box_size = calculateMap(screensize, boxes_per_row, edge_buffer)

def main():
    # Initialize
    pygame.init()

    screen = pygame.display.set_mode((screensize, screensize))
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

    placeMode = True

    # Event loop
    while True:
        # Initial things
        clock.tick(FPS)
        background.fill(light_grey)

        # Initialize game variables
        can_place_box = True

        # --- LOGIC ---

        mouse_x = pygame.mouse.get_pos()[0] - edge_buffer
        mouse_y = pygame.mouse.get_pos()[1] - edge_buffer

        # Check if placement is out of bounds
        if placeMode:
            if "placementbox" in all_objects:
                placementx = all_objects["placementbox"].x
                placementy = all_objects["placementbox"].y
                if placementx < 0 or placementx > (mapsize-box_size) or placementy < 0 or placementy > (mapsize-box_size):
                    can_place_box = False

            # Check if placement is colliding with a box
            for box in all_objects["Boxes"]:
                if box.rect.colliderect(all_objects["placementbox"]):
                    can_place_box = False
                    break

        # --- HANDLE EVENTS --- 

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

            # In Placement mode
            if placeMode:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if left_click and right_click:
                        continue

                    # Place box
                    if left_click:
                        if can_place_box:
                            addBox(valid_x, valid_y, mouse_x, mouse_y, all_objects)

                    # Delete box
                    elif right_click:
                        if not can_place_box and all_objects["Boxes"]:
                            collide_index = all_objects["placementbox"].collidelist(all_objects["Boxes"])
                            all_objects["Boxes"].pop(collide_index)

            # In "M" mode    
            else:
                pass

        # --- CREATE VISUAL OBJECTS ---
        
        # Draw current boxes
        for box in all_objects["Boxes"]:
            box.draw(background, grey)

        # Draw placement box
        if placeMode:
            placement_box = makeAndDrawPlacementBox(valid_x, valid_y, mouse_x, mouse_y, all_objects)
            placement_box_color = light_green if can_place_box else light_red
            drawPlacementRect(background, placement_box, placement_box_color, 128)

        # Draw text
        createScreenText(mouse_x, mouse_y, background, clock)

        # --- RENDER ---
        
        screen.blit(background, (edge_buffer, edge_buffer))

        pygame.display.flip()
       

if __name__ == '__main__': main()