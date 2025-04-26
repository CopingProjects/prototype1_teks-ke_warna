import matplotlib.pyplot as plt

frekuensi_huruf = {
    'A': 17.71, 'B': 3.60, 'C': 0.74, 'D': 3.67, 'E': 7.95,
    'F': 0.22, 'G': 4.85, 'H': 2.10, 'I': 6.49, 'J': 0.82,
    'K': 5.36, 'L': 3.30, 'M': 4.51, 'N': 10.31, 'O': 1.67,
    'P': 3.04, 'Q': 0.0047, 'R': 5.32, 'S': 4.16, 'T': 5.59,
    'U': 5.85, 'V': 0.46, 'W': 0.35, 'X': 0.05,
    'Y': 1.81, 'Z': 0.057
}

frekuensi_tandabaca = {
    ';': 64050, '-': 63086, ',': 28741, ')': 22611, '(': 22595,
    ':': 12070, '~': 9924, '/': 8853, '.': 333, '"': 141,
    '?': 87, '=': 75, '!': 40, '%': 23, "'": 18, '+': 12,
    '[': 7, ']': 7, '_': 4, '|': 2, '>': 1, '<': 1,
    '{': 1, '}': 1, '`': 1
}

warna_gradasi_huruf = [
    (255, 240, 0),
    (255, 165, 0),
    (255, 0, 0),
    (0, 128, 0),
    (0, 0, 255),
    (51, 0, 102)
]

def interpolate_rgb(rgb1, rgb2, t):
    return tuple(int(rgb1[i] + (rgb2[i] - rgb1[i]) * t) for i in range(3))

def generate_gradient(total, gradasi):
    if total <= 1:
        return [gradasi[0]]
    segmen = len(gradasi) - 1
    result = []
    for i in range(total):
        posisi = i / (total - 1)
        index_awal = int(posisi * segmen)
        t_local = (posisi * segmen) - index_awal
        if index_awal >= segmen:
            index_awal = segmen - 1
            t_local = 1.0
        rgb = interpolate_rgb(gradasi[index_awal], gradasi[index_awal + 1], t_local)
        result.append(rgb)
    return result

def generate_gray_gradient_from_freq(freq_dict):
    sorted_items = sorted(freq_dict.items(), key=lambda x: -x[1])
    gray_light = (50, 50, 50)
    gray_dark = (230, 230, 230)
    total = len(sorted_items)
    return {
        char: tuple(g / 255 for g in interpolate_rgb(gray_light, gray_dark, i / (total - 1)))
        for i, (char, _) in enumerate(sorted_items)
    }

def generate_huruf_colors():
    huruf_sorted = sorted(frekuensi_huruf.items(), key=lambda x: -x[1])
    warna_huruf = generate_gradient(len(huruf_sorted), warna_gradasi_huruf)
    return {char: tuple(c / 255 for c in color) for (char, _), color in zip(huruf_sorted, warna_huruf)}

def buat_pemetaan_warna_akhir():
    warna_huruf = generate_huruf_colors()
    warna_tandabaca = generate_gray_gradient_from_freq(frekuensi_tandabaca)
    return {**warna_huruf, **warna_tandabaca}

def huruf_ke_rgb(teks, peta_warna):
    hasil = []
    for char in teks:
        char_upper = char.upper()
        if char_upper in peta_warna:
            hasil.append((char, peta_warna[char_upper]))
        elif char in peta_warna:
            hasil.append((char, peta_warna[char]))
        else:
            hasil.append((char, (1, 1, 1)))  # putih
    return hasil

def buat_visualisasi(teks):
    peta_warna = buat_pemetaan_warna_akhir()
    baris_teks = teks.splitlines()
    tinggi = len(baris_teks)
    panjang_terpanjang = max(len(baris) for baris in baris_teks)
    fig, ax = plt.subplots(figsize=(panjang_terpanjang * 0.6, tinggi * 0.6))

    for y, baris in enumerate(baris_teks):
        warna_data = huruf_ke_rgb(baris, peta_warna)
        for x, (_, warna) in enumerate(warna_data):
            lingkaran = plt.Circle((x + 0.5, -y + 0.5), 0.45, color=warna)
            ax.add_patch(lingkaran)

    ax.set_xlim(0, panjang_terpanjang)
    ax.set_ylim(-tinggi, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.tight_layout()
    return fig