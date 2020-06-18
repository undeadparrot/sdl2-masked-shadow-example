import ctypes
import sys

import sdl2.ext
import sdl2.sdlimage
from sdl2 import (
    SDL_LoadBMP,
    SDL_QUIT,
    SDL_DestroyWindow,
    SDL_Quit,
    SDL_PollEvent,
    SDL_Event,
    SDL_CreateWindow,
    SDL_WINDOWPOS_CENTERED,
    SDL_WINDOW_SHOWN,
    SDL_GetWindowSurface,
    SDL_BlitSurface,
    SDL_UpdateWindowSurface,
    SDL_FreeSurface,
    SDL_CreateRGBSurface,
    SDL_Rect,
    SDL_BlitScaled,
    SDL_KEYDOWN, SDL_RenderClear, SDL_FillRect)

WIDTH = 90
HEIGHT = 90
SCALE = 5
BACKGROUND_COLOR = 0x151530

def main():
    window = sdl2.ext.Window("Hello World!", size=(640, 480))
    window.show()

    window = SDL_CreateWindow(
        b"Hello World",
        SDL_WINDOWPOS_CENTERED,
        SDL_WINDOWPOS_CENTERED,
        WIDTH * SCALE,
        HEIGHT * SCALE,
        SDL_WINDOW_SHOWN,
    )
    window_surface = SDL_GetWindowSurface(window)

    game_surface = SDL_CreateRGBSurface(0, WIDTH, HEIGHT, 32, 0, 0, 0, 0)
    temp_surface = SDL_CreateRGBSurface(0, WIDTH, HEIGHT, 32, 0, 0, 0, 0)

    images = {
        "link-right": SDL_LoadBMP(b"link-right.bmp"),
        "flame": SDL_LoadBMP(b"flame.bmp"),
        "link-right-alpha": sdl2.sdlimage.IMG_Load(b"link-right.png"),
        "overlay-alpha": sdl2.sdlimage.IMG_Load(b"overlay.png")
    }

    window_rect = SDL_Rect(0, 0, WIDTH * SCALE, HEIGHT * SCALE)
    game_rect = SDL_Rect(0, 0, WIDTH, HEIGHT)
    temp_rect = SDL_Rect(0, 0, WIDTH, HEIGHT)

    link_x = 0
    flame_x = 20
    flame_y = 20
    flame_w = 16
    flame_h = 16
    overlay_x = flame_x + (flame_w//2) - 25
    overlay_y = flame_y + (flame_h//2) - 25

    def draw():
        # clear the surface
        SDL_FillRect(game_surface, game_rect, BACKGROUND_COLOR)

        # blit Link
        target = SDL_Rect(link_x, link_x, 16, 16)
        SDL_BlitSurface(images["link-right"], None, game_surface, target)

        # blit flame
        target = SDL_Rect(flame_x, flame_y, 16, 16)
        SDL_BlitSurface(images["flame"], None, game_surface, target)

        # blit overlay
        target = SDL_Rect(overlay_x, overlay_y, 50, 50)
        SDL_BlitSurface(images["overlay-alpha"], None, game_surface, target)

        # blit surface onto screen, scaled up
        SDL_BlitScaled(game_surface, game_rect, window_surface, window_rect)
        SDL_UpdateWindowSurface(window)

    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == SDL_QUIT:
                running = False
                break
            elif event.type == SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_RIGHT:
                    link_x += 1
        sdl2.SDL_Delay(10)
        draw()

    for image in images.values():
        SDL_FreeSurface(image)

    SDL_DestroyWindow(window)
    SDL_Quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
