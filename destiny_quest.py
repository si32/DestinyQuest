import tkinter as tk
from tkinter import ttk
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
PATH_LIST = ["None", "Mage","Warrior"]
# max money in the money pouch
MAX_MONEY = 10000
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
ICON_MONEY_BAG = "\N{MONEY BAG}"

class DestinyQuest:
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title(PROGRAM_NAME)
        self.root.resizable(False,False)
        # Open app with new hero
        self.player = Player(empty_hero)
        self.init_gui()
        # Сохранять героя при закрытии приложения
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    # Initialize GUI
    def init_gui(self):
        self.create_menu()
        self.create_mainframe()
        self.create_stats_field()
        self.create_dices_field()
        self.refresh_result()
        self.create_equipment_btn()
# =============================================================================================================================================
    def open_file(self):
        filepath = askopenfilename(
            filetypes=[("Json Files", "*.json"), ("All Files", "*.*")],
            initialdir=".\SaveData",
            )
        if not filepath:
            return
        # Сохранять героя при открытии нового героя
        with open(filepath, "r", encoding='utf-8') as input_file:
            try:
                self.player = Player(json.load(input_file))
                self.mainframe.destroy()
                self.init_gui()
            except KeyError:
                warning_msg = tk.messagebox.showwarning(title="Error", message="Bad file format!")

    def save_file(self):
        filepath = asksaveasfilename(
        defaultextension="json",
        filetypes=[("Json Files", "*.json"), ("Все файлы", "*.*")],
        initialdir=".\SaveData",
        )
        if not filepath:
            return None

        with open(filepath, "w", encoding='utf-8') as output_file:
            json.dump(self.player, output_file, default=Player.player_2_json,  ensure_ascii=False, indent=4)
        return "saved"

    def close_app(self):
        """ Save hero stats closing the app """
        confirm = tk.messagebox.askyesnocancel(title="Info", message="Save current DestinyQuest hero list?", default="yes")
        if confirm:
            if self.save_file() == "saved":
                self.root.destroy()
        # If push "Cancell" button
        elif confirm is None:
            return None
        else:
            self.root.destroy()

    def open_hero(self):
        """ Save hero before open a new one """
        confirm = tk.messagebox.askyesnocancel(title="Info", message="Save current DestinyQuest hero list?", default="yes")
        if confirm:
            if self.save_file() == "saved":
                self.open_file()
        # If push "Cancell" button
        elif confirm is None:
            return None
        else:
            self.open_file()

