import pygame
import json
import os
import time

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

DEFAULT_CONFIG = {
    "volume": 80,
    "keys": {
        "up": pygame.K_w,
        "down": pygame.K_s,
        "left": pygame.K_a,
        "right": pygame.K_d,
        "jump": pygame.K_SPACE,
        "fire": pygame.K_LCTRL
    }
}


def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Ensure keys exist
            if 'volume' not in data:
                data['volume'] = DEFAULT_CONFIG['volume']
            if 'keys' not in data:
                data['keys'] = DEFAULT_CONFIG['keys']
            return data
        except Exception:
            pass
    # Fallback default
    return DEFAULT_CONFIG.copy()


def save_config(cfg):
    try:
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def key_to_name(key):
    try:
        return pygame.key.name(key)
    except Exception:
        return str(key)


def draw_text_pixel(surface, text, font, color, pos, scale=3, center=False):
    # Render a small font then scale with nearest to emulate pixel font
    txt_s = font.render(text, False, color)
    if scale != 1:
        sw = txt_s.get_width() * scale
        sh = txt_s.get_height() * scale
        txt_s = pygame.transform.scale(txt_s, (sw, sh))
    r = txt_s.get_rect()
    if center:
        r.center = pos
    else:
        r.topleft = pos
    surface.blit(txt_s, r)
    return r


