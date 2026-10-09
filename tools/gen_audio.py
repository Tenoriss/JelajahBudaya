"""gen_audio.py -- original music and sound effects, synthesised from scratch.

Everything produced here is composed/synthesised by this script for the game
"Nusantara: Jejak Budaya" -- no samples, no copyrighted material.

Musical approach: short looping themes built from 5-tone scales that evoke the
general colour of each region (gong-like metallophones for Java, plucked strings
for the highlands, flowing marimba figures for the rivers of Kalimantan, strong
percussive pulses for Papua, and a warm welcoming theme for the prologue).
These are original melodies, not transcriptions of any traditional piece.

Outputs: assets/audio/music/*.wav, assets/audio/sfx/*.wav

Run: python3 tools/gen_audio.py
"""
from __future__ import annotations

import array
import math
import os
import random
import struct
import sys
import wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MUSIC = os.path.join(ROOT, "assets", "audio", "music")
SFX = os.path.join(ROOT, "assets", "audio", "sfx")

SR = 22050


# --------------------------------------------------------------------------
# tiny synth
# --------------------------------------------------------------------------
def write_wav(path, samples):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = array.array("h")
    peak = max(1.0, max(abs(s) for s in samples) if samples else 1.0)
    scale = 30000.0 / peak
    for s in samples:
        v = int(max(-32000, min(32000, s * scale)))
        data.append(v)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())
    return path


def note_hz(semitones_from_a4):
    return 440.0 * (2.0 ** (semitones_from_a4 / 12.0))


def adsr(i, n, a=0.01, d=0.1, s=0.6, r=0.2):
    t = i / SR
    total = n / SR
    if t < a:
        return t / a
    if t < a + d:
        return 1.0 - (1.0 - s) * ((t - a) / d)
    if t > total - r:
        return s * max(0.0, (total - t) / r)
    return s