# =============================================================================================================================================
    def refresh_result(self):
        """ Обновить результаты подсчетов """
        self.hero_dices_result_lbl["text"] = "-"
        self.enemy_dices_result_lbl["text"] = "-"
        self.hero_dices_result_lbl["bg"] = COLOR_REFRESH
        self.enemy_dices_result_lbl["bg"] = COLOR_REFRESH

    def refresh_hero(self):
        """ Обнулить значение здоровья после битвы """
        self.player.speed_modifier = 0
        self.player.brawn_modifier = 0
        self.player.magic_modifier = 0
        self.player.armour_modifier = 0
        self.player.health_modifier = 0
        self.player.battle_damage = 0
        self.stats_hero_field.grid_forget()
        self.create_stats_hero_field()

    def refresh_stats(self):
        """ Обнулить все характеристики врага и героя после боя """
        self.stats_enemy_field.grid_forget()
        self.create_stats_enemy_field()
        self.refresh_hero()

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
            self.armour = int(self.hero_armour_lbl["text"])
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
            # Применить специальные способности врага
            try:
                self.temp_special_damage = int(self.enemy_special_ability_ent.get())
            except ValueError:
                self.temp_special_damage = 0
            self.player.battle_damage += self.damage + self.temp_special_damage
            self.stats_hero_field.grid_forget()
            self.create_stats_hero_field()
        elif player == "enemy":
            self.enemy_health_ent.delete(0, tk.END)
            self.enemy_health_ent.insert(0, str(self.health - self.damage))

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
            "agility": self.player.speed + self.player.speed_modifier,
            "attack": (self.player.brawn + self.player.brawn_modifier, self.player.magic + self.player.magic_modifier),
            "speed": self.player.speed + self.player.speed_modifier,
            "brawn": self.player.brawn + self.player.brawn_modifier,
            "magic": self.player.magic + self.player.magic_modifier,
            "armour": self.player.armour + self.player.armour_modifier,
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

    """ GUI """
    def create_menu(self):
        """ Menu """
        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Открыть", command=self.open_hero)
        self.filemenu.add_command(label="Сохранить как...", command=self.save_file)
        self.menubar.add_cascade(label="Герой", menu=self.filemenu)

        self.root.config(menu=self.menubar)

    def create_mainframe(self):
        """ Create mainframe """
        self.mainframe = tk.Frame(self.root)
        self.mainframe.rowconfigure([0, 1, 2, 3], weight=1)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.grid(padx=3)

    def create_stats_hero_field(self):
        self.stats_hero_field = tk.Frame(self.stats_field)
        self.stats_hero_field.rowconfigure([0, 1, 2], weight=1)
        self.stats_hero_field.columnconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], weight=1)
        self.stats_hero_field.grid(row=0, column=0, sticky="nsew")
        # Widgets❤️
        self.hero_name_icon_lbl = tk.Label(self.stats_hero_field, text=f"{ICON_HERO}", fg="blue", font=FONT_STATS)
        self.hero_name_lbl = tk.Label(self.stats_hero_field, text=f"{self.player.name}", fg="blue", font=FONT_STATS)
        self.hero_name_icon_lbl.grid(row=0, column=0, sticky="w")
        self.hero_name_lbl.grid(row=0, column=1, columnspan=10, sticky="w")
        self.hero_path_career_lbl = tk.Label(self.stats_hero_field, text=f"{self.player.path} - {self.player.career}", font=FONT_STATS)
        self.hero_path_career_lbl.grid(row=1, column=0, columnspan=10, sticky="w")
        self.hero_speed_icon_lbl = tk.Label(self.stats_hero_field, text=f"{ICON_SPEED}", font=FONT_STATS)
        self.hero_speed_lbl = tk.Label(self.stats_hero_field, text=f"{self.player.speed + self.player.speed_modifier}", font=FONT_STATS)
        self.hero_speed_icon_lbl.grid(row=2, column=0, sticky="e")
        self.hero_speed_lbl.grid(row=2, column=1, sticky="w")
        self.hero_brawn_icon_lbl = tk.Label(self.stats_hero_field, text=f"{ICON_BRAWN}", font=FONT_STATS)
        self.hero_brawn_lbl = tk.Label(self.stats_hero_field, text=f"{self.player.brawn + self.player.brawn_modifier}", font=FONT_STATS)
        self.hero_brawn_icon_lbl.grid(row=2, column=2, sticky="e")
        self.hero_brawn_lbl.grid(row=2, column=3, sticky="w")
        self.hero_magic_icon_lbl = tk.Label(self.stats_hero_field, text=f"{ICON_MAGIC}", font=FONT_STATS)
        self.hero_magic_lbl = tk.Label(self.stats_hero_field, text=f"{self.player.magic + self.player.magic_modifier}", font=FONT_STATS)
        self.hero_magic_icon_lbl.grid(row=2, column=4, sticky="e")
        self.hero_magic_lbl.grid(row=2, column=5, sticky="w")
        self.hero_armour_icon_lbl = tk.Label(self.stats_hero_field, text=f"{ICON_ARMOUR}", font=FONT_STATS)
        self.hero_armour_lbl = tk.Label(self.stats_hero_field, text=f"{self.player.armour + self.player.armour_modifier}", font=FONT_STATS)
        self.hero_armour_icon_lbl.grid(row=2, column=6, sticky="e")
        self.hero_armour_lbl.grid(row=2, column=7, sticky="w")
        icon = tk.StringVar()
        if self.player.battle_damage == 0:
            icon.set(ICON_HEALTH)
        else:
            icon.set(ICON_BROKEN_HEART)
        self.hero_health_icon_lbl = tk.Label(self.stats_hero_field, text=icon.get(), fg="red", font=FONT_STATS)
        # Если действует модификатор (выпито зелье), то цвет сердца зеленый
        if (self.player.speed_modifier or self.player.brawn_modifier or self.player.magic_modifier or self.player.armour_modifier or self.player.health_modifier) > 0:
            self.hero_health_icon_lbl.configure(fg="green")
        self.hero_health_lbl = tk.Label(self.stats_hero_field, text=f"{self.player.health + self.player.health_modifier - self.player.battle_damage}", fg="red", font=FONT_STATS)
        self.hero_health_icon_lbl.grid(row=2, column=8, sticky="e")
        self.hero_health_lbl.grid(row=2, column=9, sticky="w")
        # Чтобы отодвинуть колонки статистики врага
        self.empty_lbl = tk.Label(self.stats_hero_field, text="", width=7).grid(row=1, column=11)
        self.empty_lbl = tk.Label(self.stats_hero_field, text="", width=7).grid(row=2, column=11)
        # tests characteristics
        self.hero_speed_lbl.bind("<Button-1>", lambda e: self.get_result(dices=2, player="hero", test="speed"))
        self.hero_brawn_lbl.bind("<Button-1>", lambda e: self.get_result(dices=2, player="hero", test="brawn"))
        self.hero_magic_lbl.bind("<Button-1>", lambda e: self.get_result(dices=2, player="hero", test="magic"))
        self.hero_armour_lbl.bind("<Button-1>", lambda e: self.get_result(dices=2, player="hero", test="armour"))
        # refresh hero health after battle
        self.hero_health_lbl.bind("<Button-1>", lambda e: self.refresh_hero())
        # edit hero's name, path, carier
        self.hero_name_lbl.bind("<Button-1>", lambda e: self.open_edit_hero_name_window())

    def create_stats_enemy_field(self):
        self.stats_enemy_field = tk.Frame(self.stats_field)
        self.stats_enemy_field.rowconfigure([0, 1, 2], weight=1)
        self.stats_enemy_field.columnconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], weight=1)
        self.stats_enemy_field.grid(row=0, column=1, sticky="nsew", padx=2)
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
        # refresh enemy stats after battle
        self.enemy_name_lbl.bind("<Button-1>", lambda e: self.refresh_stats())

    def create_stats_field(self):
        """ Top general statistic field """
        # Frames
        self.stats_field = tk.Frame(self.mainframe)
        self.stats_field.rowconfigure(0, weight=1)
        self.stats_field.columnconfigure(0, weight=1)
        self.stats_field.columnconfigure(1, weight=1)
        self.stats_field.grid(row=0, sticky="nsew")
        self.create_stats_hero_field()
        self.create_stats_enemy_field()

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
        if self._equipment_closed:
            self.create_equipment_field()
            self.equipment_btn["text"] = f"{ICON_MINUS}{ICON_BACKPACK}Equipment"
            self._equipment_closed = False
        else:
            self.equipment_field.grid_forget()
            self.equipment_btn["text"] = f"{ICON_PLUS}{ICON_BACKPACK}Equipment"
            self._equipment_closed = True

    def save_notes(self, event):
        """ Save notes if keys pressed """
        self.notes = self.notes_txt.get(1.0, tk.END)
        self.player.notes = self.notes

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
        self.cloak_value_lbl = tk.Label(
            master=self.outfit_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text=self.player.cloak_name, font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.cloak_lbl.grid(row=0, column=0, sticky="nsew", pady=(2,0), padx=2)
        self.cloak_value_lbl.grid(row=1, column=0, sticky="nsew", padx=2)
        # Head
        self.head_lbl = tk.Label(master=self.outfit_field, text="Head:", font=FONT_EQUIPMENT_LBL, bg=COLOR_EQUIPMENT, anchor="n")
        self.head_value_lbl = tk.Label(master=self.outfit_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text=self.player.head_name, font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.head_lbl.grid(row=0, column=1, sticky="nsew", pady=(2,0))
        self.head_value_lbl.grid(row=1, column=1, sticky="nsew")
        # Gloves
        self.gloves_lbl = tk.Label(master=self.outfit_field, text="Gloves:", font=FONT_EQUIPMENT_LBL, bg=COLOR_EQUIPMENT, anchor="n")
        self.gloves_value_lbl = tk.Label(master=self.outfit_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text=self.player.gloves_name, font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.gloves_lbl.grid(row=0, column=2, sticky="nsew", pady=(2,0), padx=2)
        self.gloves_value_lbl.grid(row=1, column=2, sticky="nsew", padx=2)
        # Ring 1
        self.ring1_lbl = tk.Label(master=self.outfit_field, text="Ring 1:", font=FONT_EQUIPMENT_LBL, bg=COLOR_EQUIPMENT, anchor="n")
        self.ring1_value_lbl = tk.Label(master=self.outfit_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text=self.player.ring_1_name, font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.ring1_lbl.grid(row=2, column=0, sticky="nsew", pady=(2,0), padx=2)
        self.ring1_value_lbl.grid(row=3, column=0, sticky="nsew", padx=2)
        # Necklace
        self.necklace_lbl = tk.Label(master=self.outfit_field, text="Necklace:", font=FONT_EQUIPMENT_LBL, bg=COLOR_EQUIPMENT, anchor="n")
        self.necklace_value_lbl = tk.Label(master=self.outfit_field,wraplength=WRAP_EQUIPMENT_VALUE_LBL,  text=self.player.necklace_name, font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.necklace_lbl.grid(row=2, column=1, sticky="nsew", pady=(2,0))
        self.necklace_value_lbl.grid(row=3, column=1, sticky="nsew")
        # Ring 2
        self.ring2_lbl = tk.Label(master=self.outfit_field, text="Ring 2:", font=FONT_EQUIPMENT_LBL, bg=COLOR_EQUIPMENT, anchor="n")
        self.ring2_value_lbl = tk.Label(master=self.outfit_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text=self.player.ring_2_name, font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.ring2_lbl.grid(row=2, column=2, sticky="nsew", pady=(2,0), padx=2)
        self.ring2_value_lbl.grid(row=3, column=2, sticky="nsew", padx=2)
        # # Right hand
        self.right_hand_lbl = tk.Label(master=self.outfit_field, text="Right hand:", font=FONT_EQUIPMENT_LBL, bg=COLOR_EQUIPMENT, anchor="n")
        self.right_hand_value_lbl = tk.Label(master=self.outfit_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text=self.player.right_hand_name, font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.right_hand_lbl.grid(row=4, column=0, sticky="nsew", pady=(2,0), padx=2)
        self.right_hand_value_lbl.grid(row=5, column=0, sticky="nsew", padx=2)
        # Chest
        self.chest_lbl = tk.Label(master=self.outfit_field, text="Chest:", font=FONT_EQUIPMENT_LBL, bg=COLOR_EQUIPMENT, anchor="n")
        self.chest_value_lbl = tk.Label(master=self.outfit_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text=self.player.chest_name, font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.chest_lbl.grid(row=4, column=1, sticky="nsew", pady=(2,0))
        self.chest_value_lbl.grid(row=5, column=1, sticky="nsew")
        # Left hand
        self.left_hand_lbl = tk.Label(master=self.outfit_field, text="Left hand:", font=FONT_EQUIPMENT_LBL, bg=COLOR_EQUIPMENT, anchor="n")
        self.left_hand_value_lbl = tk.Label(master=self.outfit_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text=self.player.left_hand_name, font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.left_hand_lbl.grid(row=4, column=2, sticky="nsew", pady=(2,0), padx=2)
        self.left_hand_value_lbl.grid(row=5, column=2, sticky="nsew", padx=2)
        # Talisman
        self.talisman_lbl = tk.Label(master=self.outfit_field, text="Talisman:", font=FONT_EQUIPMENT_LBL, bg=COLOR_EQUIPMENT, anchor="n")
        self.talisman_value_lbl = tk.Label(master=self.outfit_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text=self.player.talisman_name, font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.talisman_lbl.grid(row=6, column=0, sticky="nsew", pady=(2,0), padx=2)
        self.talisman_value_lbl.grid(row=7, column=0, sticky="nsew", padx=2)
        # Feet
        self.feet_lbl = tk.Label(master=self.outfit_field, text="Feet:", font=FONT_EQUIPMENT_LBL, bg=COLOR_EQUIPMENT, anchor="n")
        self.feet_value_lbl = tk.Label(master=self.outfit_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text=self.player.feet_name, font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.feet_lbl.grid(row=6, column=1, sticky="nsew", pady=(2,0))
        self.feet_value_lbl.grid(row=7, column=1, sticky="nsew")
        # Money pouch
        self.money_pouch_lbl = tk.Label(master=self.outfit_field, text="Money pouch:", font=FONT_EQUIPMENT_LBL, bg=COLOR_EQUIPMENT, anchor="n")
        self.money_pouch_value_lbl = tk.Label(master=self.outfit_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text=self.player.money_pouch, font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.money_pouch_lbl.grid(row=6, column=2, sticky="nsew", pady=(2,0), padx=2)
        self.money_pouch_value_lbl.grid(row=7, column=2, sticky="nsew", padx=2)

        # Backpack
        self.backpack_lbl = tk.Label(master=self.backpack_field, text="Backpack:", font=FONT_EQUIPMENT_LBL, anchor="nw")
        self.backpack_lbl.grid(row=0, column=0, columnspan=5, sticky="nsew", padx=2)
        # Cell 1
        self.cell1_lbl = tk.Label(
            master=self.backpack_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text=self.player.backpack_cell_1_name,
            font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.cell1_lbl.grid(row=1, column=0, sticky="nsew", padx=1)
        # Cell 2
        self.cell2_lbl = tk.Label(
            master=self.backpack_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text=self.player.backpack_cell_2_name,
            font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.cell2_lbl.grid(row=1, column=1, sticky="nsew", padx=1)
        # Cell 3
        self.cell3_lbl = tk.Label(
            master=self.backpack_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text=self.player.backpack_cell_3_name,
            font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.cell3_lbl.grid(row=1, column=2, sticky="nsew", padx=1)
        # Cell 4
        self.cell4_lbl = tk.Label(
            master=self.backpack_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text=self.player.backpack_cell_4_name,
            font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.cell4_lbl.grid(row=1, column=3, sticky="nsew", padx=1)
        # Cell 5
        self.cell5_lbl = tk.Label(
            master=self.backpack_field, wraplength=WRAP_EQUIPMENT_VALUE_LBL, text=self.player.backpack_cell_5_name,
            font=FONT_EQUIPMENT_VALUE_LBL, bg=COLOR_EQUIPMENT, height=2, anchor="n")
        self.cell5_lbl.grid(row=1, column=4, sticky="nsew", padx=1)
        # Notes
        self.notes_lbl = tk.Label(master=self.backpack_field, text="Notes:", font=FONT_EQUIPMENT_LBL, anchor="nw")
        self.notes_lbl.grid(row=2, column=0, columnspan=5, sticky="nsew", padx=2)
        self.notes_txt = tk.Text(master=self.backpack_field, height=3)
        self.notes_txt.insert(1.0, self.player.notes)
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
        self.money_pouch_lbl.bind("<Button-1>", self.open_money_pouch_window)
        self.money_pouch_value_lbl.bind("<Button-1>", self.open_money_pouch_window)
        self.cell1_lbl.bind("<Button-1>", lambda e: self.open_equipment_window("Backpack cell 1:"))
        self.cell2_lbl.bind("<Button-1>", lambda e: self.open_equipment_window("Backpack cell 2:"))
        self.cell3_lbl.bind("<Button-1>", lambda e: self.open_equipment_window("Backpack cell 3:"))
        self.cell4_lbl.bind("<Button-1>", lambda e: self.open_equipment_window("Backpack cell 4:"))
        self.cell5_lbl.bind("<Button-1>", lambda e: self.open_equipment_window("Backpack cell 5:"))
        self.notes_txt.bind("<KeyRelease>", self.save_notes)

# =============================================================================================================================
    # Словарь открытых окон для каждого оборудования. Чтобы окно для каждого оборудования открывалось 1 раз.
    global opened_window
    opened_window = {}
    def open_equipment_window(self, equipment_cell_name):
        """ Открыть одно новое окно для любой ячейки в обмундировании и рюкзаке """
        # Make ID_cell from cell label name
        self.id_cell = equipment_cell_name[:-1].lower().replace(" ", "_")
        self.equip = self.define_equipment(self.id_cell)
        global opened_window
        if self.id_cell not in opened_window.keys():
            opened_window[self.id_cell] = 1
            # Если у героя нет еще оборудования, то на редактирование, а так только на посмотреть
            if self.equip["equipment_name"] == "":
                self.equipment_window = EquipmentWindow(self.root, self.player, self.id_cell, self.equip, "active")
            else:
                self.equipment_window = EquipmentWindow(self.root, self.player, self.id_cell, self.equip, "disabled")

            # Запретить пользователю взаимодействовать с основным окном
            self.equipment_window.grab_set()
            # При закрытие окна, чисть глобальную переменную
            self.equipment_window.protocol("WM_DELETE_WINDOW", lambda: self.close_equipment_window(self.id_cell))
            # Реагировать только на событие дестроя всего окна, а не каждого его виджета
            self.equipment_window.bind("<Destroy>", lambda e:self.close_equipment_window(self.id_cell) if e.widget == self.equipment_window else None)

    def close_equipment_window(self, id_cell):
        """ При закрытии окна почистить глобальную переменную, чтобы иметь возможность открывать окно снова """
        self.id_cell = id_cell
        global opened_window
        if self.id_cell in opened_window:
            opened_window.pop(self.id_cell)
        self.equipment_window.destroy()
        # Update windows fields (but firstly must forget the previuos ones)
        self.stats_hero_field.grid_forget()
        self.equipment_field.grid_forget()
        self.create_stats_hero_field()
        self.create_equipment_field()

    def define_equipment(self, id_cell):
        """ Define all attributes of specific equipment """
        #  Объект player сириализуем в строку, потом эту строку в словарь питона
        self.equip_dict = json.loads(json.dumps(self.player, default=Player.player_2_json,  ensure_ascii=False, indent=4))
        try:
            self.equip = {}
            self.equip = self.equip_dict["equipment"][id_cell]
        except Error:
            pass
        return self.equip

    def open_edit_hero_name_window(self):
        self.edit_hero_name_window = EditNameWindow(self.root, self.player)
        # Запретить пользователю взаимодействовать с основным окном
        self.edit_hero_name_window.grab_set()
        # Реагировать только на событие дестроя всего окна, а не каждого его виджета
        self.edit_hero_name_window.bind("<Destroy>", lambda e:self.close_edit_hero_name_window() if e.widget == self.edit_hero_name_window else None)

    def close_edit_hero_name_window(self):
        self.edit_hero_name_window.destroy()
        self.stats_hero_field.grid_forget()
        self.create_stats_hero_field()

    def open_money_pouch_window(self, event):
        self.money_pouch_window = MoneyPouchWindow(self.root, self.player)
        # Запретить пользователю взаимодействовать с основным окном
        self.money_pouch_window.grab_set()
        # Реагировать только на событие дестроя всего окна, а не каждого его виджета
        self.money_pouch_window.bind("<Destroy>", lambda e:self.close_money_pouch_window() if e.widget == self.money_pouch_window else None)

    def close_money_pouch_window(self):
        self.money_pouch_window.destroy()
        self.equipment_field.grid_forget()
        self.create_equipment_field()

# =============================================================================================================================
class EquipmentWindow(tk.Toplevel):
    """ Class for creating a new window for any equipment cell """
    def __init__(self, master, player, id_cell, equip: dict, state="active"):
        super().__init__()
        self.master = master
        self.player = player
        self.id_cell = id_cell
        self.equipment_cell_name = self.id_cell.title().replace("_", " ")
        self.equip = equip
        self.state = state
        self.title(f"Сharacteristics {self.equipment_cell_name}")
        self.resizable(False,False)
        self.init_gui()
        self.update()
        # Child window in the center of parent window
        master_width, master_height = tuple(int(_) for _ in self.master.winfo_geometry().split("+", 1)[0].split("x"))
        master_offset_x, master_offset_y = tuple(int(_) for _ in self.master.winfo_geometry().split('+', 1)[1].split('+'))
        child_width = self.winfo_reqwidth()
        child_height = self.winfo_reqheight()
        x = (master_width - child_width) // 2 + master_offset_x
        y = (master_height - child_height) // 2 + master_offset_y
        self.geometry(f"+{x}+{y}")

    def activate_state(self, state):
        """ Make equipment window active or not depends on emptyness of the equipment cell """
        self.state = state
        if self.state == "disabled":
            for child in self.equipment_stats_field.winfo_children():
                child.configure(state="disabled")
        elif self.state == "active":
            for child in self.equipment_stats_field.winfo_children():
                child.configure(state="normal")

    def is_equipment_name(self):
        """ Check if name is not empty """
        # self.activate_state("active")
        self.name = self.equipment_name_ent.get()
        # Must have at least one visiable character
        if self.name:
            for c in self.name:
                if c.isalnum():
                    return True
            return False
        else:
            return False

    def clear_equipment_window_forms(self):
        """ Delete information about equipment in equipment window """
        self.activate_state("active")
        self.equipment_name_ent.delete(0, tk.END)
        self.equipment_type_lst.set(self.equip["equipment_type"])
        self.equipment_speed_ent.delete(0, tk.END)
        self.equipment_brawn_ent.delete(0, tk.END)
        self.equipment_magic_ent.delete(0, tk.END)
        self.equipment_armour_ent.delete(0, tk.END)
        self.equipment_health_ent.delete(0, tk.END)

    def get_update_package(self):
        """ Collect data to update package """
        self.update_package = {}
        self.update_package["equipment_name"] = self.equipment_name_ent.get()
        self.update_package["equipment_type"] = self.equipment_type_lst.get()
        self.update_package["equipment_speed"] = self.equipment_speed_ent.get()
        self.update_package["equipment_brawn"] = self.equipment_brawn_ent.get()
        self.update_package["equipment_magic"] = self.equipment_magic_ent.get()
        self.update_package["equipment_armour"] = self.equipment_armour_ent.get()
        self.update_package["equipment_health"] = self.equipment_health_ent.get()
        for key, value in self.update_package.items():
            if key in ("equipment_speed", "equipment_brawn", "equipment_magic", "equipment_armour", "equipment_health"):
                try:
                    self.update_package[key] = int(value)
                except ValueError:
                    self.update_package[key] = 0
        return self.update_package

    def operate_puton_apply_btn(self):
        """ Обработка нажатия кнопки "Put on\Apply" """
        puton_values = ["cloak", "head", "gloves", "ring_1", "necklace", "ring_2", "right_hand", "chest", "left_hand", "talisman", "feet"]
        # Если открыли уже надетое оборудование, то просто закрыть
        if self.state == "disabled" and self.id_cell in puton_values:
            self.destroy()
            return
        # Если нет имени, то ничего не делать, пока не будет имя оборудования
        if not self.is_equipment_name():
            self.equipment_name_ent.config(bg="red")
            return

        self.update_package = self.get_update_package()
        if self.update_package["equipment_type"] == self.id_cell:
            self.player.update_player(self.id_cell, self.update_package)
            self.destroy()
            return
        elif self.update_package["equipment_type"] in puton_values:
            if self.is_empty_equipment_cell(self.update_package["equipment_type"]):
                self.player.update_player(self.update_package["equipment_type"], self.update_package)

                # Очистить ячейку рюкзака
                self.clear_cell()
                self.destroy()
                return
            else:
                info_msg = tk.messagebox.showinfo(title="Info", message=f'You have already put on {self.update_package["equipment_type"]} equipment. Put it in your backpack first or throw it away')
        # Значит зелье. Необходимо применить один раз
        else:
            self.player.update_modifiers(self.update_package)
            # Очистить ячейку рюкзака
            self.clear_cell()
            self.destroy()
            return

    def clear_cell(self):
        """ Clear equipment cell """
        self.clear_equipment_window_forms()
        self.update_package  = self.get_update_package()
        self.player.update_player(self.id_cell, self.update_package)

    def operate_throw_away_btn(self):
        """ Обработка нажатия кнопки "Throw away" """
        if self.state == "disabled":
            self.clear_cell()
        self.destroy()

    def find_empty_backpack_cell(self):
        """ Find empty space in backpack to add new equipment """
        # Лист возможных значение для ячеек рюкзака
        self.backpack_cells = {
            "backpack_cell_1": self.player.backpack_cell_1_name,
            "backpack_cell_2": self.player.backpack_cell_2_name,
            "backpack_cell_3": self.player.backpack_cell_3_name,
            "backpack_cell_4": self.player.backpack_cell_4_name,
            "backpack_cell_5": self.player.backpack_cell_5_name
        }
        for k, v in self.backpack_cells.items():
            if v == "":
                return k
        return False

    def is_empty_equipment_cell(self, id_cell):
        """ check if equipment cell is empty """
        equipment_name = str(id_cell) + "_name"
        if self.player.__dict__[equipment_name]:
            return False
        return True

    def operate_in_backpack_btn(self):
        # Если уже в рюкзаке, то просто закрыть (убрать обратно в рюкзак)
        if self.id_cell in ("backpack_cell_1", "backpack_cell_2", "backpack_cell_3", "backpack_cell_4", "backpack_cell_5"):
            if self.state == "disabled":
                return self.destroy()
            elif self.state == "active":
                if not self.is_equipment_name():
                    self.equipment_name_ent.config(bg="red")
                    return
            self.update_package = self.get_update_package()
            self.player.update_player(self.id_cell, self.update_package)
            self.destroy()
        # Если открыта ячейка оборудования и мы хотим убрать его в рюкзак
        else:
            # Ищем место в рюкзаке
            self.empty_backpack_cell = self.find_empty_backpack_cell()
            if not self.empty_backpack_cell:
                info_msg = tk.messagebox.showinfo(title="Info", message="You don't have empty space in your backpack")
            else:
                if self.state == "active":
                    if not self.is_equipment_name():
                        self.equipment_name_ent.config(bg="red")
                        return
                    self.update_package = self.get_update_package()
                    self.player.update_player(self.empty_backpack_cell, self.update_package)
                    self.destroy()
                elif self.state == "disabled":
                    self.update_package = self.get_update_package()
                    self.player.update_player(self.empty_backpack_cell, self.update_package)
                    # Снять с себя одетую вещь
                    self.clear_cell()
                    self.destroy()

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
        self.equipment_stats_field.rowconfigure([0, 1, 2], weight=1)
        self.equipment_stats_field.columnconfigure([0,1,2,3,4,5,6,7,8,9], weight=1)
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
        self.equipment_cell_name_lbl = tk.Label(master=self.equipment_cell_name_field, text=f"{self.equipment_cell_name}:", font=FONT_STATS)
        self.equipment_cell_name_lbl.grid(row=0, sticky="w")
        # Equipment stats
        self.equipment_name_lbl = tk.Label(self.equipment_stats_field, text="Name:", font=FONT_STATS)
        self.equipment_name_lbl.grid(row=0, sticky="nw", columnspan=2)
        self.equipment_name_ent = tk.Entry(self.equipment_stats_field, font=FONT_EQUIPMENT_VALUE_LBL)
        self.equipment_name_ent.grid(row=0, sticky="nwe", column=2, columnspan=8)
        self.equipment_name_ent.insert(0, self.equip["equipment_name"])
        self.equipment_type_lbl = tk.Label(self.equipment_stats_field, text="Type:", font=FONT_STATS)
        self.equipment_type_lbl.grid(row=1, sticky="nw", columnspan=2)
        self.equipment_type_lst = ttk.Combobox(self.equipment_stats_field,
        values = [
            "cloak", "head","gloves",
            "ring_1", "necklace", "ring_2",
            "right_hand", "chest", "left_hand",
            "talisman", "feet",
            "potion", "other"
        ],
        state="readonly"
        )
        self.equipment_type_lst.set(self.equip["equipment_type"])
        self.equipment_type_lst.grid(row=1, sticky="nw", column=2, columnspan=4)
        self.equipment_speed_lbl = tk.Label(self.equipment_stats_field, text=f"{ICON_SPEED}", font=FONT_STATS)
        self.equipment_speed_lbl.grid(row=2, column=0, sticky="e")
        self.equipment_speed_ent = tk.Entry(self.equipment_stats_field, width=2, font=FONT_STATS)
        self.equipment_speed_ent.insert(0, self.equip["equipment_speed"])
        self.equipment_speed_ent.grid(row=2, column=1, sticky="ew")
        self.equipment_brawn_lbl = tk.Label(self.equipment_stats_field, text=f"{ICON_BRAWN}", font=FONT_STATS)
        self.equipment_brawn_lbl.grid(row=2, column=2, sticky="e")
        self.equipment_brawn_ent = tk.Entry(self.equipment_stats_field, width=2, font=FONT_STATS)
        self.equipment_brawn_ent.insert(0, self.equip["equipment_brawn"])
        self.equipment_brawn_ent.grid(row=2, column=3, sticky="ew")
        self.equipment_magic_lbl = tk.Label(self.equipment_stats_field, text=f"{ICON_MAGIC}", font=FONT_STATS)
        self.equipment_magic_lbl.grid(row=2, column=4, sticky="e")
        self.equipment_magic_ent = tk.Entry(self.equipment_stats_field, width=2, font=FONT_STATS)
        self.equipment_magic_ent.insert(0, self.equip["equipment_magic"])
        self.equipment_magic_ent.grid(row=2, column=5, sticky="ew")
        self.equipment_armour_lbl = tk.Label(self.equipment_stats_field, text=f"{ICON_ARMOUR}", font=FONT_STATS)
        self.equipment_armour_lbl.grid(row=2, column=6, sticky="e")
        self.equipment_armour_ent = tk.Entry(self.equipment_stats_field, width=2, font=FONT_STATS)
        self.equipment_armour_ent.insert(0, self.equip["equipment_armour"])
        self.equipment_armour_ent.grid(row=2, column=7, sticky="ew")
        self.equipment_health_lbl = tk.Label(self.equipment_stats_field, text=f"{ICON_HEALTH}", fg="red", font=FONT_STATS)
        self.equipment_health_lbl.grid(row=2, column=8, sticky="e")
        self.equipment_health_ent = tk.Entry(self.equipment_stats_field, width=2, font=FONT_STATS)
        self.equipment_health_ent.insert(0, self.equip["equipment_health"])
        self.equipment_health_ent.grid(row=2, column=9, sticky="ew")
        # Buttons
        self.put_on_btn = tk.Button(master=self.buttons_field, text="Put on/Apply", command=self.operate_puton_apply_btn)
        self.throw_away_btn = tk.Button(master=self.buttons_field, text="Throw away", command=self.operate_throw_away_btn)
        self.in_backpack_btn = tk.Button(master=self.buttons_field, text="In backpack", command=self.operate_in_backpack_btn)
        self.put_on_btn.grid(row=0, column=0, sticky="nsew", padx=5)
        self.throw_away_btn.grid(row=0, column=1, sticky="nsew", padx=5)
        self.in_backpack_btn.grid(row=0, column=2, sticky="nsew", padx=5)
        # Activate state of window
        self.activate_state(self.state)
# =============================================================================================================================
class EditNameWindow(tk.Toplevel):
    """ Window for editing hero's name, path, career """
    def __init__(self, master, player):
        super().__init__()
        self.master = master
        self.player = player
        self.title(f"Edit Hero's name, path, career")
        self.resizable(False,False)
        self.init_gui()
        self.update()
        # Child window in the center of parent window
        master_width, master_height = tuple(int(_) for _ in self.master.winfo_geometry().split("+", 1)[0].split("x"))
        master_offset_x, master_offset_y = tuple(int(_) for _ in self.master.winfo_geometry().split('+', 1)[1].split('+'))
        child_width = self.winfo_reqwidth()
        child_height = self.winfo_reqheight()
        x = (master_width - child_width) // 2 + master_offset_x
        y = (master_height - child_height) // 2 + master_offset_y
        self.geometry(f"+{x}+{y}")

    def is_hero_name(self):
        """ Check if hero name is not empty """
        self.name = self.hero_name_ent.get()
        # Must have at least one visiable character
        if self.name:
            for c in self.name:
                if c.isalnum():
                    return True
            return False
        else:
            return False

    def operate_save_btn(self):
        self.name = self.hero_name_ent.get()
        self.path = self.hero_path_lst.get()
        self.career = self.hero_career_ent.get()
        if not self.is_hero_name():
            self.hero_name_ent.config(bg="red")
            return
        if self.path not in PATH_LIST:
            tk.messagebox.showinfo(title="Info", message=f'Your hero path {self.path} is not valid!')
            return
        self.player.name = self.name
        self.player.path = self.path
        self.player.career = self.career
        self.destroy()

    def init_gui(self):
        """ Create window GUI """
        # Create mainframe
        self.mainframe = tk.Frame(self)
        self.mainframe.rowconfigure([0, 1], weight=1)
        self.mainframe.columnconfigure(0, weight=1)
        # Create edit hero frame
        self.edit_hero_field = tk.Frame(self.mainframe)
        self.edit_hero_field.rowconfigure([0, 1], weight=1)
        self.edit_hero_field.columnconfigure([0, 1, 2, 3], weight=1)
        # Create buttons frame
        self.buttons_field = tk.Frame(self.mainframe)
        self.buttons_field.rowconfigure(0, weight=1)
        self.buttons_field.columnconfigure([0, 1], weight=1)
        # Frames grid
        self.mainframe.grid(padx=3)
        self.edit_hero_field.grid(row=0, sticky="nsew", padx=5, pady=5)
        self.buttons_field.grid(row=1, sticky="nsew", padx=5, pady=(10,5))
        # Edit hero
        self.hero_name_lbl = tk.Label(self.edit_hero_field, text="Name:", font=FONT_STATS)
        self.hero_name_lbl.grid(row=0, column=0, sticky="nw")
        self.hero_name_ent = tk.Entry(self.edit_hero_field, font=FONT_EQUIPMENT_VALUE_LBL)
        self.hero_name_ent.grid(row=0, sticky="nwe", column=1, columnspan=3)
        self.hero_name_ent.insert(0, self.player.name)
        self.hero_path_lbl = tk.Label(self.edit_hero_field, text="Path:", font=FONT_STATS)
        self.hero_path_lbl.grid(row=1, column=0, sticky="nw")
        self.hero_path_lst = ttk.Combobox(self.edit_hero_field, values = PATH_LIST, state="readonly")
        self.hero_path_lst.set(self.player.path)
        self.hero_path_lst.grid(row=1, column=1, sticky="nw")
        self.hero_career_lbl = tk.Label(self.edit_hero_field, text="Career:", font=FONT_STATS)
        self.hero_career_lbl.grid(row=1, column=2, sticky="nw")
        self.hero_career_ent = tk.Entry(self.edit_hero_field, font=FONT_EQUIPMENT_VALUE_LBL)
        self.hero_career_ent.insert(0, self.player.career)
        self.hero_career_ent.grid(row=1, column=3, sticky="nwe")
        # Buttons
        self.save_btn = tk.Button(master=self.buttons_field, text="Save", command=self.operate_save_btn)
        self.cancel_btn = tk.Button(master=self.buttons_field, text="Cancel", command=self.destroy)
        self.save_btn.grid(row=0, column=0, sticky="nsew", padx=5)
        self.cancel_btn.grid(row=0, column=1, sticky="nsew", padx=5)
# =============================================================================================================================
class MoneyPouchWindow(tk.Toplevel):
    """ Window for editing money pouch """
    def __init__(self, master, player):
        super().__init__()
        self.master = master
        self.player = player
        self.title(f"Money pouch")
        self.resizable(False,False)
        self.init_gui()
        self.update()
        # Child window in the center of parent window
        master_width, master_height = tuple(int(_) for _ in self.master.winfo_geometry().split("+", 1)[0].split("x"))
        master_offset_x, master_offset_y = tuple(int(_) for _ in self.master.winfo_geometry().split('+', 1)[1].split('+'))
        child_width = self.winfo_reqwidth()
        child_height = self.winfo_reqheight()
        x = (master_width - child_width) // 2 + master_offset_x
        y = (master_height - child_height) // 2 + master_offset_y
        self.geometry(f"+{x}+{y}")

    def operate_save_btn(self):
        try:
            self.money = int(self.money_pouch_sbx.get())
            self.player.money_pouch = self.money
            self.destroy()
        except ValueError:
            tk.messagebox.showinfo(title="Info", message=f"It's not a number!")
            return

    def init_gui(self):
        """ Create window GUI """
        # Create mainframe
        self.mainframe = tk.Frame(self)
        self.mainframe.rowconfigure([0, 1], weight=1)
        self.mainframe.columnconfigure(0, weight=1)
        # Create edit hero frame
        self.money_field = tk.Frame(self.mainframe)
        self.money_field.rowconfigure(0, weight=1)
        self.money_field.columnconfigure([0, 1], weight=1)
        # Create buttons frame
        self.buttons_field = tk.Frame(self.mainframe)
        self.buttons_field.rowconfigure(0, weight=1)
        self.buttons_field.columnconfigure([0, 1], weight=1)
        # Frames grid
        self.mainframe.grid(padx=3)
        self.money_field.grid(row=0, sticky="nsew", padx=5, pady=5)
        self.buttons_field.grid(row=1, sticky="nsew", padx=5, pady=(10,5))
        # Edit money
        self.money_pouch_lbl = tk.Label(self.money_field, text=f"{ICON_MONEY_BAG}", font=FONT_STATS)
        self.money_pouch_lbl.grid(row=0, column=0, sticky="nw")
        self.money_pouch_sbx = ttk.Spinbox(self.money_field, from_=0, to=MAX_MONEY, increment=1, font=FONT_EQUIPMENT_VALUE_LBL)
        self.money_pouch_sbx.grid(row=0, sticky="nwe", column=1)
        self.money_pouch_sbx.insert(0, self.player.money_pouch)
        # Buttons
        self.save_btn = tk.Button(master=self.buttons_field, text="Save", command=self.operate_save_btn)
        self.cancel_btn = tk.Button(master=self.buttons_field, text="Cancel", command=self.destroy)
        self.save_btn.grid(row=0, column=0, sticky="nsew", padx=5)
        self.cancel_btn.grid(row=0, column=1, sticky="nsew", padx=5)

def main():
    root = tk.Tk()
    DestinyQuest(root)
    root.mainloop()

if __name__ == "__main__":
    main()
