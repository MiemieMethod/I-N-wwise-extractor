import os

import json5
from PIL import Image

from main import *


def unpackFastPatches():
    for i in range(19, 23):
        if os.path.exists(f"output/FastPatchPaks/PatchPak_{i}_387_P.pak"):
            if not os.path.exists(f"output/unpacked{i}"):
                os.mkdir(f"output/unpacked{i}")

            subprocess.run(['./quickbms_4gb_files', '-C', '-o', '-F', f'PatchPak_{i}_387_P.pak',
                            r'./output/bms/unreal_tournament_4_0.4.27e_infinity_nikki.bms', f'./output/FastPatchPaks',
                            f'./output/unpacked{i}'],
                           encoding='utf-8')
        if os.path.exists(f"output/FastPatchPaks/PatchPakWithShader_{i}_387_P.pak"):
            if not os.path.exists(f"output/unpacked{i}"):
                os.mkdir(f"output/unpacked{i}")

            subprocess.run(['./quickbms_4gb_files', '-C', '-o', '-F', f'PatchPakWithShader_{i}_387_P.pak',
                            r'./output/bms/unreal_tournament_4_0.4.27e_infinity_nikki.bms', f'./output/FastPatchPaks',
                            f'./output/unpacked{i}'],
                           encoding='utf-8')
        if os.path.exists(f"output/FastPatchPaks/PatchPak_Default_Movie_{i}_387_P.pak"):
            if not os.path.exists(f"output/unpacked{i}"):
                os.mkdir(f"output/unpacked{i}")

            subprocess.run(['./quickbms_4gb_files', '-C', '-o', '-F', f'PatchPak_Default_Movie_{i}_387_P.pak',
                            r'./output/bms/unreal_tournament_4_0.4.27e_infinity_nikki.bms', f'./output/FastPatchPaks',
                            f'./output/unpacked{i}'],
                           encoding='utf-8')



def processImage():
    OUTPUT = 'output/image' # change here to your path
    os.makedirs(OUTPUT, exist_ok=True)
    I_N_DATA_PATH = r'E:/I-N-Data' # change here to your path
    I_N_IMAGES_PATH = r'E:/I-N-Images' # change here to your path

    with open(os.path.join(I_N_DATA_PATH, r'X6Game/Content/__ExternalPaper2dAtlas__/Intermediate/TextureAtlasInfo.Json'),
              'r', encoding='utf-8') as f:
        atlas = json5.load(f)

    folders = atlas['folders']

    for folder in folders:
        texture2DMap = folders[folder]['texture2DMap']
        for path in texture2DMap:
            actualPath = os.path.join(I_N_IMAGES_PATH, path.replace('/Game', 'X6Game/Content') + '.png')
            if os.path.exists(actualPath):
                elegantCopy(actualPath, f"{OUTPUT}/{path.replace('/Game/', '')}.png")
            else:
                target_path = os.path.join(I_N_IMAGES_PATH,
                                           path.replace('/Game', 'X6Game/Content/__ExternalPaper2dAtlas__/SaveAtlas'))
                dir = os.path.dirname(target_path)
                filename = os.path.basename(target_path)
                target_path = dir + f'/__Frames/{filename}_PNG.json'
                if not os.path.exists(target_path):
                    print(f"Missing target json for {target_path}")
                else:
                    with open(target_path, 'r', encoding='utf-8') as f:
                        frames = json.load(f)
                    for frame in frames:
                        if frame['Type'] == 'PaperSprite':
                            properties = frame['Properties']
                            left = properties['BakedSourceUV']['X']
                            top = properties['BakedSourceUV']['Y']
                            right = left + properties['BakedSourceDimension']['X']
                            bottom = top + properties['BakedSourceDimension']['Y']
                            if not properties['BakedSourceTexture']:
                                print(properties)
                            image_path = properties['BakedSourceTexture']['ObjectPath'].replace('/Game',
                                                                                                'X6Game/Content').split('.')[0] + '.png'
                            image = Image.open(os.path.join(I_N_IMAGES_PATH, image_path))
                            crop_area = (left, top, right, bottom)
                            cropped_image = image.crop(crop_area)
                            if 'BakedSourceTextureRotated' in properties and properties['BakedSourceTextureRotated']:
                                cropped_image = cropped_image.rotate(90, expand=True)
                            os.makedirs(f"{OUTPUT}/{os.path.dirname(path.replace('/Game/', ''))}", exist_ok=True)
                            cropped_image.save(f"{OUTPUT}/{path.replace('/Game/', '')}.png")


if __name__ == '__main__':
    unpackFastPatches()
    # processImage()
    # decodeWems()
    # processBanks()
