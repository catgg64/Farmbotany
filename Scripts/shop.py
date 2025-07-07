import pygame
from globals import *
import fbbutton
import inventorymanager

# Remove this import
# import farmbotany

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
    def __init__(self, pos_x: int, pos_y: int, floutwitch, check_slot_interaction_func=None):
        self.image = self._load_image()
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.floutwitch = floutwitch
        self.shop_open = False
        self.shop_ui = ShopUI(100, 100)
        self.exit_button = fbbutton.FBButton(150, 150, 100, 50, "Exit")
        self.buy_button = fbbutton.FBButton(200, 250, 100, 50, "Buy")
        self.exit_buy_menu_button = fbbutton.FBButton(150, 150, 100, 50, "Back")
        self.sell_button = fbbutton.FBButton(550, 250, 100, 50, "Sell")
        self.exit_sell_menu_button = fbbutton.FBButton(150, 150, 100, 50, "Back")
        self.sell_slot_data = inventorymanager.ItemData("1", 0)
        self.sell_slot_data_list = [self.sell_slot_data]
        self.sell_slot_list = []
        self.sell_slot = inventorymanager.Slot(self.sell_slot_data.id, 1, self.sell_slot_data.quantity, 400, 200, self.sell_slot_list, 64)
        self.mouse_realeased = False
        # Store the function for slot interaction
        self.check_slot_interaction_func = check_slot_interaction_func

    # ... other methods unchanged until update_shop_ui ...

    def update_shop_ui(self, screen: pygame.Surface) -> None:
        self.shop_ui.update(screen)
        if self.shop_open:
            self.exit_button.update(screen, (255, 154, 46), (200, 105, 1), (161, 83, 0), self.mouse_realeased)
            if self.shop_ui.status == "menu":
                self.buy_button.update(screen, (255, 154, 46), (200, 105, 1), (161, 83, 0), self.mouse_realeased)
                self.sell_button.update(screen, (255, 154, 46), (200, 105, 1), (161, 83, 0), self.mouse_realeased)
            if self.shop_ui.status == "buy_menu":
                self.exit_buy_menu_button.update(screen, (255, 154, 46), (200, 105, 1), (161, 83, 0), self.mouse_realeased)

            if self.shop_ui.status == "sell_menu":
                self.exit_sell_menu_button.update(screen, (255, 154, 46), (200, 105, 1), (161, 83, 0), self.mouse_realeased)
                inventorymanager.update_inventory(self.sell_slot_data_list, screen, self.sell_slot_list, 64, 0, 0, 0, 64)
                # Use the passed function instead of importing farmbotany
                if self.check_slot_interaction_func:
                    self.check_slot_interaction_func(self.mouse_just_clicked, self.sell_slot_list, self.sell_slot_data_list, self.sell_slot_data)

            if self.exit_button.state == "pressed" and self.shop_ui.status == "menu":
                self._close_shop()
            if self.buy_button.state == "pressed":
                self._open_buy_menu()
            if self.exit_buy_menu_button.pressed:
                self._close_buy_menu()
            if self.sell_button.pressed:
                self._open_sell_menu()
            if self.exit_sell_menu_button.pressed:
                self._close_sell_menu()
    
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
        self.shop_ui.status = "buy_menu"
        
    def _close_buy_menu(self):
        self.shop_ui.status = "menu"
        self.exit_buy_menu_button.status = "none"
        self.exit_buy_menu_button.pressed = False
    
    def _open_sell_menu(self):
        self.shop_ui.status = "sell_menu"
    
    def _close_sell_menu(self):
        self.shop_ui.status = "menu"
        self.exit_sell_menu_button.status = "none"
        self.exit_sell_menu_button.pressed = False

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