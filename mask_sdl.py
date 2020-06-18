import sys

import sdl2.blendmode
import sdl2.ext
import sdl2.sdlimage
from sdl2 import (SDL_BLENDMODE_BLEND, SDL_ComposeCustomBlendMode, SDL_CreateTexture,
                  SDL_CreateTextureFromSurface, SDL_FreeSurface, SDL_KEYDOWN, SDL_LoadBMP,
                  SDL_PIXELFORMAT_RGBA8888, SDL_QUIT, SDL_Quit, SDL_Rect, SDL_RenderClear,
                  SDL_RenderCopy, SDL_RenderPresent, SDL_SetRenderDrawColor, SDL_SetRenderTarget,
                  SDL_SetTextureBlendMode, SDL_TEXTUREACCESS_TARGET)

WIDTH = 90
HEIGHT = 90
SCALE = 5
BACKGROUND_COLOR = 0x151530
OVERLAY_SIZE = 90


def main():
    window = sdl2.ext.Window("Hello World", size=(WIDTH * SCALE, HEIGHT * SCALE))
    window.show()
    renderer = sdl2.ext.Renderer(window)
    game_tex = SDL_CreateTexture(
        renderer.sdlrenderer,
        SDL_PIXELFORMAT_RGBA8888,
        SDL_TEXTUREACCESS_TARGET,
        WIDTH,
        HEIGHT,
    )
    temp_tex = SDL_CreateTexture(
        renderer.sdlrenderer,
        SDL_PIXELFORMAT_RGBA8888,
        SDL_TEXTUREACCESS_TARGET,
        WIDTH,
        HEIGHT,
    )

    blendmode = SDL_ComposeCustomBlendMode(
        # src col factor
        sdl2.blendmode.SDL_BLENDFACTOR_ONE,
        # dst col factor
        sdl2.blendmode.SDL_BLENDFACTOR_ONE,
        # color operation
        sdl2.blendmode.SDL_BLENDOPERATION_SUBTRACT,
        # src alpha factor
        sdl2.blendmode.SDL_BLENDFACTOR_SRC_ALPHA,
        # dst alpha factor
        sdl2.blendmode.SDL_BLENDFACTOR_ZERO,
        # alpha operation
        sdl2.blendmode.SDL_BLENDOPERATION_ADD,
    )

    surfaces = {
        "link-right": SDL_LoadBMP(b"link-right.bmp"),
        "flame": SDL_LoadBMP(b"flame.bmp"),
        "overlay": sdl2.sdlimage.IMG_Load(b"overlay.png"),
    }

    images = {
        key: SDL_CreateTextureFromSurface(renderer.sdlrenderer, img)
        for key, img in surfaces.items()
    }

    link_x = 3
    flame_x = 20
    flame_y = 20
    flame_w = 16
    flame_h = 16

    def draw():
        # clear the surface
        SDL_RenderClear(renderer.sdlrenderer)

        # start rendering to the temporary texture
        # which will contain Link with a shadow
        SDL_SetRenderTarget(renderer.sdlrenderer, temp_tex)
        # with a transparent background
        SDL_SetRenderDrawColor(renderer.sdlrenderer, 0, 0, 0, 0)
        SDL_RenderClear(renderer.sdlrenderer)

        # blit overlay to temp texture
        link_target = SDL_Rect(link_x, link_x, 16, 16)
        overlay_target = SDL_Rect(flame_x + link_x, flame_y + link_x, 16, 16)
        SDL_RenderCopy(
            renderer.sdlrenderer, images["overlay"], overlay_target, link_target
        )

        # blit Link to temp texture,
        # using his own alpha but subtracting colour from the overlay
        link_target = SDL_Rect(link_x, link_x, 16, 16)
        SDL_SetTextureBlendMode(images["link-right"], blendmode)
        SDL_RenderCopy(renderer.sdlrenderer, images["link-right"], None, link_target)

        # render to the game map
        SDL_SetRenderTarget(renderer.sdlrenderer, game_tex)
        # with a gloomy red backdrop
        SDL_SetRenderDrawColor(renderer.sdlrenderer, 30, 20, 25, 255)
        SDL_RenderClear(renderer.sdlrenderer)

        # draw the bonfire
        target = SDL_Rect(flame_x, flame_y, flame_w, flame_h)
        SDL_RenderCopy(renderer.sdlrenderer, images["flame"], None, target)

        # draw the game map to the screen, scaled up
        SDL_SetTextureBlendMode(temp_tex, SDL_BLENDMODE_BLEND)
        SDL_RenderCopy(renderer.sdlrenderer, temp_tex, None, None)

        # blit surface onto screen, scaled up
        SDL_SetRenderTarget(renderer.sdlrenderer, None)
        SDL_RenderCopy(renderer.sdlrenderer, game_tex, None, None)

        SDL_RenderPresent(renderer.sdlrenderer)

        window.refresh()

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

    for image in surfaces.values():
        SDL_FreeSurface(image)

    window.close()
    SDL_Quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
