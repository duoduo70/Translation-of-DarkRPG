file_path = "global_packs/required_data/translation_pack/data/darkspins/loot_tables/darkspins.json"
with open(file_path, "r") as file:
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

with open(file_path, "w") as file:
    file.write(filedata)

with open("global_packs/required_data/translation_pack/pack.mcmeta", "w") as f:
    f.write(
        """{
    "pack": {
        "pack_format": 15,
        "description": "Translation of DarkRPG"
    }
}"""
    )
