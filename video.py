
import os
import subprocess
import shutil

from config import CURRENT_ALBUM, ASS_VIDEO_GENERATOR_PATH, GENERATE_VIDEO_PATHS, FILE_MAP

def elegantCopy(source, dest):
    if not os.path.exists(f"{dest}"):
        os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.exists(f"{source}"):
        shutil.copy2(f"{source}", f"{dest}")
        return True
    return False

def buildAss():
    if not os.path.exists("output/audio1"):
        os.mkdir("output/audio1")

    for root, dirs, files in os.walk("output/real/SFX/bgm"):
        for file in files:
            if file.endswith(".wav"):
                path = root.replace("output/real/SFX/bgm", "output/audio1") + "/" + file
                # elegantCopy(root + "/" + file, path)
                assPath = path.replace(".wav", ".ass")
                assTitle = FILE_MAP[os.path.basename(file)]
                assAlbum = os.path.relpath(f"input/{CURRENT_ALBUM}", os.path.dirname(path))
                assContent = f"[Script Info]\n\
; Script generated by Aegisub 9706-cibuilds-20caaabc0\n\
; http://www.aegisub.org/\n\
Title: {assTitle}\n\
ScriptType: v4.00+\n\
WrapStyle: 0\n\
ScaledBorderAndShadow: yes\n\
YCbCr Matrix: TV.709\n\
PlayResX: 3840\n\
PlayResY: 2160\n\
\n\
[Aegisub Project Garbage]\n\
Audio File: {os.path.basename(file)}\n\
Video AR Mode: 4\n\
Video AR Value: 1.777778\n\
Video Zoom Percent: 0.250000\n\
Active Line: 1\n\
Video Position: 125\n\
\n\
[V4+ Styles]\n\
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n\
Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1\n\
\n\
[Events]\n\
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n\
Comment: 0,0:00:00.00,0:00:05.00,Default,,0,0,0,,#meta music-visualizer\n\
Comment: 0,0:00:05.00,0:00:07.00,Default,,0,0,0,,title={assTitle}\n\
Comment: 0,0:00:05.00,0:00:07.00,Default,,0,0,0,,album={assAlbum}\n\
Comment: 0,0:00:05.00,0:00:07.00,Default,,0,0,0,,resolution=3840x2160\n\
Comment: 0,0:00:05.00,0:00:07.00,Default,,0,0,0,,fade=1\n\
Comment: 0,0:00:05.00,0:00:07.00,Default,,0,0,0,,args:c:v=copy\n\
Comment: 0,0:00:05.00,0:00:07.00,Default,,0,0,0,,args:c:a=pcm_s32le\n\
Comment: 0,0:00:05.00,0:00:07.00,Default,,0,0,0,,args:ar=48000"

                with open(assPath, "w", encoding="utf-8") as f:
                    f.write(assContent)

def generateVideo(reverse=False):
    if not os.path.exists("output/video"):
        os.mkdir("output/video")

    for path in GENERATE_VIDEO_PATHS:
        for root, dirs, files in os.walk(path):
            if reverse:
                files.reverse()
            for file in files:
                if file.endswith(".ass"):
                    if os.path.exists(f"output/video/{FILE_MAP[os.path.basename(file.replace(".ass", ".wav"))].replace(" | ", "｜")}.mkv"):
                        print(f"[Video] Skipped {FILE_MAP[os.path.basename(file.replace(".ass", ".wav"))].replace(" | ", "｜")}.mkv")
                        continue
                    else:
                        print(f"[Video] Processing {FILE_MAP[os.path.basename(file.replace(".ass", ".wav"))].replace(" | ", "｜")}.mkv")
                    absolutePath = os.path.abspath(root + "/" + file).replace("\\", "/")
                    subprocess.run(f'yarn run render "{absolutePath}"', cwd=ASS_VIDEO_GENERATOR_PATH,
                                   encoding='utf-8', shell=True)
                    print(root + "/" + file.replace(".ass", ".subtitle.mkv"), f"output/video/{FILE_MAP[os.path.basename(file.replace(".ass", ".wav"))]}.mkv")
                    elegantCopy(root + "/" + file.replace(".ass", ".subtitle.mkv"), f"output/video/{FILE_MAP[os.path.basename(file.replace(".ass", ".wav"))].replace(" | ", "｜")}.mkv")



    # absolutePath = os.path.abspath("output/audio/Silence Wav.ass")
    # subprocess.run(['yarn', 'run', 'render', f'{absolutePath}'], cwd=ASS_VIDEO_GENERATOR_PATH, encoding='utf-8', shell=True)
    # # move Silence Wav.subtitle.mkv file into output/video under same folder tree but change name to FILE_MAP[os.path.basename('Silence Wav')]
    # elegantCopy("output/audio/Silence Wav.subtitle.mkv", "output/video/静音.mkv")