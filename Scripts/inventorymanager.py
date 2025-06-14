import pygame

items = {
    "1": [{"name": "nothing", "texture": "Sprites/book.png"}],
    "2": [{"name": "book", "texture": "Sprites/book.png"}],
    "3": [{"name": "seed", "texture": "Sprites/vsauce_face.png"}]
}

pygame.font.init()

text_font = pygame.font.SysFont("Ariel", 30)

def setup_item_surfaces():
    for item in items.items():
        if item != "1":
            print(item)
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
        slots_list.append(self)


    # Updates it every frame (hope this works)
    def update(self, screen, item_size, pos_x, pos_y, item):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 5)
        if item.id != "1":
            screen.blit(pygame.transform.scale(pygame.image.load(items[item.id][0]["texture"]), (item_size, item_size)), (pos_x + 10, pos_y + 10))
            text = text_font.render(str(item.quantity), True, (255, 255, 255))
            screen.blit(text, (pos_x + 64, pos_y + 64))

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

def check_for_clicked_slot_interaction(mouse_just_clicked, slot_list, inventory, clicked_slot_data):
    if mouse_just_clicked:
        if check_point_collision_with_all_slots(slot_list, pygame.mouse.get_pos()) != None:
            slot_clicked = inventory[check_point_collision_with_all_slots(slot_list, pygame.mouse.get_pos()) - 1]
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

def update_inventory(inventory, screen, slot_list, item_size, init_pos_x, init_pos_y, spacement_x, sprite_size):
    for item_index, item in enumerate(inventory):
        slot = slot_list[item_index]
        slot.update_id_and_quantity(item.id, item.quantity)
        slot.update(screen, sprite_size, init_pos_x + (item_index * (item_size + spacement_x)), init_pos_y + 10, item)

def update_clicked_slot(inventory, screen, slot_list, item_size, init_pos_x, init_pos_y, spacement_x, sprite_size):
    for item_index, item in enumerate(inventory):
        slot = slot_list[item_index]
        slot.update_id_and_quantity(item.id, item.quantity)
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