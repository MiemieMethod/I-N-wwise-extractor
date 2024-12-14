import json
import os
import subprocess
import shutil

def unpackPaks():
    print("[Main] unpacking paks...")
    if not os.path.exists("input"):
        print("[Main] missing `input` folder!")

    latestKeys = r'keys/Release (338)/keys.json'

    with open(latestKeys, "r", encoding="utf-8") as f:
        keys = json.load(f)

    mainKey = keys["mainKey"]

    with open("unreal_tournament_4_0.4.27e_infinity_nikki.bms", "r", encoding="utf-8") as f:
        script = f.read()

    script = script.replace('set AES_KEY binary ""', f'set AES_KEY binary "0x{mainKey}"')

    if not os.path.exists("output"):
        os.mkdir("output")
    if not os.path.exists("output/bms"):
        os.mkdir("output/bms")

    with open("output/bms/unreal_tournament_4_0.4.27e_infinity_nikki.bms", "w", encoding="utf-8") as f:
        f.write(script)

    if not os.path.exists("output/unpacked"):
        os.mkdir("output/unpacked")

    subprocess.run(['./quickbms_4gb_files', '-C', '-o', '-F', r'*.pak', r'./output/bms/unreal_tournament_4_0.4.27e_infinity_nikki.bms', r'./input', r'./output/unpacked'],
                            encoding='utf-8')

def decodeWems():
    for root, dirs, files in os.walk("output/unpacked/X6Game/Content/Audio/Media"):
        for file in files:
            if file.endswith(".wem"):
                path = root.replace("\\", "/") + "/" + file
                short_path = path.replace("output/unpacked/X6Game/Content/Audio/Media/", "").replace("wem", "wav")
                if not os.path.exists(f"output/decode/{short_path}"):
                    os.makedirs(os.path.dirname(f"output/decode/{short_path}"), exist_ok=True)
                subprocess.run(
                    ["./vgmstream/vgmstream-cli", path, "-o", f"output/decode/{short_path}"])

def elegantCopy(source, dest):
    if not os.path.exists(f"{dest}"):
        os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.exists(f"{source}"):
        shutil.copy2(f"{source}", f"{dest}")
        return True
    return False

def processBanks():
    with open("output/unpacked/X6Game/Content/Audio/GeneratedSoundBanks/Windows/SoundbanksInfo.json", "r", encoding="utf-8") as f:
        banks = json.load(f)

    if not os.path.exists("output/real"):
        os.makedirs("output/real")

    banksData = banks["SoundBanksInfo"]["SoundBanks"]
    for bank in banksData:
        print(f"processing {bank['ShortName']}")
        if "Media" not in bank:
            continue
        medias = bank["Media"]
        for media in medias:
            path = media["Path"].replace("wem", "wav").replace("Media", "output/decode")
            if not os.path.exists(path):
                print(f"missing {path}")
            copyPath = "output/real" + '/' + media["Language"] + '/' + media["ShortName"].replace(r"\\", "/")
            elegantCopy(path, copyPath)

if __name__ == '__main__':
    # unpackPaks()
    # decodeWems()
    processBanks()