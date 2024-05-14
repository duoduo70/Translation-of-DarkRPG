file_path = "global_packs/required_data/translation_pack/data/darkspins/loot_tables/darkspins.json"
with open(file_path, "r", encoding="utf-8") as file:
    filedata = file.read()

filedata = filedata.replace("Super Potion", "超级药水")
filedata = filedata.replace("Aegis of The Paladin", "圣骑士的神盾")
filedata = filedata.replace("Rage of The Warrior", "战士的怒火")
filedata = filedata.replace("Bane of The Witcher", "女巫的灾星")
filedata = filedata.replace("Self Reflection", "自我反省")
filedata = filedata.replace("Ultra Potion", "极品药水")
filedata = filedata.replace("Creed of Assassins", "刺客的信条")
filedata = filedata.replace("Aquafinity", "水之亲和")
filedata = filedata.replace("Omega Potion", "欧米伽药水")
filedata = filedata.replace("Revenge of Jaffar", "贾法尔的复仇")

with open(file_path, "w", encoding="utf-8") as file:
    file.write(filedata)

with open("global_packs/required_data/translation_pack/pack.mcmeta", "w", encoding="utf-8") as f:
    f.write(
        """{
    "pack": {
        "pack_format": 15,
        "description": "Translation of DarkRPG"
    }
}"""
    )

file_path = "config/puffish_skills/categories/combat/definitions.json"
with open(file_path, "r", encoding="utf-8") as file:
    filedata = file.read()

filedata = filedata.replace("Heart", "生命值")
filedata = filedata.replace("Resistance", "抗性提升")
filedata = filedata.replace("Melee Damage", "近战伤害")
filedata = filedata.replace("Ranged Damage", "远程伤害")
filedata = filedata.replace("Attack Speed", "攻击速度")
filedata = filedata.replace("Movement Speed", "移动速度")
filedata = filedata.replace("Stamina", "耐力")
filedata = filedata.replace("Healing", "治疗")
filedata = filedata.replace("Jump", "跳跃")

with open(file_path, "w", encoding="utf-8") as file:
    file.write(filedata)

file_path = "config/puffish_skills/categories/combat/category.json"
with open(file_path, "r", encoding="utf-8") as file:
    filedata = file.read()

filedata = filedata.replace("Combat", "战斗")

with open(file_path, "w", encoding="utf-8") as file:
    file.write(filedata)

file_path = "config/puffish_skills/categories/mining/category.json"
with open(file_path, "r", encoding="utf-8") as file:
    filedata = file.read()

filedata = filedata.replace("Mining", "挖掘")

with open(file_path, "w", encoding="utf-8") as file:
    file.write(filedata)

file_path = "config/puffish_skills/categories/mining/definitions.json"
with open(file_path, "r", encoding="utf-8") as file:
    filedata = file.read()

filedata = filedata.replace("Fortune", "时运")
filedata = filedata.replace("Mining Speed", "挖掘速度")

with open(file_path, "w", encoding="utf-8") as file:
    file.write(filedata)