class Track:
    """A mono sample buffer.  Every instrument writes into the buffer at a
    start time (and also returns the generated samples)."""

    def __init__(self, seconds):
        self.n = int(seconds * SR)
        self.buf = [0.0] * self.n

    def add(self, start, samples, gain=1.0):
        i0 = max(0, int(start * SR))
        for i, s in enumerate(samples):
            j = i0 + i
            if j >= self.n:
                break
            self.buf[j] += s * gain

    # ---- instruments (start is in seconds) ------------------------------
    def pluck(self, freq, dur, gain=0.5, harm=(1.0, 0.5, 0.25, 0.12), decay=3.0,
              detune=0.0, start=0.0):
        n = int(dur * SR)
        out = []
        for i in range(n):
            t = i / SR
            env = math.exp(-decay * t) * adsr(i, n, 0.004, 0.02, 0.9, 0.05)
            v = 0.0
            for k, amp in enumerate(harm):
                f = freq * (k + 1)
                if detune:
                    f *= (1.0 + detune * math.sin(2 * math.pi * 4.7 * t))
                v += amp * math.sin(2 * math.pi * f * t)
            out.append(v * env)
        self.add(start, out, gain)
        return out

    def marimba(self, freq, dur, gain=0.6, start=0.0):
        n = int(dur * SR)
        out = []
        for i in range(n):
            t = i / SR
            env = math.exp(-5.5 * t) * adsr(i, n, 0.003, 0.01, 1.0, 0.02)
            v = math.sin(2 * math.pi * freq * t)
            v += 0.35 * math.sin(2 * math.pi * freq * 4.0 * t) * math.exp(-12 * t)
            v += 0.16 * math.sin(2 * math.pi * freq * 9.2 * t) * math.exp(-20 * t)
            out.append(v * env)
        self.add(start, out, gain)
        return out

    def gong(self, freq, dur, gain=0.5, start=0.0):
        """Metallophone / gong-like tone with inharmonic partials and beating."""
        n = int(dur * SR)
        out = []
        partials = ((1.0, 1.0), (2.02, 0.5), (2.98, 0.35), (4.06, 0.2), (5.4, 0.12), (6.9, 0.08))
        for i in range(n):
            t = i / SR
            env = math.exp(-1.5 * t) * adsr(i, n, 0.01, 0.06, 0.7, 0.5)
            v = 0.0
            for mult, amp in partials:
                beat = 1.0 + 0.0015 * math.sin(2 * math.pi * 1.7 * t + mult)
                v += amp * math.sin(2 * math.pi * freq * mult * t * beat)
            out.append(v * env)
        self.add(start, out, gain)
        return out

    def pad(self, freq, dur, gain=0.35, vibrato=4.5, start=0.0):
        n = int(dur * SR)
        out = []
        phase = 0.0
        for i in range(n):
            t = i / SR
            env = adsr(i, n, 0.35, 0.2, 0.75, 0.6)
            f = freq * (1.0 + 0.004 * math.sin(2 * math.pi * vibrato * t))
            v = math.sin(2 * math.pi * f * t)
            v += 0.45 * math.sin(2 * math.pi * f * 2.0 * t)
            v += 0.22 * math.sin(2 * math.pi * f * 3.01 * t)
            v += 0.09 * math.sin(2 * math.pi * f * 5.0 * t)
            out.append(v * env * 0.5)
        self.add(start, out, gain)
        return out

    def flute(self, freq, dur, gain=0.4, start=0.0):
        n = int(dur * SR)
        out = []
        for i in range(n):
            t = i / SR
            env = adsr(i, n, 0.06, 0.1, 0.8, 0.18)
            breath = 0.05 * (random.random() * 2 - 1) * math.exp(-2.5 * t)
            f = freq * (1.0 + 0.005 * math.sin(2 * math.pi * 5.2 * t))
            v = math.sin(2 * math.pi * f * t) + 0.22 * math.sin(2 * math.pi * f * 2.0 * t) + breath
            out.append(v * env * 0.6)
        self.add(start, out, gain)
        return out

    def bass(self, freq, dur, gain=0.6, start=0.0):
        n = int(dur * SR)
        out = []
        for i in range(n):
            t = i / SR
            env = adsr(i, n, 0.01, 0.05, 0.8, 0.12)
            v = math.sin(2 * math.pi * freq * t) + 0.3 * math.sin(2 * math.pi * freq * 2 * t)
            out.append(v * env * 0.7)
        self.add(start, out, gain)
        return out

    def perc(self, dur, kind="wood", gain=0.25, start=0.0):
        n = int(dur * SR)
        out = []
        for i in range(n):
            t = i / SR
            if kind == "wood":
                env = math.exp(-38 * t)
                v = math.sin(2 * math.pi * 420 * t) * env
                v += 0.6 * (random.random() * 2 - 1) * math.exp(-90 * t)
            elif kind == "drum":
                env = math.exp(-9 * t)
                f = 130 * math.exp(-18 * t) + 55
                v = math.sin(2 * math.pi * f * t) * env
                v += 0.25 * (random.random() * 2 - 1) * math.exp(-40 * t)
            elif kind == "shake":
                env = math.exp(-16 * t)
                v = (random.random() * 2 - 1) * env
            else:  # gong hit
                env = math.exp(-4 * t)
                v = (math.sin(2 * math.pi * 168 * t) + 0.6 * math.sin(2 * math.pi * 342 * t)
                     + 0.4 * math.sin(2 * math.pi * 517 * t)) * env
            out.append(v)
        self.add(start, out, gain)
        return out

    def echo(self, delay=0.26, decay=0.34, taps=3):
        dry = list(self.buf)
        for tap in range(1, taps + 1):
            d = int(delay * tap * SR)
            g = decay ** tap
            for i in range(self.n - d):
                self.buf[i + d] += dry[i] * g

    def normalise(self, target=0.86):
        peak = max(1e-6, max(abs(s) for s in self.buf))
        k = target / peak
        self.buf = [s * k for s in self.buf]


# --------------------------------------------------------------------------
# scales (semitone offsets from A4)
# --------------------------------------------------------------------------
def scale_tones(root, steps):
    return [root + s for s in steps]


PENTA = [0, 2, 4, 7, 9]                  # major pentatonic
PENTA_MINOR = [0, 3, 5, 7, 10]
PELOG_ISH = [0, 1, 3, 7, 8]              # 5-tone stretched scale (gamelan colour)
PAPUA_ISH = [0, 2, 5, 7, 10]


def melody(track, tones, t0, beats, beat_len, inst, gain=0.5, octave=0, rest=0.15, seed=1):
    rng = random.Random(seed)
    t = t0
    bar = 0
    end = t0 + beats * beat_len
    while t < end - 0.001:
        if rng.random() > rest:
            deg = rng.randrange(len(tones))
            if rng.random() < 0.3:
                deg = max(0, deg - 1)
            semi = tones[deg] + 12 * octave
            dur = beat_len * rng.choice([0.5, 1.0, 1.0, 1.5, 2.0])
            f = note_hz(semi)
            fn = getattr(track, inst)
            fn(f, dur * 1.6, gain, start=t)
        t += beat_len * rng.choice([0.5, 1.0, 1.0, 1.5])
        bar += 1
        if bar % 8 == 0:
            t += beat_len * 0.5


