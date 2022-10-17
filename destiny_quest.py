import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import random
import json
import sys
from player import empty_hero, Player

# Чтобы русские символы из json в stdout нормально отображались
sys.stdout.reconfigure(encoding='cp1251')

PROGRAM_NAME = "Destiny Quest Hero List (v.1.0)"

FONT_STATS = ("Courier New", 13, "bold")
# FONT_SIZE_CHARACTERISTICS = ("Courier New", 13, "bold")
FONT_DICES_RESULT = ("Courier New", 25, "bold")
FONT_DICES_BUTTON = ("Courier New", 10)
FONT_EQUIPMENT_LBL = ("Courier New", 12, "bold")
FONT_EQUIPMENT_VALUE_LBL = ("Courier New", 10)

# Через 40 мм переносить текст на другую строку в label
WRAP_EQUIPMENT_VALUE_LBL = "40m"

# BG_MAINFRAME = "#fce3ff"
COLOR_AGILITY = "#c1f797"
COLOR_ATTACK = "#e0807b"
COLOR_TEST = "#7cc7f5"
COLOR_REFRESH = "#dbdbdb"
COLOR_EQUIPMENT = "#dbdbdb"

ICON_HERO = "\N{Mage}"
ICON_ENEMY = "\N{Dragon Face}"
ICON_DICE = "\N{Game Die}"
ICON_REFRESH = "\N{Black Universal Recycling Symbol}"
ICON_AGILITY = "\N{CROSSED SWORDS}"
ICON_ATTACK = "\N{HEART WITH ARROW}"
ICON_SPEED = "\N{FOOTPRINTS}"
ICON_BRAWN = "\N{FLEXED BICEPS}"
ICON_MAGIC = "\N{Lightning Mood}"
ICON_ARMOUR = "\N{BLACK CROSS ON SHIELD}"
ICON_HEALTH = "\N{White Heart}"
ICON_BROKEN_HEART = "\N{Broken Heart}"
ICON_ENEMY_SPECIAL_ABILITY = "\N{Skull}"
ICON_BACKPACK = "\N{School Satchel}"
ICON_PLUS = "\N{Heavy Plus Sign}"
ICON_MINUS = "\N{Heavy Minus Sign}"

