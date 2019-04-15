import datetime
import picamera
import pygame
import io


# Init pygame
pygame.init()
screen = pygame.display.set_mode((0, 0))

# Init camera
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.crop = (0.0, 0.0, 1.0, 1.0)
camera.vflip = True

x = (screen.get_width() - camera.resolution[0]) / 2
y = (screen.get_height() - camera.resolution[1]) / 2

# Init buffer
rgb = bytearray(camera.resolution[0] * camera.resolution[1] * 3)

preview_button_pressed = False

header_font = pygame.font.SysFont(None, 70)
instructions_font = pygame.font.SysFont(None, 40)

###background###
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

###background image###
background_image_rect = pygame.Rect((0,0),(screen.get_width(), screen.get_height()))
background_image = pygame.image.load('ale_ric.jpg')
background_image = pygame.transform.scale(background_image, background_image_rect.size)
background_image = background_image.convert()

###all the texts###
header = header_font.render('Alessandra + Riccardo', True, (190, 190, 190))
instructions_first_line = instructions_font.render('Per fare una foto', True, (255, 0, 0))
instructions_second_line = instructions_font.render('Premere il pulsante giallo', True, (0, 255, 0))
instructions_third_line = instructions_font.render('Aspettare la preview', True, (0, 0, 255))
instructions_fourth_line = instructions_font.render('Premere il pulsante verde', True, (0, 255, 0))

###wrapping texts in rects### 
headerpos = header.get_rect()
instructions_first_line_pos = instructions_first_line.get_rect()
instructions_second_line_pos = instructions_second_line.get_rect()
instructions_third_line_pos = instructions_third_line.get_rect()
instructions_fourth_line_pos = instructions_fourth_line.get_rect()

###setting texts positions###
headerpos.centerx = background.get_rect().centerx
instructions_first_line_pos.centerx = background.get_rect().centerx
instructions_first_line_pos.y = 60
instructions_second_line_pos.centerx = background.get_rect().centerx
instructions_second_line_pos.y = 100
instructions_third_line_pos.centerx = background.get_rect().centerx
instructions_third_line_pos.y = 140
instructions_fourth_line_pos.centerx = background.get_rect().centerx
instructions_fourth_line_pos.y = 180

###blit all to background###
background.blit(background_image, background_image_rect)
background.blit(header, headerpos)
background.blit(instructions_first_line, instructions_first_line_pos)
background.blit(instructions_second_line, instructions_second_line_pos)
background.blit(instructions_third_line, instructions_third_line_pos)
background.blit(instructions_fourth_line, instructions_fourth_line_pos)


def preview():
    stream = io.BytesIO()
    camera.capture(stream, use_video_port=True, format='rgb')
    stream.seek(0)
    stream.readinto(rgb)
    stream.close()
    img = pygame.image.frombuffer(rgb[0:
          (camera.resolution[0] * camera.resolution[1] * 3)],
           camera.resolution, 'RGB')

    screen.fill(0)
    if img:
        screen.blit(img, (x, y))

def show_interface():
    #background = pygame.Surface.(screen.get_size())
    #background = background.convert()
    #background.fill((250, 250, 250))
	
    #text = font.render('Waiting for tap', True, (190, 190, 190))
    #background.blit(text, textpos)
    screen.blit(background, (0, 0))

def _create_file_name(timestamp):
    return str(timestamp).replace(' ', '') + '.jpeg'

# Main loop
exitFlag = True
while exitFlag:
    for event in pygame.event.get():
        #if event.type is pygame.MOUSEBUTTONDOWN:
        #    filename = _create_file_name(datetime.datetime.now())
        #    camera.capture(filename)
	if event.type is pygame.KEYDOWN:
	    if event.key == pygame.K_SPACE:
	      preview_button_pressed = True
	    if event.key == pygame.K_RETURN:
	      if preview_button_pressed == True:
	        filename = _create_file_name(datetime.datetime.now())
                camera.capture(filename)
	        preview_button_pressed = False


        if event.type is pygame.QUIT:
                exitFlag = False

    if preview_button_pressed:
        preview()
    else:
        show_interface()

    pygame.display.update()

camera.close()
pygame.display.quit()