def build_theme(name, root, scale, bpm, inst_melody, inst_pad, seconds, seed,
                perc_pattern=None, perc_kind="wood", pad_gain=0.3, melody_gain=0.35,
                bass=True, octave=0, rest=0.2):
    beat = 60.0 / bpm
    tr = Track(seconds)
    tones = scale_tones(root, scale)
    # pad / drone
    for i in range(0, int(seconds / (beat * 4)) + 1):
        t0 = i * beat * 4
        deg = tones[(i * 2) % len(tones)]
        tr.pad(note_hz(deg), beat * 4.2, pad_gain, vibrato=3.2 + (i % 3), start=t0)
        tr.pad(note_hz(deg + 12), beat * 4.2, pad_gain * 0.4, vibrato=4.1, start=t0)
    # bass
    if bass:
        for i in range(0, int(seconds / (beat * 2)) + 1):
            t0 = i * beat * 2
            deg = tones[(i * 3) % len(tones)] - 24
            tr.bass(note_hz(deg), beat * 1.9, 0.42, start=t0)
    melody(tr, tones, 0.0, seconds / beat, beat, inst_melody, melody_gain,
           octave=octave, rest=rest, seed=seed)
    # a second, answering line an octave up
    melody(tr, tones, beat * 2.0, seconds / beat - 4, beat, inst_melody,
           melody_gain * 0.45, octave=octave + 1, rest=rest + 0.25, seed=seed + 77)
    if perc_pattern:
        rng = random.Random(seed + 5)
        t = 0.0
        while t < seconds - 0.05:
            pos = t % (beat * 2)
            for sub, kind, g in perc_pattern:
                if abs(pos - sub * beat) < 0.03:
                    tr.perc(0.35, kind, g, start=t)
            t += beat * 0.5
    tr.echo(0.24 if bpm > 80 else 0.34, 0.3, 3)
    tr.normalise()
    return tr


def build_riverside(name, root, bpm, seconds, seed):
    """Kalimantan: flowing marimba figure over a soft drone."""
    beat = 60.0 / bpm
    tr = Track(seconds)
    tones = scale_tones(root, PENTA)
    for i in range(0, int(seconds / (beat * 4)) + 1):
        tr.pad(note_hz(tones[i % 5] - 12), beat * 4.4, 0.26, vibrato=2.6, start=i * beat * 4)
    t = 0.0
    rng = random.Random(seed)
    step = beat * 0.5
    while t < seconds - 0.1:
        deg = tones[rng.randrange(5)]
        tr.marimba(note_hz(deg), step * 1.7, 0.42, start=t)
        if rng.random() < 0.45:
            tr.marimba(note_hz(deg + 7), step * 1.4, 0.28, start=t)
        t += step
    for i in range(0, int(seconds / (beat * 4)) + 1):
        tr.bass(note_hz(tones[i % 5] - 24), beat * 3.4, 0.34, start=i * beat * 4)
    t = 0.0
    while t < seconds - 0.1:
        tr.perc(0.25, "shake", 0.09, start=t)
        if abs((t % (beat * 4))) < 0.03:
            tr.perc(0.5, "drum", 0.14, start=t)
        t += beat
    tr.echo(0.3, 0.32, 3)
    tr.normalise()
    return tr


