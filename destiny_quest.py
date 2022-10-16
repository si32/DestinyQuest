import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import random
import json
import sys
from player import empty_hero, Player

# Чтобы русские символы из json в stdout нормально отображались
sys.stdout.reconfigure(encoding='cp1251')

PROGRAM_NAME = "Destiny Quest Hero List"

FONT_STATS = ("Courier New", 13, "bold")
FONT_SIZE_CHARACTERISTICS = ("Courier New", 13, "bold")
FONT_DICES_RESULT = ("Courier New", 25, "bold")
FONT_DICES_BUTTON = ("Courier New", 10)

BG_MAINFRAME = "#fce3ff"
COLOR_AGILITY = "#c1f797"
COLOR_ATTACK = "#e0807b"
COLOR_TEST = "#7cc7f5"
COLOR_REFRESH = "#dbdbdb"

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
            print("done!")
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
        self.damage = attack_result - self.armour
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
        self.mainframe = tk.Frame(self.root, bg=BG_MAINFRAME)
        self.mainframe.rowconfigure([0, 1, 2, 3], weight=1)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.grid(padx=3)

    def create_stats_field(self):
        """ Top general statistic field """
        # Frames
        self.stats_field = tk.Frame(self.mainframe)
        self.stats_field.rowconfigure(0, weight=1)
        self.stats_field.columnconfigure(0, weight=1)
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

# class equipment(tk.Frame):
#     def __init__(self):
#         super().__init__()


# =============================================================================================================================
def main():
    root = tk.Tk()
    DestinyQuest(root)
    root.mainloop()

if __name__ == "__main__":
    main()
