# Montezuma Again! — versões nativas + Templo Asteca

Conjunto de projetos em torno de **Montezuma Again!** (romhack de Atari 8-bit do Pepe, Chile) e de um jogo novo no estilo do Atari 2600:

| # | Versão | Plataforma | Linguagem | Estado dos testes |
|---|--------|------------|-----------|-------------------|
| 1 | Montezuma Again! — **navegador** | qualquer navegador moderno | JavaScript | Núcleo testado (quadro idêntico à versão em C); página não testada em navegador real |
| 2 | Montezuma Again! — **Windows** | Windows (um único `.exe`) | C (Win32) | Núcleo testado; janela/áudio **não testados** no Windows |
| 3 | Montezuma Again! — **Nintendo Switch** | Switch com firmware customizado (`.nro`) | C (libnx) | Núcleo testado; vídeo/áudio/controle **não testados** no console |
| 4 | **Templo Asteca — Novas Fases** | navegador | JavaScript | Lógica testada com busca automática; página não testada em navegador real |

> *English:* native/browser/Switch ports of the Atari 8-bit ROM hack **Montezuma Again!** built on a small purpose-made Atari emulator (6502 + ANTIC + GTIA + POKEY), plus an original 2600-style platformer, **Templo Asteca**, with 12 new rooms. The game data of the ROM hack is **not** included; you supply your own `.xex`.

---

## O que é cada versão

### 1–3. Montezuma Again! (portes)
Em vez de empacotar um emulador de terceiros, o projeto traz um **mini-runtime Atari 8-bit** escrito só para este jogo:

- **CPU 6502** (instruções oficiais, modo decimal);
- **ANTIC** (lista de exibição, modos de texto e bitmap, DLI, WSYNC) e **GTIA** (cores, jogadores/mísseis, prioridades, colisões);
- **POKEY** (4 canais, polinômios, modo de 16 bits) para o áudio;
- **OS simplificado**: interrupção de VBI, cópia das variáveis de sombra, `XITVBV`.

O jogo é carregado a partir de uma imagem de 32 KB em `$4000–$BFFF` com entrada em `$AA06`, extraída do `.xex` original. Não há dependências externas.

**Verificação:** o mesmo quadro (nº 370 de um roteiro de entradas) saiu **idêntico, pixel a pixel**, na versão em C e na versão em JavaScript. Foram rodados 6000 quadros com entradas aleatórias sem erro.

**Limitações conhecidas:** vídeo NTSC 60 Hz; sem scroll fino nem modos GTIA 9/10/11 (o jogo não os usa); temporização por linha aproximada; sem teclado do Atari nem IRQs de timer do POKEY; cores aproximadas.

**Controles**

| Ação | Teclado | Switch |
|------|---------|--------|
| Mover / subir escadas | Setas ou WASD | D-pad ou analógico esquerdo |
| Pular (tiro) | Espaço, Ctrl, Z ou Enter | A, B, X ou Y |
| START / SELECT / OPTION | F2 / F3 / F4 | L / R / ZL |
| Sair | Esc | + |

### 4. Templo Asteca — Novas Fases (jogo original)
Plataforma de exploração no estilo do Atari 2600 (tela 160×192, sprites de 8 px com uma cor por linha, blocos grossos), **inspirada em Montezuma's Revenge, mas com código, sprites e salas totalmente novos**. Não usa nada da ROM original.

- 3 mundos, **12 salas** (Entrada, Câmaras, Tesouro);
- escadas, poços de fogo, caveiras patrulheiras, chaves, portas, gemas;
- 5 vidas; quedas muito altas matam; só se muda de sala pelo chão;
- mesmos controles do teclado acima, com botões na tela para celular.

**Verificação:** uma busca automática (em largura) jogou cada mundo, com as caveiras ativas, e achou caminho até a gema nos três. Isso prova que as fases têm solução; não mede a dificuldade.

---

## Como usar

> Este repositório **não inclui** o jogo. Você precisa do seu próprio `montezuma_again_final_v1.xex`, distribuído pelo autor em <https://montemaker.blogspot.com/2018/09/montezuma-again-final-version-10.html>.

**1. Gerar os dados do jogo (versões 1–3)**
```bash
python tools/make_game_data.py montezuma_again_final_v1.xex game_data.h
```
Copie o `game_data.h` para a pasta do porte que for compilar.

**2. Compilar**

| Versão | Comando |
|--------|---------|
| Windows (MinGW) | `gcc -O2 -mwindows montezuma.c -o Montezuma.exe -lgdi32 -lwinmm` |
| Windows (Visual Studio) | `cl /O2 montezuma.c user32.lib gdi32.lib winmm.lib /link /SUBSYSTEM:WINDOWS` |
| Switch | com o devkitPro (`switch-dev`) instalado: `make` → `montezuma.nro` em `/switch/montezuma/` no SD |
| Navegador | abra o `.html` (a versão do repositório deve carregar o `.xex` por seleção de arquivo) |
| Templo Asteca | abra `templo_asteca.html` no navegador; não precisa de nada além dele |

Quem não tem compilador no Windows pode usar o [w64devkit](https://github.com/skeeto/w64devkit/releases), que é só uma pasta para extrair.

## Estrutura sugerida do repositório
```
├── core.h                 # mini-runtime Atari (CPU, ANTIC, GTIA, POKEY)
├── core.js                # o mesmo núcleo em JavaScript
├── windows/               # montezuma.c, build.bat
├── switch/                # source/main.c, Makefile
├── web/                   # montezuma.html (carrega o .xex), templo_asteca.html
├── tools/make_game_data.py
└── LICENSE
```

## Licença e créditos

- **Código original deste repositório** (núcleo do emulador, portes, Templo Asteca): escolha uma licença aberta, por exemplo MIT, e coloque no arquivo `LICENSE`. Ela **não** cobre o jogo.
- **Montezuma Again!** é um romhack do **Pepe (Chile)**, feito sobre **Montezuma's Revenge** (Parker Bros., hoje parte da Hasbro/Atari). Os dados do jogo **não devem ser versionados** neste repositório (o `.gitignore` já os exclui). Para compartilhar portes com os dados embutidos, peça autorização ao autor.
- Este projeto não é afiliado ao autor do romhack, à Parker Bros., à Atari nem à Nintendo. *Montezuma's Revenge*, *Atari* e *Nintendo Switch* são marcas de seus respectivos donos.
- O porte para Switch destina-se a **homebrew em console próprio**.