def build_pulse(name, root, bpm, seconds, seed):
    """Papua-inspired theme: strong, steady pulse with a soaring melody."""
    beat = 60.0 / bpm
    tr = Track(seconds)
    tones = scale_tones(root, PAPUA_ISH)
    for i in range(0, int(seconds / (beat * 4)) + 1):
        tr.pad(note_hz(tones[i % 5] - 12), beat * 4.3, 0.22, vibrato=5.0, start=i * beat * 4)
        tr.pad(note_hz(tones[(i + 2) % 5]), beat * 4.3, 0.14, vibrato=3.4, start=i * beat * 4)
    t = 0.0
    while t < seconds - 0.05:
        beatpos = t % (beat * 4)
        if abs(beatpos) < 0.03:
            tr.perc(0.6, "drum", 0.30, start=t)
        elif abs(beatpos - beat * 2) < 0.03:
            tr.perc(0.5, "drum", 0.20, start=t)
        elif abs(beatpos - beat) < 0.03 or abs(beatpos - beat * 3) < 0.03:
            tr.perc(0.3, "wood", 0.14, start=t)
        t += beat * 0.5
    melody(tr, tones, 0.0, seconds / beat, beat, "flute", 0.3, octave=0, rest=0.30, seed=seed)
    for i in range(0, int(seconds / (beat * 2)) + 1):
        tr.bass(note_hz(tones[(i * 2) % 5] - 24), beat * 1.8, 0.40, start=i * beat * 2)
    tr.echo(0.22, 0.28, 3)
    tr.normalise()
    return tr


# --------------------------------------------------------------------------
# sound effects
# --------------------------------------------------------------------------
def sfx_footstep(seed, hard=False):
    random.seed(seed)
    n = int(0.11 * SR)
    out = []
    for i in range(n):
        t = i / SR
        env = math.exp(-42 * t)
        v = (random.random() * 2 - 1) * env * 0.7
        v += math.sin(2 * math.pi * (165 if hard else 220) * t) * env * 0.4
        out.append(v)
    return out


def sfx_water(dur=0.5, seed=3, kind="splash"):
    random.seed(seed)
    n = int(dur * SR)
    out = []
    for i in range(n):
        t = i / SR
        if kind == "splash":
            env = math.exp(-7 * t) * (1 - math.exp(-90 * t))
            v = (random.random() * 2 - 1) * env * 0.9
        else:  # stream / gentle
            env = 0.5 + 0.5 * math.sin(2 * math.pi * 0.7 * t)
            v = (random.random() * 2 - 1) * 0.35 * env
            v += math.sin(2 * math.pi * (420 + 60 * math.sin(2 * math.pi * 0.9 * t)) * t) * 0.12
        out.append(v)
    return out


def sfx_bird(seed=1):
    random.seed(seed)
    n = int(0.45 * SR)
    out = []
    base = random.uniform(1600, 2600)
    for i in range(n):
        t = i / SR
        env = math.exp(-6 * t) * (1 - math.exp(-120 * t))
        f = base * (1 + 0.35 * math.sin(2 * math.pi * 7 * t))
        chirps = math.sin(2 * math.pi * f * t)
        out.append(chirps * env * 0.5)
    return out


def sfx_ui(kind="click"):
    n = int((0.09 if kind == "click" else 0.16) * SR)
    out = []
    for i in range(n):
        t = i / SR
        if kind == "click":
            env = math.exp(-48 * t)
            v = math.sin(2 * math.pi * 900 * t) * env
            v += (random.random() * 2 - 1) * math.exp(-160 * t) * 0.3
        elif kind == "open":
            env = math.exp(-11 * t)
            f = 420 + 900 * t / 0.16
            v = math.sin(2 * math.pi * f * t) * env
        elif kind == "error":
            env = math.exp(-11 * t)
            v = math.sin(2 * math.pi * 180 * t) * env
            v += math.sin(2 * math.pi * 150 * t) * env * 0.6
        else:  # confirm
            env = math.exp(-9 * t)
            v = math.sin(2 * math.pi * 660 * t) * env
            v += math.sin(2 * math.pi * 990 * t) * env * 0.6
        out.append(v)
    return out


def sfx_quest():
    """Warm rising arpeggio for quest completion."""
    tr = Track(1.6)
    for k, semi in enumerate((0, 4, 7, 12, 16, 19)):
        tr.pluck(note_hz(semi), 0.9, 0.5, decay=3.2, start=k * 0.11)
        tr.gong(note_hz(semi - 12), 0.9, 0.14, start=k * 0.11)
    tr.echo(0.18, 0.3, 3)
    return tr.buf


def sfx_collect():
    tr = Track(0.8)
    for k, semi in enumerate((0, 7, 12)):
        tr.marimba(note_hz(semi + 12), 0.5, 0.6, start=k * 0.06)
    return tr.buf


def sfx_discovery():
    """Culture discovered: shimmering gong swell."""
    tr = Track(2.4)
    tr.gong(note_hz(0), 2.2, 0.6)
    tr.gong(note_hz(7), 2.0, 0.35)
    tr.gong(note_hz(12), 1.8, 0.3)
    for k in range(6):
        tr.marimba(note_hz(12 + k * 2), 0.7, 0.25, start=0.25 + k * 0.09)
    tr.echo(0.3, 0.4, 4)
    return tr.buf


