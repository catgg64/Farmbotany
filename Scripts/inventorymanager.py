import pygame

items = {
    "1": [{"name": "nothing", "texture": "Sprites/book.png", "stackable": True, "can_be_sold": False, "value": 0}],
    "2": [{"name": "book", "texture": "Sprites/book.png", "stackable": True, "can_be_sold": True, "value": 10}],
    "3": [{"name": "seed", "texture": "Sprites/wheat_growing.png", "stackable": True, "can_be_sold": True, "value": 20}],
    "4": [{"name": "wheat", "texture": "Sprites/wheat.png", "stackable": True, "can_be_sold": True, "value": 50}],
    "5": [{"name": "hoe", "texture": "Sprites/hoe.png", "stackable": False, "can_be_sold": False, "value": 0}],
    "6": [{"name": "pickaxe", "texture": "Sprites/pickaxe.png", "stackable": False, "can_be_sold": False, "value": 0}],
    "7": [{"name": "water can", "texture": "Sprites/watercan.png", "stackable": False, "can_be_sold": False, "value": 0}],
    "8": [{"name": "potato", "texture": "Sprites/potato.png", "stackable": True, "can_be_sold": True, "value": 10}],
    "9": [{"name": "potato seed", "texture": "Sprites/potato seed.png", "stackable": True, "can_be_sold": True, "value": 5}]
}

pygame.font.init()

text_font = pygame.font.SysFont("Ariel", 30)

def setup_item_surfaces():
    for item in items.items():
        if item != "1":
            image = pygame.image.load(item[0]["texture"]).convert_alpha()
            item["texture"] = image


class ItemData:
    def __init__(self, id, quantity):
        self.id = id
        self.quantity = quantity

class Slot:
    # Initialized the Slot
    def __init__(self, id, index, quantity, pos_x, pos_y, slots_list, item_size):
        self.id = id
        self.quantity = quantity
        self.index = index
        self.rect = pygame.Rect(pos_x, pos_y, item_size, item_size)
        self.rect_color = (255, 255, 255)
        slots_list.append(self)


    # Updates it every frame (hope this works)
    def update(self, screen, item_size, pos_x, pos_y, item):
        item_data = items[item.id][0]

        pygame.draw.rect(screen, (227, 227, 227), self.rect, 0)
        pygame.draw.rect(screen, self.rect_color, self.rect, 5)
        if item.id != "1":
            screen.blit(pygame.transform.scale(pygame.image.load(items[item.id][0]["texture"]), (item_size, item_size)), (self.rect.x + 10, self.rect.y + 10))
            
            if item_data["stackable"]:
                text = text_font.render(str(item.quantity), True, (255, 255, 255))
                screen.blit(text, (self.rect.x + 45, self.rect.y + 45))
            
            self.rect_color = (255, 255, 255)

    #YAAAAY it worked let's add some more.
    def is_colliding_with_point(self, point):
        if self.rect.collidepoint(point):
            return self.index + 1
        return None

    # Updates the slot's position (regular updates just can't do).
    def update_position(self, pos_x, pos_y):
        self.rect.x = pos_x
        self.rect.y = pos_y

    # Updates the slot's id and quantity (dk how i didn't add this later)
    def update_id_and_quantity(self, id, quantity):
        self.id = id
        self.quantity = quantity

    # Sets the light mode of the slot to on.
    def light_up(self):
        self.rect_color = (255, 112, 112) # Original colors were (255, 253, 150)

    # Sets it to the normal color.
    def un_light_up(self):
        self.rect_color = (255, 255, 255)