def open_config_menu():
    pygame.init()
    # Create fullscreen so it matches base menu style
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    # Colors
    DARK_BLUE = (10, 24, 58)
    GRAY = (100, 100, 110)
    CYAN = (56, 217, 222)
    LIGHT = (200, 220, 230)

    cfg = load_config()

    # Attempt to load background image to create pixelated/blurred effect
    bg = None
    try:
        bg_path = os.path.join(os.path.dirname(__file__), 'assets', 'menu', 'fondo.png')
        if os.path.exists(bg_path):
            bg = pygame.image.load(bg_path).convert()
            # Pixelate: scale down then up
            small = pygame.transform.scale(bg, (max(1, WIDTH // 40), max(1, HEIGHT // 40)))
            bg = pygame.transform.scale(small, (WIDTH, HEIGHT))
        else:
            bg = None
    except Exception:
        bg = None

    if bg is None:
        # Procedural subtle pattern
        bg = pygame.Surface((WIDTH, HEIGHT))
        bg.fill(DARK_BLUE)
        for i in range(0, WIDTH, 32):
            pygame.draw.rect(bg, (12, 30, 70), (i, 0, 16, HEIGHT), 1)

    # Fonts
    base_font = pygame.font.SysFont('dejavusansmono', 14)
    title_font = pygame.font.SysFont('dejavusansmono', 20)

    # Load click sound if exists
    click_sound = None
    try:
        click_path = os.path.join(os.path.dirname(__file__), 'assets', 'menu', 'click.wav')
        if os.path.exists(click_path):
            click_sound = pygame.mixer.Sound(click_path)
        else:
            # try common path
            alt = os.path.join(os.path.dirname(__file__), 'assets', 'musica', 'click.wav')
            if os.path.exists(alt):
                click_sound = pygame.mixer.Sound(alt)
    except Exception:
        click_sound = None

    def play_click():
        if click_sound:
            try:
                click_sound.play()
            except Exception:
                pass

    # UI state
    selection_index = 0
    panes = ['Volumen', 'Controles', 'Créditos', 'Volver']
    running = True
    anim_t = 0.0

    # Controls state
    listening = None  # None or key name (like 'up') when waiting

    # Fade in
    fade = 255
    fade_speed = 12

    while running:
        dt = clock.tick(60) / 1000.0
        anim_t += dt * 8.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if listening:
                    # Assign new key
                    cfg['keys'][listening] = event.key
                    save_config(cfg)
                    listening = None
                    play_click()
                else:
                    if event.key in (pygame.K_ESCAPE,):
                        # Exit menu
                        # fade out effect
                        for a in range(0, 260, fade_speed):
                            s = pygame.Surface((WIDTH, HEIGHT))
                            s.fill((0, 0, 0))
                            s.set_alpha(a)
                            screen.blit(bg, (0, 0))
                            screen.blit(s, (0, 0))
                            pygame.display.flip()
                            clock.tick(60)
                        running = False
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        play_click()
                        current = panes[selection_index]
                        if current == 'Volver':
                            running = False
                        elif current == 'Volumen':
                            # nothing to activate; left/right adjust
                            pass
                        elif current == 'Controles':
                            # select first control
                            listening = 'up'  # toggle to first; user must pick which to edit using mouse
                            listening = None
                        elif current == 'Créditos':
                            pass
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        selection_index = (selection_index - 1) % len(panes)
                        play_click()
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        selection_index = (selection_index + 1) % len(panes)
                        play_click()
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        if panes[selection_index] == 'Volumen':
                            cfg['volume'] = max(0, cfg.get('volume', 80) - 5)
                            pygame.mixer.music.set_volume(cfg['volume'] / 100.0)
                            save_config(cfg)
                            play_click()
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        if panes[selection_index] == 'Volumen':
                            cfg['volume'] = min(100, cfg.get('volume', 80) + 5)
                            pygame.mixer.music.set_volume(cfg['volume'] / 100.0)
                            save_config(cfg)
                            play_click()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                # compute button rectangles like below and detect clicks
                # We'll handle by computing positions each frame; mark clicks by setting actions
                if event.button == 1:
                    # We'll capture clicks in main loop using rects
                    pass

        # Draw background
        screen.blit(bg, (0, 0))

        # Draw panel
        panel_w = min(900, WIDTH - 200)
        panel_h = min(600, HEIGHT - 200)
        panel_x = (WIDTH - panel_w) // 2
        panel_y = (HEIGHT - panel_h) // 2

        # Panel background
        panel = pygame.Surface((panel_w, panel_h))
        panel.fill((20, 28, 48))
        # subtle border
        pygame.draw.rect(panel, (60, 70, 90), (0, 0, panel_w, panel_h), 4, border_radius=8)

        # Title
        draw_text_pixel(panel, 'CONFIGURACIÓN', title_font, CYAN, (panel_w // 2, 20), scale=3, center=True)

        # Draw menu options on left
        left_x = 40
        top_y = 90
        gap = 70
        option_rects = []
        for i, name in enumerate(panes):
            y = top_y + i * gap
            is_sel = (i == selection_index)
            # big button look
            btn_w = panel_w // 3
            btn_h = 56
            btn = pygame.Rect(left_x, y, btn_w, btn_h)
            color = GRAY if not is_sel else CYAN
            pygame.draw.rect(panel, (30, 36, 56), btn, border_radius=6)
            # border glow
            if is_sel:
                pygame.draw.rect(panel, color, btn.inflate(6, 6), 3, border_radius=10)
            draw_text_pixel(panel, name, base_font, LIGHT, (btn.centerx, btn.centery - 8), scale=2, center=True)
            option_rects.append((btn.move(panel_x, panel_y)))

        # Right side content
        content_x = panel_w // 3 + 80
        content_y = 80

        # Volume pane
        if panes[selection_index] == 'Volumen':
            draw_text_pixel(panel, 'Volumen general', base_font, LIGHT, (content_x, content_y), scale=2)
            vol = cfg.get('volume', 80)
            # Slider
            slider_w = panel_w - content_x - 60
            slider_h = 14
            sx = content_x
            sy = content_y + 50
            slider_rect = pygame.Rect(sx, sy, slider_w, slider_h)
            pygame.draw.rect(panel, (40, 48, 68), slider_rect, border_radius=6)
            filled_w = int((vol / 100.0) * slider_w)
            pygame.draw.rect(panel, CYAN, (sx, sy, filled_w, slider_h), border_radius=6)
            # Handle
            handle_x = sx + filled_w
            pygame.draw.rect(panel, LIGHT, (handle_x - 8, sy - 6, 16, slider_h + 12), border_radius=6)
            # Percentage
            draw_text_pixel(panel, f"{vol}%", base_font, LIGHT, (sx + slider_w + 10, sy - 6), scale=2)

            # Mouse handling for slider
            if pygame.mouse.get_pressed()[0]:
                mx, my = pygame.mouse.get_pos()
                # translate to panel coords
                px = mx - panel_x
                py = my - panel_y
                if slider_rect.collidepoint(px, py):
                    rel = (px - sx) / slider_w
                    rel = max(0.0, min(1.0, rel))
                    cfg['volume'] = int(rel * 100)
                    pygame.mixer.music.set_volume(cfg['volume'] / 100.0)
                    save_config(cfg)

        # Controls pane
        elif panes[selection_index] == 'Controles':
            draw_text_pixel(panel, 'Controles', base_font, LIGHT, (content_x, content_y), scale=2)
            keys = cfg.get('keys', DEFAULT_CONFIG['keys'])
            # Solo permitir reasignar: izquierda, derecha, salto y disparar
            ctrl_names = [('Izquierda', 'left'), ('Derecha', 'right'), ('Salto', 'jump'), ('Disparar', 'fire')]
            cy = content_y + 30
            irects = []
            for i, (label, keyid) in enumerate(ctrl_names):
                y = cy + i * 48
                draw_text_pixel(panel, label, base_font, LIGHT, (content_x, y), scale=2)
                # Obtener nombre de la tecla, soportando que cfg almacene ints
                raw_key = keys.get(keyid, DEFAULT_CONFIG['keys'].get(keyid))
                try:
                    key_name = key_to_name(int(raw_key))
                except Exception:
                    key_name = key_to_name(raw_key)
                btn_rect = pygame.Rect(content_x + 220, y - 8, 140, 34)
                pygame.draw.rect(panel, (28, 36, 48), btn_rect, border_radius=6)
                pygame.draw.rect(panel, CYAN, btn_rect, 2, border_radius=6)
                draw_text_pixel(panel, key_name.upper(), base_font, LIGHT, btn_rect.center, scale=2, center=True)
                irects.append((btn_rect.move(panel_x, panel_y), keyid))

            # Click detection for assigning
            if pygame.mouse.get_pressed()[0]:
                mx, my = pygame.mouse.get_pos()
                for r, kid in irects:
                    if r.collidepoint((mx, my)):
                        listening = kid
                        play_click()
                        time.sleep(0.12)  # debounce

            # If listening show prompt
            if listening:
                draw_text_pixel(panel, 'Presiona la nueva tecla...', base_font, CYAN, (content_x, cy + 300), scale=2)

        # Credits pane
        elif panes[selection_index] == 'Créditos':
            credits_text = 'Créditos: Álvarez, Gioffre y Mascia'
            # Caja sutil con texto más pequeño para que quepa cómodamente
            # Caja sutil con texto 50% más pequeño para que quepa cómodamente
            box_w = panel_w - (content_x + 160)
            box_h = 60
            box_x = content_x + 40
            box_y = (panel_h // 2) - (box_h // 2)
            pygame.draw.rect(panel, (18, 24, 36), (box_x, box_y, box_w, box_h), border_radius=8)
            pygame.draw.rect(panel, (60, 80, 100), (box_x, box_y, box_w, box_h), 2, border_radius=8)
            # Usar escala 1 (50% más pequeño que antes) para texto pixelado dentro del recuadro
            draw_text_pixel(panel, credits_text, base_font, CYAN, (box_x + box_w // 2, box_y + box_h // 2), scale=1, center=True)

        # Blit panel to screen
        screen.blit(panel, (panel_x, panel_y))

        # If listening for key mapping, show overlay
        if listening:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            draw_text_pixel(overlay, f'Presiona la nueva tecla para: {listening.upper()}', title_font, LIGHT, (WIDTH // 2, HEIGHT // 2), scale=3, center=True)
            screen.blit(overlay, (0, 0))

        # Fade-in
        if fade > 0:
            s = pygame.Surface((WIDTH, HEIGHT))
            s.fill((0, 0, 0))
            s.set_alpha(fade)
            screen.blit(s, (0, 0))
            fade = max(0, fade - fade_speed)

        pygame.display.flip()

    # Clean up and apply volume
    try:
        pygame.mixer.music.set_volume(cfg.get('volume', 80) / 100.0)
    except Exception:
        pass


if __name__ == '__main__':
    open_config_menu()