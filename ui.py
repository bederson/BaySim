from Tkinter import *
from constants import *
from simulation import *


class UI():
    def __init__(self, sim):
        self.root = None
        self.canvas = None
        self.simulation = sim
        self.world_images = {}
        self.creature_id = None
        self.creature_meter_id = None
        self.cell_id_dict = {}
        self.watercell_id_dict = {}
        self.plant_id_dict = {}
        self.text_id_dict = {}

    ######## HANDLER CODE
    def init_handlers(self):
        self.simulation.delay_creature_auto_movement()
        self.create_event_timer()
        self.canvas.bind_all('<KeyPress>', self.key_handler)
        self.simulation.add_world_handler(self.world_handler)
        self.simulation.add_creature_handler(self.creature_handler)

    def create_event_timer(self, delay_time=STEP_TIME):
        self.root.after(delay_time, self.timer_handler)

    def timer_handler(self):
        self.simulation.step()
        self.create_event_timer()

    def key_handler(self, evt):
        if not evt.keysym in DIRECTION_DELTAS:
            return
        original_location = self.simulation.creature.get_location()
        new_location = self.simulation.creature.move(evt.keysym, self.simulation.world)
        if new_location:
            self.simulation.creature.eat(self.simulation.world)
            self.simulation.delay_creature_auto_movement()
            self.creature_handler(original_location, new_location)      # Call manually because creature doesn't fire events

    # Gets called by simulation when world changes
    def world_handler(self):
        self.canvas_update_creature_meter()
        self.canvas_update_water_and_plant()

    # Gets called by simulation when creature changes
    def creature_handler(self, original_location, new_location):
        if new_location:
            self.canvas_move_creature(original_location, new_location)
            self.canvas_update_creature_meter()

    ######### RENDERING CODE
    def canvas_allocate_images(self):
        self.world_images = {
            IMAGE_CREATURE_UP: PhotoImage(file=IMAGE_CREATURE_UP),
            IMAGE_CREATURE_DOWN: PhotoImage(file=IMAGE_CREATURE_DOWN),
            IMAGE_CREATURE_LEFT: PhotoImage(file=IMAGE_CREATURE_LEFT),
            IMAGE_CREATURE_RIGHT: PhotoImage(file=IMAGE_CREATURE_RIGHT),
            IMAGE_WATER_SOURCE: PhotoImage(file=IMAGE_WATER_SOURCE),
            IMAGE_ARABLE_LAND: PhotoImage(file=IMAGE_ARABLE_LAND),
            IMAGE_LAND1: PhotoImage(file=IMAGE_LAND1),
            IMAGE_LAND2: PhotoImage(file=IMAGE_LAND2),
            IMAGE_LAND3: PhotoImage(file=IMAGE_LAND3),
            IMAGE_LAND4: PhotoImage(file=IMAGE_LAND4),
            IMAGE_LAND5: PhotoImage(file=IMAGE_LAND5),
            IMAGE_LAND6: PhotoImage(file=IMAGE_LAND6),
            IMAGE_LAND7: PhotoImage(file=IMAGE_LAND7),
            IMAGE_LAND8: PhotoImage(file=IMAGE_LAND8),
            IMAGE_LAND9: PhotoImage(file=IMAGE_LAND9),
            IMAGE_LAND10: PhotoImage(file=IMAGE_LAND10),
            IMAGE_PLANT1: PhotoImage(file=IMAGE_PLANT1),
            IMAGE_PLANT2: PhotoImage(file=IMAGE_PLANT2),
            IMAGE_PLANT3: PhotoImage(file=IMAGE_PLANT3),
            IMAGE_PLANT4: PhotoImage(file=IMAGE_PLANT4),
            IMAGE_PLANT5: PhotoImage(file=IMAGE_PLANT5),
            IMAGE_PLANT6: PhotoImage(file=IMAGE_PLANT6),
            IMAGE_PLANT7: PhotoImage(file=IMAGE_PLANT7),
            IMAGE_PLANT8: PhotoImage(file=IMAGE_PLANT8),
            IMAGE_PLANT9: PhotoImage(file=IMAGE_PLANT9),
            IMAGE_PLANT10: PhotoImage(file=IMAGE_PLANT10),
            IMAGE_WATER1: PhotoImage(file=IMAGE_WATER1),
            IMAGE_WATER2: PhotoImage(file=IMAGE_WATER2),
            IMAGE_WATER3: PhotoImage(file=IMAGE_WATER3),
            IMAGE_WATER4: PhotoImage(file=IMAGE_WATER4),
            IMAGE_WATER5: PhotoImage(file=IMAGE_WATER5),
            IMAGE_WATER6: PhotoImage(file=IMAGE_WATER6),
            IMAGE_WATER7: PhotoImage(file=IMAGE_WATER7),
            IMAGE_WATER8: PhotoImage(file=IMAGE_WATER8),
            IMAGE_WATER9: PhotoImage(file=IMAGE_WATER9),
            IMAGE_WATER10: PhotoImage(file=IMAGE_WATER10),
        }

    def canvas_get_image(self, image_key):
        return self.world_images[image_key]

    def canvas_get_creatureimage(self, direction):
        creature_image = None
        if direction == 'Left':
            creature_image = self.canvas_get_image(IMAGE_CREATURE_LEFT)
        elif direction == 'Right':
            creature_image = self.canvas_get_image(IMAGE_CREATURE_RIGHT)
        elif direction == 'Up':
            creature_image = self.canvas_get_image(IMAGE_CREATURE_UP)
        elif direction == 'Down':
            creature_image = self.canvas_get_image(IMAGE_CREATURE_DOWN)
        return creature_image

    def canvas_get_landimage(self, elevation):
        land_image = None
        if 0 < elevation <= 0.5:
            land_image = self.canvas_get_image(IMAGE_LAND1)
        elif 0.5 < elevation <= 1.0:
            land_image = self.canvas_get_image(IMAGE_LAND2)
        elif 1.0 < elevation <= 1.5:
            land_image = self.canvas_get_image(IMAGE_LAND3)
        elif 1.5 < elevation <= 2.0:
            land_image = self.canvas_get_image(IMAGE_LAND4)
        elif 2.0 < elevation <= 2.5:
            land_image = self.canvas_get_image(IMAGE_LAND5)
        elif 2.5 < elevation <= 3.0:
            land_image = self.canvas_get_image(IMAGE_LAND6)
        elif 3.0 < elevation <= 3.5:
            land_image = self.canvas_get_image(IMAGE_LAND7)
        elif 3.5 < elevation <= 4.0:
            land_image = self.canvas_get_image(IMAGE_LAND8)
        elif 4.0 < elevation <= 4.5:
            land_image = self.canvas_get_image(IMAGE_LAND9)
        elif 4.5 < elevation:
            land_image = self.canvas_get_image(IMAGE_LAND10)
        return land_image

    def canvas_get_waterimage(self, water_amount):
        watercell_image = None
        if 0 < water_amount <= 0.1:
            watercell_image = self.canvas_get_image(IMAGE_WATER1)
        elif 0.1 < water_amount <= 0.2:
            watercell_image = self.canvas_get_image(IMAGE_WATER2)
        elif 0.2 < water_amount <= 0.3:
            watercell_image = self.canvas_get_image(IMAGE_WATER3)
        elif 0.3 < water_amount <= 0.4:
            watercell_image = self.canvas_get_image(IMAGE_WATER4)
        elif 0.4 < water_amount <= 0.5:
            watercell_image = self.canvas_get_image(IMAGE_WATER5)
        elif 0.5 < water_amount <= 0.6:
            watercell_image = self.canvas_get_image(IMAGE_WATER6)
        elif 0.6 < water_amount <= 0.7:
            watercell_image = self.canvas_get_image(IMAGE_WATER7)
        elif 0.7 < water_amount <= 0.8:
            watercell_image = self.canvas_get_image(IMAGE_WATER8)
        elif 0.8 < water_amount <= 0.9:
            watercell_image = self.canvas_get_image(IMAGE_WATER9)
        elif 0.9 < water_amount:
            watercell_image = self.canvas_get_image(IMAGE_WATER10)
        return watercell_image

    def canvas_get_plantimage(self, plant_amount):
        plant_image = None
        if 0 < plant_amount <= 0.1:
            plant_image = self.canvas_get_image(IMAGE_PLANT1)
        elif 0.1 < plant_amount <= 0.2:
            plant_image = self.canvas_get_image(IMAGE_PLANT2)
        elif 0.2 < plant_amount <= 0.3:
            plant_image = self.canvas_get_image(IMAGE_PLANT3)
        elif 0.3 < plant_amount <= 0.4:
            plant_image = self.canvas_get_image(IMAGE_PLANT4)
        elif 0.4 < plant_amount <= 0.5:
            plant_image = self.canvas_get_image(IMAGE_PLANT5)
        elif 0.5 < plant_amount <= 0.6:
            plant_image = self.canvas_get_image(IMAGE_PLANT6)
        elif 0.6 < plant_amount <= 0.7:
            plant_image = self.canvas_get_image(IMAGE_PLANT7)
        elif 0.7 < plant_amount <= 0.8:
            plant_image = self.canvas_get_image(IMAGE_PLANT8)
        elif 0.8 < plant_amount <= 0.9:
            plant_image = self.canvas_get_image(IMAGE_PLANT9)
        elif 0.9 < plant_amount:
            plant_image = self.canvas_get_image(IMAGE_PLANT10)
        return plant_image

    def canvas_create_cell(self, row_num, col_num, image):
        cell_id = self.canvas.create_image(col_num*CELL_SIZE, row_num*CELL_SIZE, anchor=NW, image=image)
        return cell_id

    def canvas_create_creaturecell(self, row_num, col_num, direction):
        if self.creature_id:
            self.canvas.delete(self.creature_id)
        creature_image = self.canvas_get_creatureimage(direction)
        self.creature_id = self.canvas_create_cell(row_num, col_num, creature_image)
        return self.creature_id

    def canvas_create_landcell(self, row_num, col_num, elevation):
        land_image = self.canvas_get_landimage(elevation)
        land_id = self.canvas_create_cell(row_num, col_num, land_image)
        key = (row_num, col_num)
        if key in self.cell_id_dict:
            self.canvas.delete(self.cell_id_dict[key])
        self.cell_id_dict[key] = land_id
        return land_image

    def canvas_create_watercell(self, row_num, col_num, water_level):
        water_image = self.canvas_get_waterimage(water_level)
        water_id = self.canvas_create_cell(row_num, col_num, water_image)
        key = (row_num, col_num)
        if key in self.watercell_id_dict:
            self.canvas.delete(self.watercell_id_dict[key])
        self.watercell_id_dict[key] = water_id
        return water_id

    def canvas_create_plantcell(self, row_num, col_num, plant_level):
        plant_image = self.canvas_get_plantimage(plant_level)
        plant_id = self.canvas_create_cell(row_num, col_num, plant_image)
        key = (row_num, col_num)
        if key in self.plant_id_dict:
            self.canvas.delete(self.plant_id_dict[key])
        self.plant_id_dict[key] = plant_id
        return plant_id

    def canvas_create_world(self):
        for row_num, row in enumerate(self.simulation.world.grid):
            for col_num, cell in enumerate(row):
                elevation = cell.get_elevation()
                self.canvas_create_landcell(row_num, col_num, elevation)
                if isinstance(cell, WaterSourceCell):
                    watersource_image = self.canvas_get_image(IMAGE_WATER_SOURCE)
                    self.canvas_create_cell(row_num, col_num, watersource_image)

                if DEBUG_ELEVATION:
                    elev_str = str(elevation)[0:3]
                else:
                    elev_str = ""
                text_id = self.canvas.create_text(CELL_SIZE * col_num + TEXT_OFFSET, CELL_SIZE * row_num, anchor=NW, fill='black', text=elev_str)
                self.text_id_dict[(row_num, col_num)] = text_id

        creature_loc = self.simulation.creature.get_location()
        creature_row = creature_loc[ROW_INDEX]
        creature_col = creature_loc[COL_INDEX]
        self.canvas_create_creaturecell(creature_row, creature_col, 'Up')
        self.canvas_update_creature_meter()

    def canvas_move_creature(self, original_location, new_location):
        delta_row = new_location[ROW_INDEX] - original_location[ROW_INDEX]
        delta_col = new_location[COL_INDEX] - original_location[COL_INDEX]
        if delta_row == 1:
            direction = 'Down'
        elif delta_row == -1:
            direction = 'Up'
        elif delta_col == 1:
            direction = 'Right'
        else:
            direction = 'Left'
        self.canvas_create_creaturecell(new_location[ROW_INDEX], new_location[COL_INDEX], direction)

    def canvas_update_creature_meter(self):
        creature_loc = self.simulation.creature.get_location()
        creature_row = creature_loc[ROW_INDEX]
        creature_col = creature_loc[COL_INDEX]
        value = self.simulation.creature.get_hunger_level()
        x1 = CELL_SIZE * creature_col
        y1 = CELL_SIZE * creature_row
        x2 = x1 + value * CELL_SIZE / LEVEL_MAX
        y2 = y1 + METER_HEIGHT
        if not self.creature_meter_id:
            self.creature_meter_id = self.canvas.create_rectangle(x1, y1, x2, y2, outline='gray', fill='orange')
        else:
            self.canvas.coords(self.creature_meter_id, x1, y1, x2, y2)

    def canvas_update_water_and_plant(self):
        for row_num, row in enumerate(self.simulation.world.grid):
            for col_num, cell in enumerate(row):
                if isinstance(cell, WaterSourceCell):
                    continue
                water_level = cell.get_water_level()
                key = (row_num, col_num)
                if key in self.watercell_id_dict:
                    self.canvas.delete(self.watercell_id_dict[key])
                if water_level > 0:
                    watercell_image = self.canvas_get_waterimage(water_level)
                    watercell_id = self.canvas.create_image(col_num * CELL_SIZE, row_num * CELL_SIZE, anchor=NW, image=watercell_image)
                    self.watercell_id_dict[(row_num, col_num)] = watercell_id
                else:
                    if isinstance(cell, ArableLandCell):
                        plant_level = cell.get_food_level()
                        if key in self.plant_id_dict:
                            self.canvas.delete(self.plant_id_dict[key])
                        if plant_level > 0:
                            plant_image = self.canvas_get_plantimage(plant_level)
                            plant_id = self.canvas.create_image(col_num * CELL_SIZE, row_num * CELL_SIZE, anchor=NW, image=plant_image)
                            self.plant_id_dict[(row_num, col_num)] = plant_id

                if DEBUG_WATER_LEVEL:
                    water_str = ""
                    if water_level > 0:
                        water_str = str(water_level)[:3]
                    cell_id = (row_num, col_num)
                    text_id = self.text_id_dict[cell_id]
                    self.canvas.itemconfig(text_id, text=water_str)
                    self.canvas.tag_raise(text_id)

    def init_simulation(self, size=WORLD_DIM * CELL_SIZE):
        self.root = Tk()
        self.root.wm_title("HW 8")
        canvas = Canvas(self.root, width=size, height=size)
        canvas.pack(fill="both", expand=1)
        self.root.wait_visibility(self.root)
        self.canvas = canvas
        self.canvas_allocate_images()
        self.init_handlers()
        self.canvas_create_world()
        self.root.mainloop()                # Enter Tk event loop

sim = Simulation()
ui = UI(sim)
ui.init_simulation()