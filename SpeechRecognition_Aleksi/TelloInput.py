import pygame

# Initialize pygame library
def init():
    pygame.init()
    # Set control display size as 400*400 pixels
    windows = pygame.display.set_mode((400, 400))

if __name__=='__main__':
    init()
    while True:
        main()