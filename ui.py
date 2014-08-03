from Tkinter import *
from simulation import *


class UI():
    def __init__(self, simulation):
        self.root = None
        self.canvas = None
        self.simulation = simulation
        self.world_images = {}
        self.cell_id_dict = {}
        self.watercell_id_dict = {}
        self.pollutioncell_id_dict = {}
        self.plant_id_dict = {}
        self.text_id_dict = {}
        self.crab_id_dict = {}
        # UI
        self.label_num_crabs = None

    ######## HANDLER CODE
    def init_handlers(self):
        self.create_event_timer()
        self.canvas.bind_all('<KeyPress>', self.key_handler)
        self.canvas.bind_all('<Button-1>', self.mouse_handler)
        self.simulation.add_world_handler(self.world_handler)
        self.simulation.add_crab_handler(self.crab_handler)

    def create_event_timer(self, delay_time=STEP_TIME):
        self.root.after(delay_time, self.timer_handler)

    def timer_handler(self):
        self.simulation.step()
        self.create_event_timer()

    def key_handler(self, evt):
        # handle evt.keysym
        pass

    def mouse_handler(self, evt):
        # Click prints cell location
#        print "[" + str(evt.y / 8) + ", " + str(evt.x / 8) + "],"
        pass

    # Gets called by simulation when world changes
    def world_handler(self):
        self.canvas_update_visuals()
        self.update_stats()

    def crab_handler(self, cell):
        loc = cell.location
        health = 0
        if cell.crab:
            health = cell.crab.health
        self.update_crab_item(loc[ROW_INDEX], loc[COL_INDEX], health)

    ######### RENDERING CODE
    def canvas_allocate_images(self):
        self.world_images = {
            IMAGE_CRAB1: PhotoImage(file=IMAGE_CRAB1),
            IMAGE_CRAB2: PhotoImage(file=IMAGE_CRAB2),
            IMAGE_CRAB3: PhotoImage(file=IMAGE_CRAB3),
            IMAGE_CRAB4: PhotoImage(file=IMAGE_CRAB4),
            IMAGE_CRAB5: PhotoImage(file=IMAGE_CRAB5),
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
            IMAGE_POLLUTION1: PhotoImage(file=IMAGE_POLLUTION1),
            IMAGE_POLLUTION2: PhotoImage(file=IMAGE_POLLUTION2),
            IMAGE_POLLUTION3: PhotoImage(file=IMAGE_POLLUTION3),
            IMAGE_POLLUTION4: PhotoImage(file=IMAGE_POLLUTION4),
            IMAGE_POLLUTION5: PhotoImage(file=IMAGE_POLLUTION5),
            IMAGE_POLLUTION6: PhotoImage(file=IMAGE_POLLUTION6),
            IMAGE_POLLUTION7: PhotoImage(file=IMAGE_POLLUTION7),
            IMAGE_POLLUTION8: PhotoImage(file=IMAGE_POLLUTION8),
            IMAGE_POLLUTION9: PhotoImage(file=IMAGE_POLLUTION9),
            IMAGE_POLLUTION10: PhotoImage(file=IMAGE_POLLUTION10),
            IMAGE_BUILDING: PhotoImage(file=IMAGE_BUILDING)
        }

    def canvas_get_image(self, image_key):
        return self.world_images[image_key]

    def canvas_get_crabimage(self, health):
        crab_image = None
        if 0 < health <= 0.2 * MAX_HEALTH:
            crab_image = self.canvas_get_image(IMAGE_CRAB1)
        elif 0.2 * MAX_HEALTH < health <= 0.4 * MAX_HEALTH:
            crab_image = self.canvas_get_image(IMAGE_CRAB2)
        elif 0.4 * MAX_HEALTH < health <= 0.6 * MAX_HEALTH:
            crab_image = self.canvas_get_image(IMAGE_CRAB3)
        elif 0.6 * MAX_HEALTH < health <= 0.8 * MAX_HEALTH:
            crab_image = self.canvas_get_image(IMAGE_CRAB4)
        elif 0.8 * MAX_HEALTH < health:
            crab_image = self.canvas_get_image(IMAGE_CRAB5)
        return crab_image

    def canvas_get_landimage(self, elevation):
        land_image = None
        world = self.simulation.world
        elev_min = world.elevation_min
        elev_max = world.elevation_max
        elev_range = elev_max - elev_min
        if elev_min * 0.0/10 < elevation <= elev_min + elev_range * 1.0/10:
            land_image = self.canvas_get_image(IMAGE_LAND1)
        elif elev_min * 1.0/10 <= elevation <= elev_min + elev_range * 2.0/10:
            land_image = self.canvas_get_image(IMAGE_LAND2)
        elif elev_min * 2.0/10 <= elevation <= elev_min + elev_range * 3.0/10:
            land_image = self.canvas_get_image(IMAGE_LAND3)
        elif elev_min * 3.0/10 <= elevation <= elev_min + elev_range * 4.0/10:
            land_image = self.canvas_get_image(IMAGE_LAND4)
        elif elev_min * 4.0/10 <= elevation <= elev_min + elev_range * 5.0/10:
            land_image = self.canvas_get_image(IMAGE_LAND5)
        elif elev_min * 5.0/10 <= elevation <= elev_min + elev_range * 6.0/10:
            land_image = self.canvas_get_image(IMAGE_LAND6)
        elif elev_min * 6.0/10 <= elevation <= elev_min + elev_range * 7.0/10:
            land_image = self.canvas_get_image(IMAGE_LAND7)
        elif elev_min * 7.0/10 <= elevation <= elev_min + elev_range * 8.0/10:
            land_image = self.canvas_get_image(IMAGE_LAND8)
        elif elev_min * 8.0/10 <= elevation <= elev_min + elev_range * 9.0/10:
            land_image = self.canvas_get_image(IMAGE_LAND9)
        elif elev_min * 9.0/10 <= elevation:
            land_image = self.canvas_get_image(IMAGE_LAND10)
        return land_image

    def canvas_get_waterimage(self, water_amount):
        watercell_image = None
        world = self.simulation.world
        elev_range = 10
        if 0.0/10 < water_amount <= elev_range * 1.0/10:
            watercell_image = self.canvas_get_image(IMAGE_WATER1)
        elif 1.0/10 < water_amount <= elev_range * 2.0/10:
            watercell_image = self.canvas_get_image(IMAGE_WATER2)
        elif 2.0/10 < water_amount <= elev_range * 3.0/10:
            watercell_image = self.canvas_get_image(IMAGE_WATER3)
        elif 3.0/10 < water_amount <= elev_range * 4.0/10:
            watercell_image = self.canvas_get_image(IMAGE_WATER4)
        elif 4.0/10 < water_amount <= elev_range * 5.0/10:
            watercell_image = self.canvas_get_image(IMAGE_WATER5)
        elif 5.0/10 < water_amount <= elev_range * 6.0/10:
            watercell_image = self.canvas_get_image(IMAGE_WATER6)
        elif 6.0/10 < water_amount <= elev_range * 7.0/10:
            watercell_image = self.canvas_get_image(IMAGE_WATER7)
        elif 7.0/10 < water_amount <= elev_range * 8.0/10:
            watercell_image = self.canvas_get_image(IMAGE_WATER8)
        elif 8.0/10 < water_amount <= elev_range * 9.0/10:
            watercell_image = self.canvas_get_image(IMAGE_WATER9)
        elif 9.0/10 < water_amount:
            watercell_image = self.canvas_get_image(IMAGE_WATER10)
        return watercell_image

    def canvas_get_pollutionimage(self, pollution_amount):
        pollutioncell_image = None
        if 0 < pollution_amount <= 0.1:
            pollutioncell_image = self.canvas_get_image(IMAGE_POLLUTION1)
        elif 0.1 < pollution_amount <= 0.2:
            pollutioncell_image = self.canvas_get_image(IMAGE_POLLUTION2)
        elif 0.2 < pollution_amount <= 0.3:
            pollutioncell_image = self.canvas_get_image(IMAGE_POLLUTION3)
        elif 0.3 < pollution_amount <= 0.4:
            pollutioncell_image = self.canvas_get_image(IMAGE_POLLUTION4)
        elif 0.4 < pollution_amount <= 0.5:
            pollutioncell_image = self.canvas_get_image(IMAGE_POLLUTION5)
        elif 0.5 < pollution_amount <= 0.6:
            pollutioncell_image = self.canvas_get_image(IMAGE_POLLUTION6)
        elif 0.6 < pollution_amount <= 0.7:
            pollutioncell_image = self.canvas_get_image(IMAGE_POLLUTION7)
        elif 0.7 < pollution_amount <= 0.8:
            pollutioncell_image = self.canvas_get_image(IMAGE_POLLUTION8)
        elif 0.8 < pollution_amount <= 0.9:
            pollutioncell_image = self.canvas_get_image(IMAGE_POLLUTION9)
        elif 0.9 < pollution_amount:
            pollutioncell_image = self.canvas_get_image(IMAGE_POLLUTION10)
        return pollutioncell_image

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

    def canvas_create_image(self, row_num, col_num, image, offset=0):
        cell_id = self.canvas.create_image(col_num*CELL_SIZE+offset, row_num*CELL_SIZE+offset, anchor=NW, image=image)
        return cell_id

    def update_crab_item(self, row_num, col_num, health):
        key = (row_num, col_num)
        if key in self.crab_id_dict:
            self.canvas.delete(self.crab_id_dict[key])
            del self.crab_id_dict[key]
        crab_image = self.canvas_get_crabimage(health)
        if crab_image:
            crab_id = self.canvas_create_image(row_num, col_num, crab_image, offset= (10 - health) / 2)
            self.crab_id_dict[key] = crab_id

    def update_land_item(self, row_num, col_num, elevation):
        key = (row_num, col_num)
        if key in self.cell_id_dict:
            self.canvas.delete(self.cell_id_dict[key])
            del self.cell_id_dict[key]
        land_image = self.canvas_get_landimage(elevation)
        land_id = self.canvas_create_image(row_num, col_num, land_image)
        self.cell_id_dict[key] = land_id

    def update_building_item(self, row_num, col_num, elevation):
        key = (row_num, col_num)
        if key in self.cell_id_dict:
            self.canvas.delete(self.cell_id_dict[key])
            del self.cell_id_dict[key]
        building_image = self.canvas_get_image(IMAGE_BUILDING)
        building_id = self.canvas_create_image(row_num, col_num, building_image)
        self.cell_id_dict[key] = building_id

    def update_water_item(self, row_num, col_num, water_level):
        key = (row_num, col_num)
        if key in self.watercell_id_dict:
            self.canvas.delete(self.watercell_id_dict[key])
            del self.watercell_id_dict[key]
        if water_level > 0:
            water_image = self.canvas_get_waterimage(water_level)
            water_id = self.canvas_create_image(row_num, col_num, water_image)
            self.watercell_id_dict[key] = water_id

    def update_pollution_item(self, row_num, col_num, pollution_level):
        key = (row_num, col_num)
        if key in self.pollutioncell_id_dict:
            self.canvas.delete(self.pollutioncell_id_dict[key])
            del self.pollutioncell_id_dict[key]
        if pollution_level > 0:
            pollution_image = self.canvas_get_pollutionimage(pollution_level)
            pollution_id = self.canvas_create_image(row_num, col_num, pollution_image)
            self.pollutioncell_id_dict[key] = pollution_id

    def update_plant_item(self, row_num, col_num, plant_level):
        key = (row_num, col_num)
        if key in self.plant_id_dict:
            self.canvas.delete(self.plant_id_dict[key])
            del self.plant_id_dict[key]
        if plant_level > 0:
            plant_image = self.canvas_get_plantimage(plant_level)
            plant_id = self.canvas_create_image(row_num, col_num, plant_image)
            self.plant_id_dict[key] = plant_id

    def canvas_create_world(self):
        for row_num, row in enumerate(self.simulation.world.grid):
            for col_num, cell in enumerate(row):
                elevation = cell.get_elevation()
                if isinstance(cell, BuildingCell):
                    self.update_building_item(row_num, col_num, elevation)
                else:
                    self.update_land_item(row_num, col_num, elevation)

                if isinstance(cell, WaterSourceCell):
                    watersource_image = self.canvas_get_image(IMAGE_WATER_SOURCE)
                    self.canvas_create_image(row_num, col_num, watersource_image)

    def canvas_update_visuals(self):
        crab_count = 0
        for row_num, row in enumerate(self.simulation.world.grid):
            for col_num, cell in enumerate(row):
                if isinstance(cell, WaterSourceCell):
                    continue
                if isinstance(cell, BuildingCell):
                    continue

                # Update water overlay
                water_level = cell.get_water_level()
                self.update_water_item(row_num, col_num, water_level)

                # Update pollution overlay
                pollution_level = cell.get_pollution_level()
                self.update_pollution_item(row_num, col_num, pollution_level)

                # Update crab overlay
                if cell.crab:
                    # print cell.crab.health
                    self.update_crab_item(row_num, col_num, cell.crab.health)
                    crab_count += 1

                # Update plants
                if isinstance(cell, ArableLandCell):
                    plant_level = cell.get_food_level()
                    self.update_plant_item(row_num, col_num, plant_level)
        # print "crab count: " + str(crab_count)
        self.simulation.world.num_crabs = crab_count

    def update_stats(self):
        world = self.simulation.world
        text = str(world.num_crabs) + " crab"
        if world.num_crabs != 1:
            text += "s"
        self.label_num_crabs.set(text)

    def init_simulation(self, world_width=WORLD_WIDTH * CELL_SIZE, world_height=WORLD_HEIGHT * CELL_SIZE):
        self.root = Tk()
        self.root.wm_title("BaySim")

        self.canvas = Canvas(self.root, width=world_width, height=world_height)
        self.canvas.grid(row=1, column=1)
        frame = Frame(self.root)
        frame.grid(row=1, column=2)
        Label(frame, text="Bay Health").grid(row=1, column=2, columnspan=2)
        Label(frame).grid(row=2, column=2)
        self.label_num_crabs = StringVar()
        Label(frame, textvariable=self.label_num_crabs, anchor=W).grid(row=3, column=2, columnspan=2)
        Label(frame, text="some thing: ").grid(row=4, column=2)
        Button(frame, text="Do thing", command=f2_cmd).grid(row=4, column=3)

        Label(frame).grid(row=49, column=2, columnspan=2, stick=N+S+E+W)

        Button(frame, text="Exit", command=frame.quit).grid(row=50, column=2, columnspan=2, sticky=W+E)

        self.root.wait_visibility(self.root)
        self.canvas_allocate_images()
        self.init_handlers()
        self.canvas_create_world()
        self.root.lift()
        self.root.mainloop()                # Enter Tk event loop
        self.root.destroy()

def f2_cmd():
    print "Do it"

sim = Simulation()
ui = UI(sim)
ui.init_simulation()