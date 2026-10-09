"""gen_ambience.py -- original looping ambience beds (30 s, mono, 22.05 kHz OGG).

All sound is synthesised from noise and simple oscillators; no external audio.
Layers are cross-faded at the ends so the loops join without a click.
"""
from __future__ import annotations
import math, os, sys
import numpy as np
import soundfile as sf

RATE = 22050
LEN = 30.0
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "assets", "audio", "sfx")


def env(n, attack=2.0, release=2.0):
    e = np.ones(n)
    a = int(RATE * attack)
    r = int(RATE * release)
    e[:a] = np.linspace(0, 1, a)
    e[-r:] = np.linspace(1, 0, r)
    return e


def noise(n, seed):
    rng = np.random.default_rng(seed)
    return rng.normal(0, 1, n)


def lowpass(x, cut):
    """one-pole low pass"""
    a = math.exp(-2.0 * math.pi * cut / RATE)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = a * acc + (1 - a) * x[i]
        y[i] = acc
    return y


def band(x, low, high):
    return lowpass(x, high) - lowpass(lowpass(x, high), low)


def slow_waves(n, seed, period=7.0, depth=0.7):
    t = np.arange(n) / RATE
    rng = np.random.default_rng(seed)
    phase = rng.uniform(0, 6.28)
    return 1.0 - depth + depth * (0.5 + 0.5 * np.sin(2 * math.pi * t / period + phase))


def chirps(n, seed, count=14, f0=(1800, 4200), dur=(0.05, 0.16), gain=0.16):
    rng = np.random.default_rng(seed)
    buf = np.zeros(n)
    for _ in range(count):
        d = int(RATE * rng.uniform(*dur))
        start = rng.integers(0, max(1, n - d - 1))
        t = np.arange(d) / RATE
        f = rng.uniform(*f0)
        sweep = f * (1.0 + 1.6 * t / max(t[-1], 1e-6))
        tone = np.sin(2 * math.pi * sweep * t) * np.hanning(d)
        buf[start:start + d] += tone * gain * rng.uniform(0.6, 1.0)
    return buf


def crickets(n, seed, gain=0.10):
    rng = np.random.default_rng(seed)
    buf = np.zeros(n)
    t = np.arange(n) / RATE
    for base in rng.uniform(2600, 4200, 7):
        gate = (np.sin(2 * math.pi * rng.uniform(8, 14) * t) > 0.86).astype(float)
        buf += np.sin(2 * math.pi * base * t) * gate * gain
    return buf


def pulse_pad(n, seed, freq, gain=0.06, rate=1.2):
    t = np.arange(n) / RATE
    rng = np.random.default_rng(seed)
    lfo = 0.5 + 0.5 * np.sin(2 * math.pi * rate * t + rng.uniform(0, 6))
    return np.sin(2 * math.pi * freq * t) * lfo * gain


def normalise(x, peak=0.7):
    m = np.max(np.abs(x)) or 1.0
    return x / m * peak


def write(name, x):
    x = normalise(np.nan_to_num(x))
    x *= env(len(x), 1.5, 1.5)
    path = os.path.join(OUT, name + ".ogg")
    sf.write(path, x.astype("float32"), RATE, format="OGG", subtype="VORBIS")
    print("%-14s %5.1f dB  %5.0f KB" % (name, 20 * math.log10(np.sqrt((x ** 2).mean()) + 1e-9),
                                        os.path.getsize(path) / 1024))


def main():
    os.makedirs(OUT, exist_ok=True)
    n = int(RATE * LEN)

    waves = lowpass(noise(n, 1), 700) * slow_waves(n, 2, 8.0, 0.8) * 3.0
    write("amb_waves", waves)

    stream = band(noise(n, 3), 400, 5200) * 0.6 + lowpass(noise(n, 4), 300) * slow_waves(n, 5, 4.0, 0.4)
    stream += lowpass(noise(n, 6), 1200) * slow_waves(n, 7, 1.7, 0.5) * 0.4
    write("amb_stream", stream)

    forest = lowpass(noise(n, 8), 500) * slow_waves(n, 9, 5.0, 0.6) * 1.6
    forest += band(noise(n, 10), 900, 3200) * 0.22
    forest += chirps(n, 11, 12)
    write("amb_forest", forest)

    village = lowpass(noise(n, 12), 260) * slow_waves(n, 13, 3.0, 0.5) * 1.4
    village += chirps(n, 14, 7, (1500, 2600), (0.06, 0.2), 0.10)
    village += pulse_pad(n, 15, 176.0, 0.03, 0.7)
    write("amb_village", village)

    highland = lowpass(noise(n, 16), 420) * slow_waves(n, 17, 6.0, 0.75) * 2.0
    highland += crickets(n, 18, 0.05)
    write("amb_highland", highland)

    harbour = lowpass(noise(n, 19), 800) * slow_waves(n, 20, 9.0, 0.7) * 3.0
    harbour += chirps(n, 21, 6, (1100, 2300), (0.12, 0.3), 0.09)
    write("amb_harbour", harbour)

    night = lowpass(noise(n, 22), 300) * slow_waves(n, 23, 7.0, 0.5) * 1.2
    night += crickets(n, 24, 0.11)
    write("amb_night_crickets", night)

    print("ambience beds written to", OUT)


if __name__ == "__main__":
    main()