def check_for_clicked_slot_interaction(mouse_just_clicked, right_just_clicked, slot_list, inventory, clicked_slot_data, is_picking_up, mouse_pos):
    
    if clicked_slot_data.id == "1":
        is_picking_up = False

    if mouse_just_clicked:
        if check_point_collision_with_all_slots(slot_list, mouse_pos) != None:
            slot_clicked = inventory[check_point_collision_with_all_slots(slot_list, mouse_pos) - 1]
            if slot_clicked.id != "1" and clicked_slot_data.id == "1":
                clicked_slot_data.id = slot_clicked.id
                clicked_slot_data.quantity = slot_clicked.quantity
                slot_clicked.id = "1"
                slot_clicked.quantity = 0
            elif slot_clicked.id == "1" and clicked_slot_data.id != "1":
                slot_clicked.id = clicked_slot_data.id
                slot_clicked.quantity = clicked_slot_data.quantity
                clicked_slot_data.id = "1"
                clicked_slot_data.quantity = 0
            elif slot_clicked.id == clicked_slot_data.id and slot_clicked.id != "1" and clicked_slot_data.id != "1":
                slot_clicked.quantity += clicked_slot_data.quantity
                clicked_slot_data.id = "1"
                clicked_slot_data.quantity = 0
            elif slot_clicked.id != "1" and clicked_slot_data.id != "1":
                new_slot_cliked = ItemData("1", 0)
                new_clicked_slot_data = ItemData("1", 0)
                new_slot_cliked.id = clicked_slot_data.id
                new_slot_cliked.quantity = clicked_slot_data.quantity
                new_clicked_slot_data.id = slot_clicked.id
                new_clicked_slot_data.quantity = slot_clicked.quantity
                slot_clicked.id = new_slot_cliked.id
                slot_clicked.quantity = new_slot_cliked.quantity
                clicked_slot_data.id = new_clicked_slot_data.id
                clicked_slot_data.quantity = new_clicked_slot_data.quantity
    if right_just_clicked:
        if check_point_collision_with_all_slots(slot_list, mouse_pos):
            slot_clicked = inventory[check_point_collision_with_all_slots(slot_list, mouse_pos) - 1]
            if slot_clicked.id != "1" and clicked_slot_data.id == "1":
                is_picking_up = True
                clicked_slot_data.id = slot_clicked.id
                clicked_slot_data.quantity += 1
                slot_clicked.quantity -= 1
            elif slot_clicked.id != "1" and is_picking_up:
                is_picking_up = True
                clicked_slot_data.id = slot_clicked.id
                clicked_slot_data.quantity += 1
                slot_clicked.quantity -= 1
            if clicked_slot_data.id != "1" and not is_picking_up:
                slot_clicked.id = clicked_slot_data.id
                slot_clicked.quantity += 1
                clicked_slot_data.quantity -= 1

def setup_inventory(size):
    inventory_list = [None] * size
    for x in range(0, size):
        inventory_list[x] = ItemData("1", 0)
    return inventory_list

def position_to_slot_value(position):
    result = round((position[0] / 64))
    return result

def draw_inventory(inventory, screen, item_size, init_pos_x, init_pos_y):
    for item_index, item in enumerate(inventory):
        if item.id != "1":
            screen.blit(pygame.transform.scale(pygame.image.load(items[item.id][0]["texture"]), (item_size, item_size)), (init_pos_x + (10 + (item_index * 64)), init_pos_y + 10))
            text = text_font.render(str(item.quantity), True, (255, 255, 255))
            screen.blit(text, (init_pos_x + (64 + (item_index * 64)), init_pos_y + 64))

def initialize_inventory(inventory, slot_list, init_pos_x, init_pos_y, item_size, rect_size, spacement_x):
    for item_index, item in enumerate(inventory):
        Slot(item.id, item_index, item.quantity, init_pos_x + (item_index * (item_size + spacement_x)), init_pos_y + 10, slot_list, rect_size)

def update_inventory(inventory, screen, slot_list, item_size, init_pos_x, init_pos_y, spacement_x, sprite_size, value_to_increase_from_y_position):
    for item_index, item in enumerate(inventory): # Checks for each slot.
        slot = slot_list[item_index]
        if inventory[item_index].quantity == 0:
            inventory[item_index].id = "1" # Checks if the quantity is 0, if so, make the slot's id 1 (nothing).
        slot.update_id_and_quantity(item.id, item.quantity) # Updates it's id and quantity
        slot.update(screen, sprite_size, init_pos_x + (item_index * (item_size + spacement_x)), init_pos_y + value_to_increase_from_y_position, item) # posisions them on screen

def update_clicked_slot(inventory, screen, slot_list, item_size, init_pos_x, init_pos_y, spacement_x, sprite_size):
    for item_index, item in enumerate(inventory):
        slot = slot_list[item_index]
        slot.update_id_and_quantity(item.id, item.quantity)
        if inventory[item_index].quantity == 0:
            inventory[item_index].id = "1"
        if slot.id != "1":
            slot.update_position(init_pos_x, init_pos_y)
            slot.update(screen, sprite_size, init_pos_x + (1 * (item_size + spacement_x)), init_pos_y, item)

def check_point_collision_with_all_slots(slot_list, point):
    for slot in slot_list:
        if slot.is_colliding_with_point(point):
            return slot.is_colliding_with_point(point)
        else:
            continue
    return None

def add_item_to_inventory(inventory, my_item):
    global tiles
    for index, item in enumerate(inventory):
        check_item = inventory[index]
        check_item_data = items[check_item.id][0]
        if check_item.id == my_item.id and check_item and check_item_data["stackable"]:
            check_item.quantity += my_item.quantity
            return

    for index, item in enumerate(inventory):
        check_item = inventory[index]
        if check_item.id == "1":
            check_item.id = my_item.id
            check_item.quantity = my_item.quantity
            return

def light_slot_by_number(light_number, slot_list):
    for index, slot in enumerate(slot_list):
        slot = slot_list[index]
        if index == light_number:
            slot.light_up()
        else:
            slot.un_light_up()
