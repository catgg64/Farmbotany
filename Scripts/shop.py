import pygame
from globals import *
import fbbutton

# Constants for shop and UI dimensions
SHOP_TILE_SIZE = 64
SHOP_SCALED_SIZE = 250
UI_WIDTH = 94
UI_HEIGHT = 94
UI_SCALED_WIDTH = 600
UI_SCALED_HEIGHT = 350
SHOP_TILE_POS = (0, 2944)
UI_TILE_POS = (2848, 16)
BORDER_COLOR = (255, 255, 255)
BORDER_WIDTH = 5

class Shop:
    """A class representing a shop in the game that can be interacted with."""
    def __init__(self, pos_x: int, pos_y: int, floutwitch):
        """Initialize the shop with position and floutwitch reference."""
        self.image = self._load_image()
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.floutwitch = floutwitch
        self.shop_open = False
        self.shop_ui = ShopUI(100, 100)
        self.exit_button = fbbutton.FBButton(150, 150, 100, 50, "Exit")
        self.buy_button = fbbutton.FBButton(200, 250, 100, 50, "Buy")
        self.mouse_realeased = False

    def _load_image(self) -> pygame.Surface:
        """Load and prepare the shop image."""
        try:
            image = pygame.image.load("Sprites/tile_set.png")
            subsurface_rect = pygame.Rect(SHOP_TILE_POS, (SHOP_TILE_SIZE, SHOP_TILE_SIZE))
            image = image.subsurface(subsurface_rect)
            return pygame.transform.scale(image, (SHOP_SCALED_SIZE, SHOP_SCALED_SIZE))
        except pygame.error as e:
            print(f"Error loading shop image: {e}")
            raise

    def update(self, surface: pygame.Surface, screen: pygame.Surface, mouse_realeased) -> None:
        """Update shop state and render it."""
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, BORDER_COLOR, self.rect, BORDER_WIDTH)
        
        """Updates the check of the mouse realsed"""
        self.mouse_realeased = mouse_realeased

        # Check collision only if shop is not already open
        if not self.shop_open and self.rect.colliderect(self.floutwitch.rect) and self.floutwitch.is_walking:
            self._open_shop()
        elif self.shop_open and not self.rect.colliderect(self.floutwitch.rect):
            self._close_shop()
        


    def update_shop_ui(self, screen: pygame.Surface) -> None:
        """Update and render the shop UI if visible."""
        self.shop_ui.update(screen)
                
        if self.shop_open:
            self.exit_button.update(screen, (255, 154, 46), (200, 105, 1), (161, 83, 0), self.mouse_realeased)
            self.buy_button.update(screen, (255, 154, 46), (200, 105, 1), (161, 83, 0), self.mouse_realeased)

            if self.exit_button.state == "pressed" and self.state == "menu":
                self._close_shop()
            if self.buy_button.state == "pressed":
                self._open_buy_menu()

    def _open_shop(self) -> None:
        """Open the shop and update related states."""
        self.shop_open = True
        print('Shop opened')
        self.floutwitch.can_move = False
        self.shop_ui.visibility = True

    def _close_shop(self) -> None:
        """Close the shop and update related states."""
        self.shop_open = False
        print('Shop closed')
        self.floutwitch.can_move = True
        self.shop_ui.visibility = False

    def _open_buy_menu(self):
        print("opend buy menu")

    def _close_buy_menu(self):
        print("close buy menu")


class ShopUI:
    """A class representing the shop's user interface."""
    def __init__(self, pos_x: int, pos_y: int):
        """Initialize the shop UI with position."""
        self.image = self._load_image()
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
        self.visibility = False  # Default to hidden
        self.status = "menu"

    def _load_image(self) -> pygame.Surface:
        """Load and prepare the shop UI image."""
        try:
            image = pygame.image.load("Sprites/tile_set.png")
            subsurface_rect = pygame.Rect(UI_TILE_POS, (UI_WIDTH, UI_HEIGHT))
            image = image.subsurface(subsurface_rect)
            return pygame.transform.scale(image, (UI_SCALED_WIDTH, UI_SCALED_HEIGHT))
        except pygame.error as e:
            print(f"Error loading shop UI image: {e}")
            raise

    def update(self, internal_surface: pygame.Surface) -> None:
        """Render the shop UI if visible."""
        if self.visibility:
            internal_surface.blit(self.image, self.rect)