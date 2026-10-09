"""to_ogg.py -- converts every generated WAV in assets/audio to OGG Vorbis (mono 22050)."""
import os, sys, glob
import soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
targets = [os.path.join(ROOT, "assets", "audio", "music"),
           os.path.join(ROOT, "assets", "audio", "sfx")]
total = 0
for folder in targets:
    for wav in sorted(glob.glob(os.path.join(folder, "*.wav"))):
        data, rate = sf.read(wav)
        out = wav[:-4] + ".ogg"
        sf.write(out, data, rate, format="OGG", subtype="VORBIS")
        os.remove(wav)
        total += 1
        print("converted", os.path.basename(wav), "->", os.path.basename(out))
print("done:", total)