def sfx_puzzle_solved():
    tr = Track(1.8)
    for k, semi in enumerate((0, 5, 9, 12, 17, 21)):
        tr.marimba(note_hz(semi), 1.0, 0.5, start=k * 0.09)
    tr.echo(0.22, 0.34, 3)
    return tr.buf


def sfx_puzzle_wrong():
    tr = Track(0.6)
    tr.pluck(note_hz(-3), 0.5, 0.5, decay=4.0, harm=(1.0, 0.7, 0.4, 0.2))
    tr.pluck(note_hz(-4), 0.5, 0.4, decay=4.5, harm=(1.0, 0.6, 0.35, 0.2), start=0.05)
    return tr.buf


def sfx_tone(semi, dur=0.7):
    tr = Track(dur + 0.3)
    tr.gong(note_hz(semi), dur, 0.7)
    tr.marimba(note_hz(semi), dur * 0.6, 0.35)
    return tr.buf


def sfx_coin():
    tr = Track(0.5)
    tr.marimba(note_hz(19), 0.28, 0.6)
    tr.marimba(note_hz(24), 0.42, 0.5, start=0.07)
    return tr.buf


def sfx_unlock():
    tr = Track(2.0)
    tr.gong(note_hz(-12), 1.8, 0.7)
    tr.pluck(note_hz(0), 1.2, 0.4)
    tr.pluck(note_hz(7), 1.2, 0.35)
    tr.pluck(note_hz(12), 1.4, 0.3)
    tr.echo(0.26, 0.35, 3)
    return tr.buf


def sfx_impact(kind="wood"):
    n = int(0.3 * SR)
    out = []
    for i in range(n):
        t = i / SR
        env = math.exp(-16 * t)
        if kind == "wood":
            v = math.sin(2 * math.pi * 320 * t) * env + (random.random() * 2 - 1) * math.exp(-70 * t) * 0.5
        elif kind == "stone":
            v = (random.random() * 2 - 1) * env * 0.9
        else:
            v = math.sin(2 * math.pi * 90 * t) * env
        out.append(v)
    return out


def sfx_tick():
    n = int(0.05 * SR)
    return [math.sin(2 * math.pi * 1400 * i / SR) * math.exp(-60 * i / SR) for i in range(n)]


def sfx_ambience(seconds, seed, kind):
    """Very light looping ambience beds (stream, forest evening, village)."""
    random.seed(seed)
    n = int(seconds * SR)
    out = [0.0] * n
    if kind == "stream":
        for i in range(n):
            t = i / SR
            out[i] = (random.random() * 2 - 1) * 0.22
            out[i] += math.sin(2 * math.pi * 0.6 * t + math.sin(t * 0.3)) * 0.05
    elif kind == "forest":
        for i in range(n):
            t = i / SR
            v = (random.random() * 2 - 1) * 0.10
            v += math.sin(2 * math.pi * 0.21 * t) * 0.06 * (0.6 + 0.4 * math.sin(t * 0.7))
            out[i] = v
        # sprinkle bird calls
        t = 0.0
        while t < seconds:
            call = sfx_bird(seed + int(t))
            i0 = int(t * SR)
            for i, s in enumerate(call):
                if i0 + i < n:
                    out[i0 + i] += s * 0.18
            t += random.uniform(3.0, 7.5)
    elif kind == "night":
        for i in range(n):
            t = i / SR
            out[i] = (random.random() * 2 - 1) * 0.07
            out[i] += math.sin(2 * math.pi * 42 * t) * 0.05 * (0.5 + 0.5 * math.sin(2 * math.pi * 0.11 * t))
            out[i] += math.sin(2 * math.pi * 3600 * t) * 0.02 * (0.5 + 0.5 * math.sin(2 * math.pi * 6.3 * t))
    elif kind == "market":
        for i in range(n):
            t = i / SR
            out[i] = (random.random() * 2 - 1) * 0.10
            out[i] += math.sin(2 * math.pi * 120 * t) * 0.03 * (0.5 + 0.5 * math.sin(2 * math.pi * 0.9 * t))
    else:  # wind
        for i in range(n):
            t = i / SR
            out[i] = (random.random() * 2 - 1) * 0.14 * (0.5 + 0.5 * math.sin(2 * math.pi * 0.13 * t))
    peak = max(1e-6, max(abs(s) for s in out))
    k = 0.7 / peak
    return [s * k for s in out]


