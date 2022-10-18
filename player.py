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
  "money_pouch": 10,
  "equipment": {
    "cloak": {
      "equipment_name": "",
      "equipment_type": "cloak",
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
      "equipment_type": "head",
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
      "equipment_type": "gloves",
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
      "equipment_type": "right_hand",
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
      "equipment_type": "chest",
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
      "equipment_type": "left_hand",
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
      "equipment_type": "talisman",
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
      "equipment_type": "feet",
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
      "equipment_type": "necklace",
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
    "ring_1": {
      "equipment_name": "",
      "equipment_type": "ring_1",
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
      "equipment_type": "ring_2",
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
  "backpack": {
    "backpack_cell_1": {
      "equipment_name": "",
      "equipment_type": "",
      "equipment_speed": 0,
      "equipment_brawn": 0,
      "equipment_magic": 0,
      "equipment_armour": 0
    },
    "backpack_cell_2": {
      "equipment_name": "",
      "equipment_type": "",
      "equipment_speed": 0,
      "equipment_brawn": 0,
      "equipment_magic": 0,
      "equipment_armour": 0
    },
    "backpack_cell_3": {
      "equipment_name": "",
      "equipment_type": "",
      "equipment_speed": 0,
      "equipment_brawn": 0,
      "equipment_magic": 0,
      "equipment_armour": 0
    },
    "backpack_cell_4": {
      "equipment_name": "",
      "equipment_type": "",
      "equipment_speed": 0,
      "equipment_brawn": 0,
      "equipment_magic": 0,
      "equipment_armour": 0
    },
    "backpack_cell_5": {
      "equipment_name": "",
      "equipment_type": "",
      "equipment_speed": 0,
      "equipment_brawn": 0,
      "equipment_magic": 0,
      "equipment_armour": 0
    }
  },
  "notes": "",
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
  }
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

        self.cloak_name = hero["equipment"]["cloak"]["equipment_name"]
        self.cloak_type = hero["equipment"]["cloak"]["equipment_type"]
        self.cloak_speed = hero["equipment"]["cloak"]["equipment_speed"]
        self.cloak_brawn = hero["equipment"]["cloak"]["equipment_brawn"]
        self.cloak_magic = hero["equipment"]["cloak"]["equipment_magic"]
        self.cloak_armour = hero["equipment"]["cloak"]["equipment_armour"]
        self.head_name = hero["equipment"]["head"]["equipment_name"]
        self.head_type = hero["equipment"]["head"]["equipment_type"]
        self.head_speed = hero["equipment"]["head"]["equipment_speed"]
        self.head_brawn = hero["equipment"]["head"]["equipment_brawn"]
        self.head_magic = hero["equipment"]["head"]["equipment_magic"]
        self.head_armour = hero["equipment"]["head"]["equipment_armour"]
        self.gloves_name = hero["equipment"]["gloves"]["equipment_name"]
        self.gloves_type = hero["equipment"]["gloves"]["equipment_type"]
        self.gloves_speed = hero["equipment"]["gloves"]["equipment_speed"]
        self.gloves_brawn = hero["equipment"]["gloves"]["equipment_brawn"]
        self.gloves_magic = hero["equipment"]["gloves"]["equipment_magic"]
        self.gloves_armour = hero["equipment"]["gloves"]["equipment_armour"]
        self.ring_1_name = hero["equipment"]["ring_1"]["equipment_name"]
        self.ring_1_type = hero["equipment"]["ring_1"]["equipment_type"]
        self.ring_1_speed = hero["equipment"]["ring_1"]["equipment_speed"]
        self.ring_1_brawn = hero["equipment"]["ring_1"]["equipment_brawn"]
        self.ring_1_magic = hero["equipment"]["ring_1"]["equipment_magic"]
        self.ring_1_armour = hero["equipment"]["ring_1"]["equipment_armour"]
        self.necklace_name = hero["equipment"]["necklace"]["equipment_name"]
        self.necklace_type = hero["equipment"]["necklace"]["equipment_type"]
        self.necklace_speed = hero["equipment"]["necklace"]["equipment_speed"]
        self.necklace_brawn = hero["equipment"]["necklace"]["equipment_brawn"]
        self.necklace_magic = hero["equipment"]["necklace"]["equipment_magic"]
        self.necklace_armour = hero["equipment"]["necklace"]["equipment_armour"]
        self.ring_2_name = hero["equipment"]["ring_2"]["equipment_name"]
        self.ring_2_type = hero["equipment"]["ring_2"]["equipment_type"]
        self.ring_2_speed = hero["equipment"]["ring_2"]["equipment_speed"]
        self.ring_2_brawn = hero["equipment"]["ring_2"]["equipment_brawn"]
        self.ring_2_magic = hero["equipment"]["ring_2"]["equipment_magic"]
        self.ring_2_armour = hero["equipment"]["ring_2"]["equipment_armour"]
        self.right_hand_name = hero["equipment"]["right_hand"]["equipment_name"]
        self.right_hand_type = hero["equipment"]["right_hand"]["equipment_type"]
        self.right_hand_speed = hero["equipment"]["right_hand"]["equipment_speed"]
        self.right_hand_brawn = hero["equipment"]["right_hand"]["equipment_brawn"]
        self.right_hand_magic = hero["equipment"]["right_hand"]["equipment_magic"]
        self.right_hand_armour = hero["equipment"]["right_hand"]["equipment_armour"]
        self.chest_name = hero["equipment"]["chest"]["equipment_name"]
        self.chest_type = hero["equipment"]["chest"]["equipment_type"]
        self.chest_speed = hero["equipment"]["chest"]["equipment_speed"]
        self.chest_brawn = hero["equipment"]["chest"]["equipment_brawn"]
        self.chest_magic = hero["equipment"]["chest"]["equipment_magic"]
        self.chest_armour = hero["equipment"]["chest"]["equipment_armour"]
        self.left_hand_name = hero["equipment"]["left_hand"]["equipment_name"]
        self.left_hand_type = hero["equipment"]["left_hand"]["equipment_type"]
        self.left_hand_speed = hero["equipment"]["left_hand"]["equipment_speed"]
        self.left_hand_brawn = hero["equipment"]["left_hand"]["equipment_brawn"]
        self.left_hand_magic = hero["equipment"]["left_hand"]["equipment_magic"]
        self.left_hand_armour = hero["equipment"]["left_hand"]["equipment_armour"]
        self.talisman_name = hero["equipment"]["talisman"]["equipment_name"]
        self.talisman_type = hero["equipment"]["talisman"]["equipment_type"]
        self.talisman_speed = hero["equipment"]["talisman"]["equipment_speed"]
        self.talisman_brawn = hero["equipment"]["talisman"]["equipment_brawn"]
        self.talisman_magic = hero["equipment"]["talisman"]["equipment_magic"]
        self.talisman_armour = hero["equipment"]["talisman"]["equipment_armour"]
        self.feet_name = hero["equipment"]["feet"]["equipment_name"]
        self.feet_type = hero["equipment"]["feet"]["equipment_type"]
        self.feet_speed = hero["equipment"]["feet"]["equipment_speed"]
        self.feet_brawn = hero["equipment"]["feet"]["equipment_brawn"]
        self.feet_magic = hero["equipment"]["feet"]["equipment_magic"]
        self.feet_armour = hero["equipment"]["feet"]["equipment_armour"]
        self.money_pouch = hero["money_pouch"]

        self.backpack_cell_1_name = hero["backpack"]["backpack_cell_1"]["equipment_name"]
        self.backpack_cell_1_type = hero["backpack"]["backpack_cell_1"]["equipment_type"]
        self.backpack_cell_1_speed = hero["backpack"]["backpack_cell_1"]["equipment_speed"]
        self.backpack_cell_1_brawn = hero["backpack"]["backpack_cell_1"]["equipment_brawn"]
        self.backpack_cell_1_magic = hero["backpack"]["backpack_cell_1"]["equipment_magic"]
        self.backpack_cell_1_armour = hero["backpack"]["backpack_cell_1"]["equipment_armour"]
        self.backpack_cell_2_name = hero["backpack"]["backpack_cell_2"]["equipment_name"]
        self.backpack_cell_2_type = hero["backpack"]["backpack_cell_2"]["equipment_type"]
        self.backpack_cell_2_speed = hero["backpack"]["backpack_cell_2"]["equipment_speed"]
        self.backpack_cell_2_brawn = hero["backpack"]["backpack_cell_2"]["equipment_brawn"]
        self.backpack_cell_2_magic = hero["backpack"]["backpack_cell_2"]["equipment_magic"]
        self.backpack_cell_2_armour = hero["backpack"]["backpack_cell_2"]["equipment_armour"]
        self.backpack_cell_3_name = hero["backpack"]["backpack_cell_3"]["equipment_name"]
        self.backpack_cell_3_type = hero["backpack"]["backpack_cell_3"]["equipment_type"]
        self.backpack_cell_3_speed = hero["backpack"]["backpack_cell_3"]["equipment_speed"]
        self.backpack_cell_3_brawn = hero["backpack"]["backpack_cell_3"]["equipment_brawn"]
        self.backpack_cell_3_magic = hero["backpack"]["backpack_cell_3"]["equipment_magic"]
        self.backpack_cell_3_armour = hero["backpack"]["backpack_cell_3"]["equipment_armour"]
        self.backpack_cell_4_name = hero["backpack"]["backpack_cell_4"]["equipment_name"]
        self.backpack_cell_4_type = hero["backpack"]["backpack_cell_4"]["equipment_type"]
        self.backpack_cell_4_speed = hero["backpack"]["backpack_cell_4"]["equipment_speed"]
        self.backpack_cell_4_brawn = hero["backpack"]["backpack_cell_4"]["equipment_brawn"]
        self.backpack_cell_4_magic = hero["backpack"]["backpack_cell_4"]["equipment_magic"]
        self.backpack_cell_4_armour = hero["backpack"]["backpack_cell_4"]["equipment_armour"]
        self.backpack_cell_5_name = hero["backpack"]["backpack_cell_5"]["equipment_name"]
        self.backpack_cell_5_type = hero["backpack"]["backpack_cell_5"]["equipment_type"]
        self.backpack_cell_5_speed = hero["backpack"]["backpack_cell_5"]["equipment_speed"]
        self.backpack_cell_5_brawn = hero["backpack"]["backpack_cell_5"]["equipment_brawn"]
        self.backpack_cell_5_magic = hero["backpack"]["backpack_cell_5"]["equipment_magic"]
        self.backpack_cell_5_armour = hero["backpack"]["backpack_cell_5"]["equipment_armour"]
        self.notes = hero["notes"]

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
              "equipment_type": "cloak",
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
              "equipment_type": "head",
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
              "equipment_type": "gloves",
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
              "equipment_type": "right_hand",
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
              "equipment_type": "chest",
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
              "equipment_type": "left_hand",
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
              "equipment_type": "talisman",
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
              "equipment_type": "feet",
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
              "equipment_type": "necklace",
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
            "ring_1": {
              "equipment_name": "",
              "equipment_type": "ring_1",
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
              "equipment_type": "ring_2",
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
            "backpack_cell_1": {
              "equipment_name": "",
              "equipment_type": "",
              "equipment_speed": 0,
              "equipment_brawn": 0,
              "equipment_magic": 0,
              "equipment_armour": 0,
            },
            "backpack_cell_2": {
              "equipment_name": "",
              "equipment_type": "",
              "equipment_speed": 0,
              "equipment_brawn": 0,
              "equipment_magic": 0,
              "equipment_armour": 0,
            },
            "backpack_cell_3": {
              "equipment_name": "",
              "equipment_type": "",
              "equipment_speed": 0,
              "equipment_brawn": 0,
              "equipment_magic": 0,
              "equipment_armour": 0,
            },
            "backpack_cell_4": {
              "equipment_name": "",
              "equipment_type": "",
              "equipment_speed": 0,
              "equipment_brawn": 0,
              "equipment_magic": 0,
              "equipment_armour": 0,
            },
            "backpack_cell_5": {
              "equipment_name": "",
              "equipment_type": "",
              "equipment_speed": 0,
              "equipment_brawn": 0,
              "equipment_magic": 0,
              "equipment_armour": 0,
            }
          },
          "comments": ""
      }
