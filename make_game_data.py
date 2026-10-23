#!/usr/bin/env python3
"""Gera game_data.h a partir do SEU arquivo montezuma_again_final_v1.xex.

Uso:  python make_game_data.py montezuma_again_final_v1.xex game_data.h

Le os segmentos do .xex, extrai a imagem de 32 KB em $4000-$BFFF e o ponto de
entrada (RUNAD, $02E0). O arquivo .xex NAO faz parte deste repositorio.
"""
import struct, sys

def main(src, dst):
    d = open(src, 'rb').read()
    i, img, run = 2, None, None
    while i + 4 <= len(d):
        if d[i:i+2] == b'\xff\xff':
            i += 2; continue
        s, e = struct.unpack('<HH', d[i:i+4]); i += 4
        n = e - s + 1
        if n <= 0 or i + n > len(d):
            sys.exit("arquivo .xex invalido")
        if s == 0x4000 and n == 0x8000: img = d[i:i+n]
        if s == 0x02E0 and n == 2:      run = struct.unpack('<H', d[i:i+2])[0]
        i += n
    if img is None or run is None:
        sys.exit("nao encontrei a imagem $4000-$BFFF / RUNAD: este e o .xex certo?")
    with open(dst, 'w') as f:
        f.write('/* gerado por tools/make_game_data.py - NAO versionar */\n')
        f.write('#define GAME_BASE 0x4000\n#define GAME_RUN 0x%04X\n' % run)
        f.write('static const unsigned char GAME_DATA[32768]={\n')
        for k in range(0, len(img), 32):
            f.write(','.join(str(b) for b in img[k:k+32]) + ',\n')
        f.write('};\n')
    print("ok: %s (entrada $%04X)" % (dst, run))

if __name__ == '__main__':
    if len(sys.argv) != 3: sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