class DestinyQuest:
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title(PROGRAM_NAME)
        self.root.resizable(False,False)

        self.player = Player(empty_hero)
        # print(self.player.__dict__)


        self.init_gui()

        # Сохранять героя при закрытии приложения
        # self.root.protocol("WM_DELETE_WINDOW", callback)

    # Initialize GUI
    def init_gui(self):
        self.create_menu()
        self.create_mainframe()
        self.create_stats_field()
        self.create_dices_field()
        self.refresh_result()
        self.create_equipment_btn()



    def open_file(self):
        filepath = askopenfilename(
            filetypes=[("Json Files", "*.json"), ("All Files", "*.*")],
            initialdir=".\SaveData",
            )
        if not filepath:
            return

        # Сохранять героя при открытии нового героя

        with open(filepath, "r", encoding='utf-8') as input_file:
            self.player = Player(json.load(input_file))
            self.mainframe.destroy()
            self.init_gui()

    def save_file(self):
        filepath = asksaveasfilename(
        defaultextension="json",
        filetypes=[("Json Files", "*.json"), ("Все файлы", "*.*")],
        initialdir=".\SaveData",
        )
        if not filepath:
            return
        with open(filepath, "w", encoding='utf-8') as output_file:
            json.dump(self.player, output_file, default=Player.player_2_json,  ensure_ascii=False, indent=4)


    def refresh_result(self):
        """ Обновить результаты подсчетов """
        self.hero_dices_result_lbl["text"] = "-"
        self.enemy_dices_result_lbl["text"] = "-"
        self.hero_dices_result_lbl["bg"] = COLOR_REFRESH
        self.enemy_dices_result_lbl["bg"] = COLOR_REFRESH

    def refresh_hero_health(self):
        """ Обнулить значение здоровья после битвы """
        self.hero_health_lbl["text"] = self.player.health
        self.hero_health_lbl["fg"] = "black"
        self.hero_health_icon_lbl["text"] = ICON_HEALTH

    def refresh_enemy(self):
        """ Обнулить все характеристики врага после боя """
        self.enemy_speed_ent.delete(0, tk.END)
        self.enemy_brawn_ent.delete(0, tk.END)
        self.enemy_magic_ent.delete(0, tk.END)
        self.enemy_armour_ent.delete(0, tk.END)
        self.enemy_health_ent.delete(0, tk.END)
        self.enemy_special_ability_name_ent.delete(0, tk.END)
        self.enemy_special_ability_ent.delete(0, tk.END)

    @staticmethod
    def get_dices(dices):
        """ Бросить кости """
        dices_result = []
        for _ in range(dices):
            dice_result = random.randint(1, 6)
            dices_result.append(dice_result)
        return dices_result

    def make_damage(self, attack_result, player):
        """ Подсчитать урон и уменьшить здоровье герою или врагу. Атрибут player - кому нанесено повреждение """
        # узнать текущее здоровье
        if player == "hero":
            self.health = int(self.hero_health_lbl["text"])
        elif player == "enemy":
            try:
                self.health = int(self.enemy_health_ent.get())
            except ValueError:
                self.health = 0
        # Узнать показатели брони
        if player == "hero":
            self.armour = self.player.armour
        elif player == "enemy":
            try:
                self.armour = int(self.enemy_armour_ent.get())
            except ValueError:
                self.armour = 0
        # Посчитать урон
        if attack_result > self.armour:
            self.damage = attack_result - self.armour
        else:
            self.damage = 0
        # Уменьшить здоровье
        if player == "hero":
            # temporary (for each battte) health
            self.temp_health = self.health - self.damage
            # Применить специальные способности
            try:
                self.temp_special_damage = int(self.enemy_special_ability_ent.get())
            except ValueError:
                self.temp_special_damage = 0
            self.temp_health -= self.temp_special_damage

            self.hero_health_lbl["text"] = self.temp_health
            self.hero_health_icon_lbl["text"] = ICON_BROKEN_HEART
            self.hero_health_lbl["fg"] = "red"
        elif player == "enemy":
            self.enemy_health_ent.delete(0, tk.END)
            self.enemy_health_ent.insert(0, str(self.health - self.damage))
            # Применить специальные способности


    def update_all_labels(self):
        # Может сделать одну функцию, которая убивает класс всей программы и создаеь новый, чтобы все обновилось, а как сохранить все что наиграл?
        pass

    def update_hero_stats(self):
        # self.stats_hero_field.destroy()
        # self.stats_hero_field.__init__()
        pass


    def get_result(self, dices, player, test):
        """ Подсчитать результат после броска кубиков с учетом модификаторов """
        if test not in ("agility", "attack", "speed", "brawn", "magic", "armour"):
            raise testError("Некорректный тип проверки")

        colors = {
            "agility":COLOR_AGILITY,
            "attack":COLOR_ATTACK,
            "speed": COLOR_TEST,
            "brawn": COLOR_TEST,
            "magic": COLOR_TEST,
            "armour": COLOR_TEST,
            }
        test_modifiers_icons = {
            "agility": ICON_SPEED,
            "attack": ICON_BRAWN,
            "speed": ICON_SPEED,
            "brawn": ICON_BRAWN,
            "magic": ICON_MAGIC,
            "armour": ICON_ARMOUR,
            }
        test_hero_modifiers = {
            "agility": self.player.speed,
            "attack": (self.player.brawn, self.player.magic),
            "speed": self.player.speed,
            "brawn": self.player.brawn,
            "magic": self.player.magic,
            "armour": self.player.armour,
            }
        test_enemy_modifiers = {
            "agility": self.enemy_speed_ent.get(),
            "attack": (self.enemy_brawn_ent.get(), self.enemy_magic_ent.get()),
            "armour": self.enemy_armour_ent.get(),
            }

        self.color = colors[test]
        self.dices_result = DestinyQuest.get_dices(dices)
        self.result_str = ""
        for dice_result in self.dices_result:
            self.result_str += f"{ICON_DICE}{dice_result}+"

        if player == "hero":
            if test == "attack":
                self.modifier = max(test_hero_modifiers[test])
                if self.player.brawn >= self.player.magic:
                    self.modifier_icon = test_modifiers_icons["brawn"]
                else:
                    self.modifier_icon = test_modifiers_icons["magic"]
            else:
                self.modifier_icon = test_modifiers_icons[test]
                self.modifier = test_hero_modifiers[test]
            self.attack_result = sum(self.dices_result) + int(self.modifier)
            self.result_str = f"{self.result_str[:-1]}+{self.modifier_icon}{str(self.modifier)}={self.attack_result}"
            self.hero_dices_result_lbl["text"] = self.result_str
            self.hero_dices_result_lbl["bg"] = self.color
            # make damage
            if test == "attack":
                self.make_damage(self.attack_result, "enemy")

        elif player == "enemy":
            try:
                self.modifier = int(max(test_enemy_modifiers[test]))
            except ValueError:
                self.modifier = 0
            if test == "attack":
                try:
                    enemy_brawn = int(self.enemy_brawn_ent.get())
                except ValueError:
                    enemy_brawn = 0
                try:
                    enemy_magic = int(self.enemy_magic_ent.get())
                except ValueError:
                    enemy_magic = 0
                if enemy_brawn >= enemy_magic:
                    self.modifier_icon = test_modifiers_icons["brawn"]
                else:
                    self.modifier_icon = test_modifiers_icons["magic"]
            else:
                self.modifier_icon = test_modifiers_icons[test]
            self.attack_result = sum(self.dices_result) + int(self.modifier)
            self.result_str = f"{self.result_str[:-1]}+{self.modifier_icon}{str(self.modifier)}={self.attack_result}"
            self.enemy_dices_result_lbl["text"] = self.result_str
            self.enemy_dices_result_lbl["bg"] = self.color
            # make damage
            if test == "attack":
                self.make_damage(self.attack_result, "hero")

    # Словарь открытых окон для каждого оборудования. Чтобы окно для каждого оборудования открывалось 1 раз.
    global opened_window
    opened_window = {}
    def open_equipment_window(self, equipment_cell_name):
        """ Открыть одно новое окно для любой ячейки в обмундировании и рюкзаке """
        global opened_window
        if equipment_cell_name not in opened_window.keys():
            opened_window[equipment_cell_name] = 1
            self.equipment_window = EquipmentWindow(equipment_cell_name)
            # Запретить пользователю взаимодействовать с основным окном
            self.equipment_window.grab_set()

    """ GUI """
    def create_menu(self):
        """ Menu """
        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Открыть", command=self.open_file)
        self.filemenu.add_command(label="Сохранить как...", command=self.save_file)
        self.menubar.add_cascade(label="Герой", menu=self.filemenu)

        self.root.config(menu=self.menubar)

    def create_mainframe(self):
        """ Create mainframe """
        self.mainframe = tk.Frame(self.root)
        self.mainframe.rowconfigure([0, 1, 2, 3], weight=1)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.grid(padx=3)

    def create_stats_field(self):
        """ Top general statistic field """
        # Frames
        self.stats_field = tk.Frame(self.mainframe)
        self.stats_field.rowconfigure(0, weight=1)
        self.stats_field.columnconfigure(0, weight=1)
        # какая строка верх или низ правильная?
        self.stats_field.columnconfigure(1, weight=1)
        self.stats_hero_field = tk.Frame(self.stats_field)
        self.stats_enemy_field = tk.Frame(self.stats_field)
        self.stats_hero_field.rowconfigure([0, 1, 2], weight=1)
        self.stats_hero_field.columnconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], weight=1)
        self.stats_enemy_field.rowconfigure([0, 1, 2], weight=1)
        self.stats_enemy_field.columnconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], weight=1)
        self.stats_field.grid(row=0, sticky="nsew")
        self.stats_hero_field.grid(row=0, column=0, sticky="nsew")
        self.stats_enemy_field.grid(row=0, column=1, sticky="nsew", padx=2)

        # Widgets❤️
        self.hero_name_icon_lbl = tk.Label(self.stats_hero_field, text=f"{ICON_HERO}", fg="blue", font=FONT_STATS)
        self.hero_name_lbl = tk.Label(self.stats_hero_field, text=f"{self.player.name}", fg="blue", font=FONT_STATS)
        self.hero_name_icon_lbl.grid(row=0, column=0, sticky="w")
        self.hero_name_lbl.grid(row=0, column=1, columnspan=10, sticky="w")

        self.hero_path_lbl = tk.Label(self.stats_hero_field, text=f"{self.player.path}", font=FONT_STATS)
        self.hero_career_lbl = tk.Label(self.stats_hero_field, text=f"{self.player.career}", font=FONT_STATS)
        self.hero_path_lbl.grid(row=1, column=0, columnspan=5, sticky="w")
        self.hero_career_lbl.grid(row=1, column=4, columnspan=5, sticky="w")

        self.hero_speed_icon_lbl = tk.Label(self.stats_hero_field, text=f"{ICON_SPEED}", font=FONT_STATS)
        self.hero_speed_lbl = tk.Label(self.stats_hero_field, text=f"{self.player.speed}", font=FONT_STATS)
        self.hero_speed_icon_lbl.grid(row=2, column=0, sticky="e")
        self.hero_speed_lbl.grid(row=2, column=1, sticky="w")
        self.hero_brawn_icon_lbl = tk.Label(self.stats_hero_field, text=f"{ICON_BRAWN}", font=FONT_STATS)
        self.hero_brawn_lbl = tk.Label(self.stats_hero_field, text=f"{self.player.brawn}", font=FONT_STATS)
        self.hero_brawn_icon_lbl.grid(row=2, column=2, sticky="e")
        self.hero_brawn_lbl.grid(row=2, column=3, sticky="w")
        self.hero_magic_icon_lbl = tk.Label(self.stats_hero_field, text=f"{ICON_MAGIC}", font=FONT_STATS)
        self.hero_magic_lbl = tk.Label(self.stats_hero_field, text=f"{self.player.magic}", font=FONT_STATS)
        self.hero_magic_icon_lbl.grid(row=2, column=4, sticky="e")
        self.hero_magic_lbl.grid(row=2, column=5, sticky="w")
        self.hero_armour_icon_lbl = tk.Label(self.stats_hero_field, text=f"{ICON_ARMOUR}", font=FONT_STATS)
        self.hero_armour_lbl = tk.Label(self.stats_hero_field, text=f"{self.player.armour}", font=FONT_STATS)
        self.hero_armour_icon_lbl.grid(row=2, column=6, sticky="e")
        self.hero_armour_lbl.grid(row=2, column=7, sticky="w")
        self.hero_health_icon_lbl = tk.Label(self.stats_hero_field, text=f"{ICON_HEALTH}", fg="red", font=FONT_STATS)
        self.hero_health_lbl = tk.Label(self.stats_hero_field, text=f"{self.player.health}", font=FONT_STATS)
        self.hero_health_icon_lbl.grid(row=2, column=8, sticky="e")
        self.hero_health_lbl.grid(row=2, column=9, sticky="w")
        # Чтобы отодвинуть колонки статистики врага
        self.empty_lbl = tk.Label(self.stats_hero_field, text="", width=7).grid(row=1, column=11)
        self.empty_lbl = tk.Label(self.stats_hero_field, text="", width=7).grid(row=2, column=11)

        self.enemy_name_lbl = tk.Label(self.stats_enemy_field, text=f"{ICON_ENEMY} Враг", fg="red", font=FONT_STATS)
        self.enemy_name_lbl.grid(row=0, column=0, columnspan=10, sticky="e")

        self.enemy_special_ability_icon_lbl = tk.Label(self.stats_enemy_field, text=f"{ICON_ENEMY_SPECIAL_ABILITY}", font=FONT_STATS)
        self.enemy_special_ability_icon_lbl.grid(row=1, column=0)
        self.enemy_special_ability_name_ent = tk.Entry(self.stats_enemy_field, font=FONT_STATS)
        self.enemy_special_ability_name_ent.grid(row=1, column=1, columnspan=9, sticky="ew")
        self.enemy_special_ability_ent = tk.Entry(self.stats_enemy_field, width=2, font=FONT_STATS)
        self.enemy_special_ability_ent.grid(row=1, column=9, columnspan=1, sticky="ew")

        self.enemy_speed_lbl = tk.Label(self.stats_enemy_field, text=f"{ICON_SPEED}", font=FONT_STATS)
        self.enemy_speed_lbl.grid(row=2, column=0, sticky="e")
        self.enemy_speed_ent = tk.Entry(self.stats_enemy_field, width=2, font=FONT_STATS)
        self.enemy_speed_ent.grid(row=2, column=1, sticky="ew")
        self.enemy_brawn_lbl = tk.Label(self.stats_enemy_field, text=f"{ICON_BRAWN}", font=FONT_STATS)
        self.enemy_brawn_lbl.grid(row=2, column=2, sticky="e")
        self.enemy_brawn_ent = tk.Entry(self.stats_enemy_field, width=2, font=FONT_STATS)
        self.enemy_brawn_ent.grid(row=2, column=3, sticky="ew")
        self.enemy_magic_lbl = tk.Label(self.stats_enemy_field, text=f"{ICON_MAGIC}", font=FONT_STATS)
        self.enemy_magic_lbl.grid(row=2, column=4, sticky="e")
        self.enemy_magic_ent = tk.Entry(self.stats_enemy_field, width=2, font=FONT_STATS)
        self.enemy_magic_ent.grid(row=2, column=5, sticky="ew")
        self.enemy_armour_lbl = tk.Label(self.stats_enemy_field, text=f"{ICON_ARMOUR}", font=FONT_STATS)
        self.enemy_armour_lbl.grid(row=2, column=6, sticky="e")
        self.enemy_armour_ent = tk.Entry(self.stats_enemy_field, width=2, font=FONT_STATS)
        self.enemy_armour_ent.grid(row=2, column=7, sticky="ew")
        self.enemy_health_lbl = tk.Label(self.stats_enemy_field, text=f"{ICON_HEALTH}", fg="red", font=FONT_STATS)
        self.enemy_health_lbl.grid(row=2, column=8, sticky="e")
        self.enemy_health_ent = tk.Entry(self.stats_enemy_field, width=2, font=FONT_STATS)
        self.enemy_health_ent.grid(row=2, column=9, sticky="ew")

        # tests characteristics
        self.hero_speed_lbl.bind("<Button-1>", lambda e: self.get_result(dices=2, player="hero", test="speed"))
        self.hero_brawn_lbl.bind("<Button-1>", lambda e: self.get_result(dices=2, player="hero", test="brawn"))
        self.hero_magic_lbl.bind("<Button-1>", lambda e: self.get_result(dices=2, player="hero", test="magic"))
        self.hero_armour_lbl.bind("<Button-1>", lambda e: self.get_result(dices=2, player="hero", test="armour"))
        # refresh health after battle
        self.hero_health_lbl.bind("<Button-1>", lambda e: self.refresh_hero_health())
        # refresh enemy stats after battle
        self.enemy_name_lbl.bind("<Button-1>", lambda e: self.refresh_enemy())

