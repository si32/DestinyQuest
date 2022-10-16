# Новый герой
empty_hero = {
  "name": "Новый герой",
  "path": "",
  "career": "",
  "characteristics": {
    "speed": 0,
    "brawn": 0,
    "magic": 0,
    "armour": 0,
    "health": 30
  },
  "money_pouch": 0,
  "equipment": {
    "cloak": {
      "equipment_name": "",
      "equipment_speed": 0,
      "equipment_brawn": 0,
      "equipment_magic": 0,
      "equipment_armour": 0,
      "equipment_special_abilities": {
        "special_ability_name": "",
        "special_ability_type": "",
        "special_ability_description": ""
      }
    },
    "head": {
      "equipment_name": "",
      "equipment_speed": 0,
      "equipment_brawn": 0,
      "equipment_magic": 0,
      "equipment_armour": 0,
      "equipment_special_abilities": {
        "special_ability_name": "",
        "special_ability_type": "",
        "special_ability_description": ""
      }
    },
    "gloves": {
      "equipment_name": "",
      "equipment_speed": 0,
      "equipment_brawn": 0,
      "equipment_magic": 0,
      "equipment_armour": 0,
      "equipment_special_abilities": {
        "special_ability_name": "",
        "special_ability_type": "",
        "special_ability_description": ""
      }
    },
    "right_hand": {
      "equipment_name": "",
      "equipment_speed": 0,
      "equipment_brawn": 0,
      "equipment_magic": 0,
      "equipment_armour": 0,
      "equipment_special_abilities": {
        "special_ability_name": "",
        "special_ability_type": "",
        "special_ability_description": ""
      }
    },
    "chest": {
      "equipment_name": "",
      "equipment_speed": 0,
      "equipment_brawn": 0,
      "equipment_magic": 0,
      "equipment_armour": 0,
      "equipment_special_abilities": {
        "special_ability_name": "",
        "special_ability_type": "",
        "special_ability_description": ""
      }
    },
    "left_hand": {
      "equipment_name": "",
      "equipment_speed": 0,
      "equipment_brawn": 0,
      "equipment_magic": 0,
      "equipment_armour": 0,
      "equipment_special_abilities": {
        "special_ability_name": "",
        "special_ability_type": "",
        "special_ability_description": ""
      }
    },
    "talisman": {
      "equipment_name": "",
      "equipment_speed": 0,
      "equipment_brawn": 0,
      "equipment_magic": 0,
      "equipment_armour": 0,
      "equipment_special_abilities": {
        "special_ability_name": "",
        "special_ability_type": "",
        "special_ability_description": ""
      }
    },
    "feet": {
      "equipment_name": "",
      "equipment_speed": 0,
      "equipment_brawn": 0,
      "equipment_magic": 0,
      "equipment_armour": 0,
      "equipment_special_abilities": {
        "special_ability_name": "",
        "special_ability_type": "",
        "special_ability_description": ""
      }
    },
    "necklace": {
      "equipment_name": "",
      "equipment_speed": 0,
      "equipment_brawn": 0,
      "equipment_magic": 0,
      "equipment_armour": 0,
      "equipment_special_abilities": {
        "special_ability_name": "",
        "special_ability_type": "",
        "special_ability_description": ""
      }
    },
    "ring_0": {
      "equipment_name": "",
      "equipment_speed": 0,
      "equipment_brawn": 0,
      "equipment_magic": 0,
      "equipment_armour": 0,
      "equipment_special_abilities": {
        "special_ability_name": "",
        "special_ability_type": "",
        "special_ability_description": ""
      }
    },
    "ring_2": {
      "equipment_name": "",
      "equipment_speed": 0,
      "equipment_brawn": 0,
      "equipment_magic": 0,
      "equipment_armour": 0,
      "equipment_special_abilities": {
        "special_ability_name": "",
        "special_ability_type": "",
        "special_ability_description": ""
      }
    }
  },
  "special_abilities": {
    "speed_special_abilities": {
      "speed_special_ability_name": "",
      "speed_special_ability_description": ""
    },
    "combat_special_abilities": {
      "combat_special_ability_name": "",
      "combat_special_ability_description": ""
    },
    "passive_special_abilities": {
      "passive_special_ability_name": "",
      "passive_special_ability_description": ""
    },
    "modifier_special_abilities": {
      "modifier_special_ability_name": "",
      "modifier_special_ability_description": ""
    }
  },
  "backpack": {
    "backpack_cell_0": {
      "backpack_cell_0_name": "",
      "backpack_cell_0_description": ""
    },
    "backpack_cell_2": {
      "backpack_cell_2_name": "",
      "backpack_cell_2_description": ""
    },
    "backpack_cell_3": {
      "backpack_cell_3_name": "",
      "backpack_cell_3_description": ""
    },
    "backpack_cell_4": {
      "backpack_cell_4_name": "",
      "backpack_cell_4_description": ""
    },
    "backpack_cell_5": {
      "backpack_cell_5_name": "",
      "backpack_cell_5_description": ""
    }
  },
  "comments": ""
}