# --------------------------------------------------------------------------
def main():
    os.makedirs(MUSIC, exist_ok=True)
    os.makedirs(SFX, exist_ok=True)
    print("music...")
    themes = {
        "prologue": build_theme("prologue", -9, PENTA, 78, "marimba", "pad", 36, 11,
                                perc_pattern=[(0.0, "wood", 0.12), (1.0, "shake", 0.07)],
                                pad_gain=0.30, melody_gain=0.34, octave=0),
        "sumatra": build_theme("sumatra", -7, PENTA_MINOR, 74, "pluck", "pad", 36, 21,
                               perc_pattern=[(0.0, "drum", 0.13), (1.5, "shake", 0.06)],
                               pad_gain=0.32, melody_gain=0.36, octave=0, rest=0.28),
        "java": build_theme("java", -5, PELOG_ISH, 62, "gong", "pad", 40, 31,
                            perc_pattern=[(0.0, "gong", 0.12), (2.0, "gong", 0.07)],
                            pad_gain=0.34, melody_gain=0.30, octave=0, rest=0.35),
        "kalimantan": build_riverside("kalimantan", -8, 84, 36, 41),
        "sulawesi": build_theme("sulawesi", -6, PENTA, 88, "pluck", "pad", 36, 51,
                                perc_pattern=[(0.0, "drum", 0.16), (0.5, "wood", 0.10), (1.5, "shake", 0.08)],
                                pad_gain=0.28, melody_gain=0.36, octave=0, rest=0.22),
        "papua": build_pulse("papua", -10, 96, 36, 61),
        "ending": build_theme("ending", -3, PENTA, 66, "pluck", "pad", 44, 71,
                              perc_pattern=[(0.0, "gong", 0.10)],
                              pad_gain=0.36, melody_gain=0.34, octave=0, rest=0.3),
        "victory": build_theme("victory", -1, PENTA, 104, "marimba", "pad", 24, 81,
                               perc_pattern=[(0.0, "drum", 0.18), (1.0, "wood", 0.12)],
                               pad_gain=0.26, melody_gain=0.4, octave=0, rest=0.12),
    }
    for name, track in themes.items():
        p = os.path.join(MUSIC, name + ".wav")
        write_wav(p, track.buf)
        print("   ", name, "%.1fs" % (len(track.buf) / SR))

    print("sfx...")
    sfx = {}
    for i in range(4):
        sfx["step_grass_%d" % i] = sfx_footstep(i, hard=False)
        sfx["step_stone_%d" % i] = sfx_footstep(i + 10, hard=True)
    sfx["water_splash"] = sfx_water(0.55, 3, "splash")
    sfx["water_stream"] = sfx_water(1.4, 4, "stream")
    for i in range(3):
        sfx["bird_%d" % i] = sfx_bird(i + 1)
    sfx["ui_click"] = sfx_ui("click")
    sfx["ui_hover"] = sfx_ui("tick")
    sfx["ui_open"] = sfx_ui("open")
    sfx["ui_confirm"] = sfx_ui("confirm")
    sfx["ui_error"] = sfx_ui("error")
    sfx["ui_tick"] = sfx_tick()
    sfx["quest_complete"] = sfx_quest()
    sfx["collect"] = sfx_collect()
    sfx["culture_discovered"] = sfx_discovery()
    sfx["puzzle_solved"] = sfx_puzzle_solved()
    sfx["puzzle_wrong"] = sfx_puzzle_wrong()
    sfx["coin"] = sfx_coin()
    sfx["unlock"] = sfx_unlock()
    sfx["impact_wood"] = sfx_impact("wood")
    sfx["impact_stone"] = sfx_impact("stone")
    sfx["drum"] = sfx_impact("drum")
    for k in range(6):
        sfx["tone_%d" % k] = sfx_tone(k * 2, 0.8)
    for k, semi in [(0, 0), (1, 4), (2, 7), (3, 12)]:
        sfx["chime_%d" % k] = sfx_tone(semi + 12, 0.55)

    for name, samples in sfx.items():
        write_wav(os.path.join(SFX, name + ".wav"), samples)
    print("    %d sfx files" % len(sfx))
    print("done")


if __name__ == "__main__":
    main()
