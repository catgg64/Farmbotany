import pygame
from globals import *
import fbbutton
import inventorymanager
import spritemanager
import solid_object

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
    def __init__(self, pos_x: int, pos_y: int, floutwitch, farmbotany):
        
        """Initialize the shop with position and floutwitch reference."""
        
        self.image = self._load_image()
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        
        self.floutwitch = floutwitch
        
        self.shop_open = False
        self.shop_ui = ShopUI(100, 100)
        
        self.exit_button = fbbutton.FBButton(150, 150, 100, 50, "Exit")
        
        self.buy_button = fbbutton.FBButton(200, 250, 100, 50, "Buy")
        self.exit_buy_menu_button = fbbutton.FBButton(150, 150, 100, 50, "Back")
        
        self.sell_button = fbbutton.FBButton(550, 250, 100, 50, "Sell")
        self.actual_sell_button = fbbutton.FBButton(550, 250, 100, 50, "Sell")
        self.exit_sell_menu_button = fbbutton.FBButton(150, 150, 100, 50, "Back")
        self.sell_slot_data = inventorymanager.ItemData("1", 0)
        self.sell_slot_data_list = [self.sell_slot_data]
        self.sell_slot_list = []
        self.sell_slot = inventorymanager.Slot(self.sell_slot_data.id, 0, self.sell_slot_data.quantity, 400, 200, self.sell_slot_list, 64)
        
        self.mouse_realeased = False

        self.brick = solid_object.Brick(pos_x, pos_y, SHOP_SCALED_SIZE, SHOP_SCALED_SIZE)
        self.brick.append_self_to_list(farmbotany.solid_objects_list)

        self.farmbotany = farmbotany
        self.check_for_clicked_slot_interaction = inventorymanager.check_for_clicked_slot_interaction(farmbotany.mouse_just_clicked, farmbotany.right_just_clicked,
                                                                                                    self.sell_slot_list, self.sell_slot_data_list, 
                                                                                                    farmbotany.clicked_slot_data, farmbotany.is_picking_up)
        
        self.product_slot_list = []
        self.wheat_seed_slot = ProductSlot(400, 200, "3", 40, self.product_slot_list, 64, (255, 255, 255), 5, self.floutwitch)

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
        self.farmbotany.sprite_list.append(spritemanager.SpriteData(self.image, self.rect.x, self.rect.y, self.rect.x + SHOP_SCALED_SIZE, self.rect.y + SHOP_SCALED_SIZE, True))
        
        """Updates the "Actual" version of the rect."""
        self.actual_rect = pygame.Rect(self.rect.x - self.farmbotany.viewport.pos_x, self.rect.y - self.farmbotany.viewport.pos_y, SHOP_SCALED_SIZE, SHOP_SCALED_SIZE)

        #self.brick.append_self_to_list(self.farmbotany.solid_objects_list)

        #surface.blit(self.image, self.rect)
        #pygame.draw.rect(surface, BORDER_COLOR, self.rect, BORDER_WIDTH)
        
        """Updates the check of the mouse realsed"""
        self.mouse_realeased = mouse_realeased

        # Check collision only if shop is not already open
        if not self.shop_open and self.actual_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self._open_shop()
        #elif self.shop_open:
        #    self._close_shop()
        


    def update_shop_ui(self, screen: pygame.Surface) -> None:
        """Update and render the shop UI if visible."""
        self.shop_ui.update(screen)
        
        self.inventory = self.farmbotany.inventory

        if self.shop_open:
    
            self.exit_button.update(screen, (255, 154, 46), (200, 105, 1), (161, 83, 0), self.mouse_realeased)

            if self.shop_ui.status == "menu":
                self.buy_button.update(screen, (255, 154, 46), (200, 105, 1), (161, 83, 0), self.mouse_realeased)
                self.sell_button.update(screen, (255, 154, 46), (200, 105, 1), (161, 83, 0), self.mouse_realeased)

            if self.shop_ui.status == "buy_menu":
                self.exit_buy_menu_button.update(screen, (255, 154, 46), (200, 105, 1), (161, 83, 0), self.mouse_realeased)

                for product_slot in self.product_slot_list:
                    product_slot.update(screen, self.mouse_realeased, self.inventory, self.floutwitch)

            if self.shop_ui.status == "menu":
                self.sell_button.update(screen, (255, 154, 46), (200, 105, 1), (161, 83, 0), self.mouse_realeased)

            if self.shop_ui.status == "sell_menu":
                self.exit_sell_menu_button.update(screen, (255, 154, 46), (200, 105, 1), (161, 83, 0), self.mouse_realeased)
                inventorymanager.update_inventory(self.sell_slot_data_list, screen, self.sell_slot_list, 64, 400, 200, -30, 40, 10)
                inventorymanager.check_for_clicked_slot_interaction(self.farmbotany.mouse_just_clicked, self.farmbotany.right_just_clicked, self.sell_slot_list, self.sell_slot_data_list, self.farmbotany.clicked_slot_data, self.farmbotany.is_picking_up)
                self.actual_sell_button.update(screen, (255, 154, 46), (200, 105, 1), (161, 83, 0), self.mouse_realeased)

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

            if self.actual_sell_button.pressed:
                self._sell(self.sell_slot_data, self.floutwitch)

    def _open_shop(self) -> None:
        """Open the shop and update related states."""
        self.shop_open = True
        self.floutwitch.can_move = False
        self.shop_ui.visibility = True

    def _close_shop(self) -> None:
        """Close the shop and update related states."""
        self.shop_open = False
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

    def _sell(self, item_data, floutwitch):
        items = inventorymanager.items
        slot_id = item_data.id
        slot_quantity = item_data.quantity
        slot_data = items[slot_id][0]
        if slot_id != "1" and slot_data["can_be_sold"]:
            floutwitch.gold += slot_data["value"] * slot_quantity
            slot_id = "1"
            slot_quantity = 0
        item_data.id = slot_id
        item_data.quantity = slot_quantity

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

class ProductSlot:
    def __init__(self, x, y, item, price, product_slot_list, slot_size, color, width, floutwitch):
        self.text_font = pygame.font.SysFont("Ariel", 30)
        
        product_slot_list.append(self)

        self.item_data = inventorymanager.items[item][0]
        self.image = pygame.image.load(self.item_data["texture"])
        self.image = pygame.transform.scale(self.image, (slot_size, slot_size))
        self.x = x
        self.y = y
        self.price = price
        self.rect = pygame.Rect(x, y, slot_size, slot_size)
        self.item = item

        self.color = color
        self.width = width

        self.slot_size = slot_size

    def update(self, surface, mouse_realeased, inventory, floutwitch):
        if floutwitch.gold >= self.item_data["value"]:
            if mouse_realeased and self.rect.collidepoint(pygame.mouse.get_pos()):
                inventorymanager.add_item_to_inventory(inventory, inventorymanager.ItemData(self.item, 1))
                floutwitch.gold -= self.item_data["value"]
        #self.farmbotany.sprite_list.append(spritemanager.SpriteData(self.image, self.rect.x, self.rect.y, self.rect.x + SHOP_SCALED_SIZE, self.rect.y + SHOP_SCALED_SIZE))
        #print(self.rect.x)
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, self.color, self.rect, self.width)
        text = self.text_font.render(str(self.item_data["value"]), True, (255, 255, 255))
        surface.blit(text, (self.rect.x + self.slot_size + 10, self.rect.y + self.slot_size + 10))