# Класс героя, чтобы иметь доступ к атрибутам через точку, а не как json ["attr"]
class Player:
    def __init__(self, hero=empty_hero):
        self.name = hero["name"]
        self.path = hero["path"]
        self.career = hero["career"]
        self.speed = hero["characteristics"]["speed"]
        self.brawn = hero["characteristics"]["brawn"]
        self.magic = hero["characteristics"]["magic"]
        self.armour = hero["characteristics"]["armour"]
        self.health = hero["characteristics"]["health"]

    def player_2_json(self):
      """ Для сериализации объекта Player в json при сохранении файла героя """
      return {
          "name": self.name,
          "path": self.path,
          "career": self.career,
          "characteristics": {
            "speed": self.speed,
            "brawn": self.brawn,
            "magic": self.magic,
            "armour": self.armour,
            "health": self.health
          },
          "money_pouch": 0,
          "equipment": {
            "cloak": {
              "equipment_name": "",
              "equipment_speed": 0,
              "equipment_brawn": 0,
              "equipment_magic": 0,
              "equipment_armour": 0,
              "equipment_special_abilities": {
                "special_ability_name": "",
                "special_ability_type": "",
                "special_ability_description": ""
              }
            },
            "head": {
              "equipment_name": "",
              "equipment_speed": 0,
              "equipment_brawn": 0,
              "equipment_magic": 0,
              "equipment_armour": 0,
              "equipment_special_abilities": {
                "special_ability_name": "",
                "special_ability_type": "",
                "special_ability_description": ""
              }
            },
            "gloves": {
              "equipment_name": "",
              "equipment_speed": 0,
              "equipment_brawn": 0,
              "equipment_magic": 0,
              "equipment_armour": 0,
              "equipment_special_abilities": {
                "special_ability_name": "",
                "special_ability_type": "",
                "special_ability_description": ""
              }
            },
            "right_hand": {
              "equipment_name": "",
              "equipment_speed": 0,
              "equipment_brawn": 0,
              "equipment_magic": 0,
              "equipment_armour": 0,
              "equipment_special_abilities": {
                "special_ability_name": "",
                "special_ability_type": "",
                "special_ability_description": ""
              }
            },
            "chest": {
              "equipment_name": "",
              "equipment_speed": 0,
              "equipment_brawn": 0,
              "equipment_magic": 0,
              "equipment_armour": 0,
              "equipment_special_abilities": {
                "special_ability_name": "",
                "special_ability_type": "",
                "special_ability_description": ""
              }
            },
            "left_hand": {
              "equipment_name": "",
              "equipment_speed": 0,
              "equipment_brawn": 0,
              "equipment_magic": 0,
              "equipment_armour": 0,
              "equipment_special_abilities": {
                "special_ability_name": "",
                "special_ability_type": "",
                "special_ability_description": ""
              }
            },
            "talisman": {
              "equipment_name": "",
              "equipment_speed": 0,
              "equipment_brawn": 0,
              "equipment_magic": 0,
              "equipment_armour": 0,
              "equipment_special_abilities": {
                "special_ability_name": "",
                "special_ability_type": "",
                "special_ability_description": ""
              }
            },
            "feet": {
              "equipment_name": "",
              "equipment_speed": 0,
              "equipment_brawn": 0,
              "equipment_magic": 0,
              "equipment_armour": 0,
              "equipment_special_abilities": {
                "special_ability_name": "",
                "special_ability_type": "",
                "special_ability_description": ""
              }
            },
            "necklace": {
              "equipment_name": "",
              "equipment_speed": 0,
              "equipment_brawn": 0,
              "equipment_magic": 0,
              "equipment_armour": 0,
              "equipment_special_abilities": {
                "special_ability_name": "",
                "special_ability_type": "",
                "special_ability_description": ""
              }
            },
            "ring_0": {
              "equipment_name": "",
              "equipment_speed": 0,
              "equipment_brawn": 0,
              "equipment_magic": 0,
              "equipment_armour": 0,
              "equipment_special_abilities": {
                "special_ability_name": "",
                "special_ability_type": "",
                "special_ability_description": ""
              }
            },
            "ring_2": {
              "equipment_name": "",
              "equipment_speed": 0,
              "equipment_brawn": 0,
              "equipment_magic": 0,
              "equipment_armour": 0,
              "equipment_special_abilities": {
                "special_ability_name": "",
                "special_ability_type": "",
                "special_ability_description": ""
              }
            }
          },
          "special_abilities": {
            "speed_special_abilities": {
              "speed_special_ability_name": "",
              "speed_special_ability_description": ""
            },
            "combat_special_abilities": {
              "combat_special_ability_name": "",
              "combat_special_ability_description": ""
            },
            "passive_special_abilities": {
              "passive_special_ability_name": "",
              "passive_special_ability_description": ""
            },
            "modifier_special_abilities": {
              "modifier_special_ability_name": "",
              "modifier_special_ability_description": ""
            }
          },
          "backpack": {
            "backpack_cell_0": {
              "backpack_cell_0_name": "",
              "backpack_cell_0_description": ""
            },
            "backpack_cell_2": {
              "backpack_cell_2_name": "",
              "backpack_cell_2_description": ""
            },
            "backpack_cell_3": {
              "backpack_cell_3_name": "",
              "backpack_cell_3_description": ""
            },
            "backpack_cell_4": {
              "backpack_cell_4_name": "",
              "backpack_cell_4_description": ""
            },
            "backpack_cell_5": {
              "backpack_cell_5_name": "",
              "backpack_cell_5_description": ""
            }
          },
          "comments": ""
      }