# =============================================================================================================================================
    def create_dices_field(self):
        """ Dices field """
        # Frames
        self.dices_field = tk.Frame(self.mainframe, borderwidth=2, relief=tk.GROOVE, padx=2)
        self.dices_field.rowconfigure([0, 1, 2], weight=1)
        self.dices_field.columnconfigure([0, 1, 2, 3, 4], weight=1)

        # Grid Frames
        self.dices_field.grid(row=1, sticky="nsew")

        # Widgets
        self.hero_dices_result_lbl = tk.Label(
            master=self.dices_field,
            font=FONT_DICES_RESULT,
            width=15,
            )
        self.hero_dices_result_lbl.grid(row=1, column=0, columnspan=2)
        # Refresh result button
        self.refresh_result_btn = tk.Button(
            master=self.dices_field,
            text=f"{ICON_REFRESH}",
            font=FONT_DICES_BUTTON,
            command=self.refresh_result,
            )
        self.refresh_result_btn.grid(row=1, column=2, padx=5)
        # Enemy dices result
        self.enemy_dices_result_lbl = tk.Label(
            master=self.dices_field,
            font=FONT_DICES_RESULT,
            width=15,
            )
        self.enemy_dices_result_lbl.grid(row=1, column=3, columnspan=2)
        # Hero dices result buttons
        self.hero_dices_agility_btn = tk.Button(
        master=self.dices_field,
        text=f"Ловкость{ICON_AGILITY}",
        font=FONT_DICES_BUTTON,
        fg="green",
        command=lambda:self.get_result(dices=2, player="hero", test="agility"),
        )
        self.hero_dices_agility_btn.grid(row=2, column=0, sticky="ew", pady=5)
        self.hero_dices_attack_btn = tk.Button(
        master=self.dices_field,
        text=f"Атака{ICON_ATTACK}",
        font=FONT_DICES_BUTTON,fg="red",
        command=lambda:self.get_result(dices=1, player="hero", test="attack"),
        )
        self.hero_dices_attack_btn.grid(row=2, column=1, sticky="ew", pady=5)
        # Enemy dices result buttons
        self.enemy_dices_agility_btn = tk.Button(
        master=self.dices_field,
        text=f"Ловкость{ICON_AGILITY}",
        font=FONT_DICES_BUTTON,
        fg="green",
        command=lambda:self.get_result(dices=2, player="enemy", test="agility"),
        )
        self.enemy_dices_agility_btn.grid(row=2, column=3, sticky="ew", pady=5)
        self.enemy_dices_attack_btn = tk.Button(
        master=self.dices_field,
        text=f"Атака{ICON_ATTACK}",
        font=FONT_DICES_BUTTON,fg="red",
        command=lambda:self.get_result(dices=1, player="enemy", test="attack"),
        )
        self.enemy_dices_attack_btn.grid(row=2, column=4, sticky="ew", pady=5)
# =============================================================================================================================================
    def create_equipment_btn(self):
        # При открытии программы оборудование скрыто
        self._equipment_closed = True
        self.equipment_btn = tk.Button(
        master=self.mainframe,
        text=f"{ICON_PLUS}{ICON_BACKPACK}Equipment",
        font=FONT_DICES_BUTTON,
        fg="orange",
        width=20,
        command=self.operate_equipment_btn,
        )
        self.equipment_btn.grid(row=2, sticky="nws")

    def operate_equipment_btn(self):
        """ Обработка нажатия кнопки Equipment """
        # Добавить сохранение в json всего что изменено
        if self._equipment_closed:
            self.create_equipment_field()
            self.equipment_btn["text"] = f"{ICON_MINUS}{ICON_BACKPACK}Equipment"
            self._equipment_closed = False
        else:
            self.equipment_field.grid_forget()
            self.equipment_btn["text"] = f"{ICON_PLUS}{ICON_BACKPACK}Equipment"
            self._equipment_closed = True


    def create_equipment_field(self):
        """ Equipment field """
        # Frames
        self.equipment_field = tk.Frame(self.mainframe, borderwidth=2, relief=tk.GROOVE, padx=2)
        self.equipment_field.rowconfigure([0, 1], weight=1)
        self.equipment_field.columnconfigure(0, weight=1)

        self.outfit_field = tk.Frame(self.equipment_field)
        self.outfit_field.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7], weight=1)
        self.outfit_field.columnconfigure([0, 1, 2], weight=1)

        self.backpack_field = tk.Frame(self.equipment_field)
        self.backpack_field.rowconfigure([0, 1, 2, 3], weight=1)
        self.backpack_field.columnconfigure([0, 1, 2, 3, 4], weight=1)

        # Grid Frames
        self.equipment_field.grid(row=3, sticky="nsew")
        self.outfit_field.grid(row=0, sticky="nsew")
        self.backpack_field.grid(row=1, sticky="nsew")

        # Cloak
        self.cloak_lbl = tk.Label(master=self.outfit_field, text="Cloak:", font=FONT_EQUIPMENT_LBL, bg=COLOR_EQUIPMENT, anchor="n")
        self.cloak_value_lbl = tk.Label(master=self.outfit_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text="мантия чародея из кожы васильска", font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.cloak_lbl.grid(row=0, column=0, sticky="nsew", pady=(2,0), padx=2)
        self.cloak_value_lbl.grid(row=1, column=0, sticky="nsew", padx=2)
        # Head
        self.head_lbl = tk.Label(master=self.outfit_field, text="Head:", font=FONT_EQUIPMENT_LBL, bg=COLOR_EQUIPMENT, anchor="n")
        self.head_value_lbl = tk.Label(master=self.outfit_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text="Корона", font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.head_lbl.grid(row=0, column=1, sticky="nsew", pady=(2,0))
        self.head_value_lbl.grid(row=1, column=1, sticky="nsew")
        # Gloves
        self.gloves_lbl = tk.Label(master=self.outfit_field, text="Gloves:", font=FONT_EQUIPMENT_LBL, bg=COLOR_EQUIPMENT, anchor="n")
        self.gloves_value_lbl = tk.Label(master=self.outfit_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text="ПДракона", font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.gloves_lbl.grid(row=0, column=2, sticky="nsew", pady=(2,0), padx=2)
        self.gloves_value_lbl.grid(row=1, column=2, sticky="nsew", padx=2)
        # Ring 1
        self.ring1_lbl = tk.Label(master=self.outfit_field, text="Ring 1:", font=FONT_EQUIPMENT_LBL, bg=COLOR_EQUIPMENT, anchor="n")
        self.ring1_value_lbl = tk.Label(master=self.outfit_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text="Кольцо власти:", font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.ring1_lbl.grid(row=2, column=0, sticky="nsew", pady=(2,0), padx=2)
        self.ring1_value_lbl.grid(row=3, column=0, sticky="nsew", padx=2)
        # Necklace
        self.necklace_lbl = tk.Label(master=self.outfit_field, text="Necklace:", font=FONT_EQUIPMENT_LBL, bg=COLOR_EQUIPMENT, anchor="n")
        self.necklace_value_lbl = tk.Label(master=self.outfit_field,wraplength=WRAP_EQUIPMENT_VALUE_LBL,  text="", font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.necklace_lbl.grid(row=2, column=1, sticky="nsew", pady=(2,0))
        self.necklace_value_lbl.grid(row=3, column=1, sticky="nsew")
        # Ring 2
        self.ring2_lbl = tk.Label(master=self.outfit_field, text="Ring 2:", font=FONT_EQUIPMENT_LBL, bg=COLOR_EQUIPMENT, anchor="n")
        self.ring2_value_lbl = tk.Label(master=self.outfit_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text="", font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.ring2_lbl.grid(row=2, column=2, sticky="nsew", pady=(2,0), padx=2)
        self.ring2_value_lbl.grid(row=3, column=2, sticky="nsew", padx=2)
        # # Right hand
        self.right_hand_lbl = tk.Label(master=self.outfit_field, text="Right hand:", font=FONT_EQUIPMENT_LBL, bg=COLOR_EQUIPMENT, anchor="n")
        self.right_hand_value_lbl = tk.Label(master=self.outfit_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text="", font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.right_hand_lbl.grid(row=4, column=0, sticky="nsew", pady=(2,0), padx=2)
        self.right_hand_value_lbl.grid(row=5, column=0, sticky="nsew", padx=2)
        # Chest
        self.chest_lbl = tk.Label(master=self.outfit_field, text="Chest:", font=FONT_EQUIPMENT_LBL, bg=COLOR_EQUIPMENT, anchor="n")
        self.chest_value_lbl = tk.Label(master=self.outfit_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text="", font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.chest_lbl.grid(row=4, column=1, sticky="nsew", pady=(2,0))
        self.chest_value_lbl.grid(row=5, column=1, sticky="nsew")
        # Left hand
        self.left_hand_lbl = tk.Label(master=self.outfit_field, text="Left hand:", font=FONT_EQUIPMENT_LBL, bg=COLOR_EQUIPMENT, anchor="n")
        self.left_hand_value_lbl = tk.Label(master=self.outfit_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text="", font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.left_hand_lbl.grid(row=4, column=2, sticky="nsew", pady=(2,0), padx=2)
        self.left_hand_value_lbl.grid(row=5, column=2, sticky="nsew", padx=2)
        # Talisman
        self.talisman_lbl = tk.Label(master=self.outfit_field, text="Talisman:", font=FONT_EQUIPMENT_LBL, bg=COLOR_EQUIPMENT, anchor="n")
        self.talisman_value_lbl = tk.Label(master=self.outfit_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text="", font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.talisman_lbl.grid(row=6, column=0, sticky="nsew", pady=(2,0), padx=2)
        self.talisman_value_lbl.grid(row=7, column=0, sticky="nsew", padx=2)
        # Feet
        self.feet_lbl = tk.Label(master=self.outfit_field, text="Feet:", font=FONT_EQUIPMENT_LBL, bg=COLOR_EQUIPMENT, anchor="n")
        self.feet_value_lbl = tk.Label(master=self.outfit_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text="", font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.feet_lbl.grid(row=6, column=1, sticky="nsew", pady=(2,0))
        self.feet_value_lbl.grid(row=7, column=1, sticky="nsew")
        # Money pouch
        self.money_pouch_lbl = tk.Label(master=self.outfit_field, text="Money pouch:", font=FONT_EQUIPMENT_LBL, bg=COLOR_EQUIPMENT, anchor="n")
        self.money_pouch_value_lbl = tk.Label(master=self.outfit_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text="", font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.money_pouch_lbl.grid(row=6, column=2, sticky="nsew", pady=(2,0), padx=2)
        self.money_pouch_value_lbl.grid(row=7, column=2, sticky="nsew", padx=2)

        # Backpack
        self.backpack_lbl = tk.Label(master=self.backpack_field, text="Backpack:", font=FONT_EQUIPMENT_LBL, anchor="nw")
        self.backpack_lbl.grid(row=0, column=0, columnspan=5, sticky="nsew", padx=2)
        # Cell 1
        self.cell1_lbl = tk.Label(master=self.backpack_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text="Копье", font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.cell1_lbl.grid(row=1, column=0, sticky="nsew", padx=1)
        # Cell 2
        self.cell2_lbl = tk.Label(master=self.backpack_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text="Копье", font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.cell2_lbl.grid(row=1, column=1, sticky="nsew", padx=1)
        # Cell 3
        self.cell3_lbl = tk.Label(master=self.backpack_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text="Копье", font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.cell3_lbl.grid(row=1, column=2, sticky="nsew", padx=1)
        # Cell 4
        self.cell4_lbl = tk.Label(master=self.backpack_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text="Копье", font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.cell4_lbl.grid(row=1, column=3, sticky="nsew", padx=1)
        # Cell 5
        self.cell5_lbl = tk.Label(master=self.backpack_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text="Копье", font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.cell5_lbl.grid(row=1, column=4, sticky="nsew", padx=1)
        # Notes
        self.notes_lbl = tk.Label(master=self.backpack_field, text="Notes:", font=FONT_EQUIPMENT_LBL, anchor="nw")
        self.notes_lbl.grid(row=2, column=0, columnspan=5, sticky="nsew", padx=2)
        self.notes_txt = tk.Text(master=self.backpack_field, height=3)
        self.notes_txt.grid(row=4, columnspan=5, sticky="nwse", padx=2, pady=2)
        #  Open equipment windows by click
        self.cloak_lbl.bind("<Button-1>", lambda e: self.open_equipment_window(self.cloak_lbl["text"]))
        self.cloak_value_lbl.bind("<Button-1>", lambda e: self.open_equipment_window(self.cloak_lbl["text"]))
        self.head_lbl.bind("<Button-1>", lambda e: self.open_equipment_window(self.head_lbl["text"]))
        self.head_value_lbl.bind("<Button-1>", lambda e: self.open_equipment_window(self.head_lbl["text"]))
        self.gloves_lbl.bind("<Button-1>", lambda e: self.open_equipment_window(self.gloves_lbl["text"]))
        self.gloves_value_lbl.bind("<Button-1>", lambda e: self.open_equipment_window(self.gloves_lbl["text"]))
        self.ring1_lbl.bind("<Button-1>", lambda e: self.open_equipment_window(self.ring1_lbl["text"]))
        self.ring1_value_lbl.bind("<Button-1>", lambda e: self.open_equipment_window(self.ring1_lbl["text"]))
        self.necklace_lbl.bind("<Button-1>", lambda e: self.open_equipment_window(self.necklace_lbl["text"]))
        self.necklace_value_lbl.bind("<Button-1>", lambda e: self.open_equipment_window(self.necklace_lbl["text"]))
        self.ring2_lbl.bind("<Button-1>", lambda e: self.open_equipment_window(self.ring2_lbl["text"]))
        self.ring2_value_lbl.bind("<Button-1>", lambda e: self.open_equipment_window(self.ring2_lbl["text"]))
        self.right_hand_lbl.bind("<Button-1>", lambda e: self.open_equipment_window(self.right_hand_lbl["text"]))
        self.right_hand_value_lbl.bind("<Button-1>", lambda e: self.open_equipment_window(self.right_hand_lbl["text"]))
        self.chest_lbl.bind("<Button-1>", lambda e: self.open_equipment_window(self.chest_lbl["text"]))
        self.chest_value_lbl.bind("<Button-1>", lambda e: self.open_equipment_window(self.chest_lbl["text"]))
        self.left_hand_lbl.bind("<Button-1>", lambda e: self.open_equipment_window(self.left_hand_lbl["text"]))
        self.left_hand_value_lbl.bind("<Button-1>", lambda e: self.open_equipment_window(self.left_hand_lbl["text"]))
        self.talisman_lbl.bind("<Button-1>", lambda e: self.open_equipment_window(self.talisman_lbl["text"]))
        self.talisman_value_lbl.bind("<Button-1>", lambda e: self.open_equipment_window(self.talisman_lbl["text"]))
        self.feet_lbl.bind("<Button-1>", lambda e: self.open_equipment_window(self.feet_lbl["text"]))
        self.feet_value_lbl.bind("<Button-1>", lambda e: self.open_equipment_window(self.feet_lbl["text"]))
        self.money_pouch_lbl.bind("<Button-1>", lambda e: self.open_equipment_window(self.money_pouch_lbl["text"]))
        self.money_pouch_value_lbl.bind("<Button-1>", lambda e: self.open_equipment_window(self.money_pouch_lbl["text"]))
        self.cell1_lbl.bind("<Button-1>", lambda e: self.open_equipment_window("Backpack cell 1:"))
        self.cell2_lbl.bind("<Button-1>", lambda e: self.open_equipment_window("Backpack cell 2:"))
        self.cell3_lbl.bind("<Button-1>", lambda e: self.open_equipment_window("Backpack cell 3:"))
        self.cell4_lbl.bind("<Button-1>", lambda e: self.open_equipment_window("Backpack cell 4:"))
        self.cell5_lbl.bind("<Button-1>", lambda e: self.open_equipment_window("Backpack cell 5:"))

# =============================================================================================================================
class EquipmentWindow(tk.Toplevel):
    """ Class for creating a new window for any equipment cell """
    def __init__(self, equipment_cell_name):
        super().__init__()
        self.equipment_cell_name = equipment_cell_name
        self.title(f"Сharacteristics {self.equipment_cell_name}")
        self.resizable(False,False)

        self.init_gui()

    def init_gui(self):
        """ Create window GUI """
        # Create mainframe
        self.mainframe = tk.Frame(self)
        self.mainframe.rowconfigure([0, 1, 2], weight=1)
        self.mainframe.columnconfigure(0, weight=1)
        # Create equipment_cell_name frame
        self.equipment_cell_name_field = tk.Frame(self.mainframe)
        self.equipment_cell_name_field.rowconfigure(0, weight=1)
        self.equipment_cell_name_field.columnconfigure(0, weight=1)
        # Create equipment_stats frame
        self.equipment_stats_field = tk.Frame(self.mainframe)
        self.equipment_stats_field.rowconfigure([0, 1], weight=1)
        self.equipment_stats_field.columnconfigure([0,1,2,3,4,5,6,7], weight=1)
        # Create buttons frame
        self.buttons_field = tk.Frame(self.mainframe)
        self.buttons_field.rowconfigure(0, weight=1)
        self.buttons_field.columnconfigure([0,1,2], weight=1)
        # Frames grid
        self.mainframe.grid(padx=3)
        self.equipment_cell_name_field.grid(row=0, sticky="nsew", padx=5, pady=5)
        self.equipment_stats_field.grid(row=1, sticky="nsew", padx=5, pady=5)
        self.buttons_field.grid(row=2, sticky="nsew", padx=5, pady=(10,5))
        # Equipment cell name label
        self.equipment_cell_name_lbl = tk.Label(master=self.equipment_cell_name_field, text=f"{self.equipment_cell_name[:-1]}", font=FONT_STATS)
        self.equipment_cell_name_lbl.grid(row=0, sticky="w")
        # Equipment stats
        self.equipment_name_lbl = tk.Label(self.equipment_stats_field, text="Name: ", font=FONT_STATS)
        self.equipment_name_lbl.grid(row=0, sticky="nw", columnspan=2)
        self.equipment_name_ent = tk.Entry(self.equipment_stats_field, font=FONT_STATS)
        self.equipment_name_ent.grid(row=0, sticky="nw", column=2, columnspan=6)
        self.equipment_speed_lbl = tk.Label(self.equipment_stats_field, text=f"{ICON_SPEED}", font=FONT_STATS)
        self.equipment_speed_lbl.grid(row=1, column=0, sticky="e")
        self.equipment_speed_ent = tk.Entry(self.equipment_stats_field, width=2, font=FONT_STATS)
        self.equipment_speed_ent.grid(row=1, column=1, sticky="ew")
        self.equipment_brawn_lbl = tk.Label(self.equipment_stats_field, text=f"{ICON_BRAWN}", font=FONT_STATS)
        self.equipment_brawn_lbl.grid(row=1, column=2, sticky="e")
        self.equipment_brawn_ent = tk.Entry(self.equipment_stats_field, width=2, font=FONT_STATS)
        self.equipment_brawn_ent.grid(row=1, column=3, sticky="ew")
        self.equipment_magic_lbl = tk.Label(self.equipment_stats_field, text=f"{ICON_MAGIC}", font=FONT_STATS)
        self.equipment_magic_lbl.grid(row=1, column=4, sticky="e")
        self.equipment_magic_ent = tk.Entry(self.equipment_stats_field, width=2, font=FONT_STATS)
        self.equipment_magic_ent.grid(row=1, column=5, sticky="ew")
        self.equipment_armour_lbl = tk.Label(self.equipment_stats_field, text=f"{ICON_ARMOUR}", font=FONT_STATS)
        self.equipment_armour_lbl.grid(row=1, column=6, sticky="e")
        self.equipment_armour_ent = tk.Entry(self.equipment_stats_field, width=2, font=FONT_STATS)
        self.equipment_armour_ent.grid(row=1, column=7, sticky="ew")
        # Buttons
        self.put_on_btn = tk.Button(master=self.buttons_field, text="Put on")
        self.throw_away_btn = tk.Button(master=self.buttons_field, text="Throw away")
        self.in_backpack_btn = tk.Button(master=self.buttons_field, text="In backpack")
        self.put_on_btn.grid(row=0, column=0, sticky="nsew", padx=5)
        self.throw_away_btn.grid(row=0, column=1, sticky="nsew", padx=5)
        self.in_backpack_btn.grid(row=0, column=2, sticky="nsew", padx=5)

# =============================================================================================================================
def main():
    root = tk.Tk()
    DestinyQuest(root)
    root.mainloop()

if __name__ == "__main__":
    main()
