#!/usr/bin/env python3
"""
Gera um GIF animado do diagrama Ansible Lab para publicar no LinkedIn.
Dependências: pip install pillow
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

# ── Config ───────────────────────────────────────────────────────────────────
W, H       = 960, 540
FPS        = 12
DURATION   = 10         # segundos de animação total
N_FRAMES   = FPS * DURATION
OUT_FILE   = os.path.join(os.path.dirname(__file__), "ansible-lab.gif")

# ── Paleta ───────────────────────────────────────────────────────────────────
BG          = (13, 17, 23)
CARD_BG     = (22, 27, 34)
CARD_BORDER = (48, 54, 61)

BLUE   = (56,  139, 253)
GREEN  = (63,  185,  80)
ORANGE = (240, 136,  62)
PURPLE = (188, 140, 255)
YELLOW = (227, 179,  65)
DIM    = (139, 148, 158)
WHITE  = (230, 237, 243)
RED    = (248,  81,  73)

# ── Helpers ──────────────────────────────────────────────────────────────────
def lerp(a, b, t): return a + (b - a) * t
def clamp(v, lo, hi): return max(lo, min(hi, v))
def ease_out(t): return 1 - (1 - t) ** 3
def ease_in_out(t): return t * t * (3 - 2 * t)

def load_font(size):
    for name in ["DejaVuSansMono.ttf", "DejaVuSansMono-Bold.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
                 "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"]:
        try: return ImageFont.truetype(name, size)
        except: pass
    return ImageFont.load_default()

FONT_SM  = load_font(11)
FONT_MD  = load_font(13)
FONT_LG  = load_font(15)
FONT_XL  = load_font(20)
FONT_T   = load_font(17)

# ── Layout dos nodos ─────────────────────────────────────────────────────────
CTRL = {"x": 400, "y": 80,  "w": 160, "h": 90,
        "label": "CONTROL NODE", "sub": "Ansible Engine",
        "ip": "192.168.56.1", "color": BLUE}

NODES = [
    {"x":  60,  "y": 280, "w": 155, "h": 100,
     "label": "lb-01", "sub": "HAProxy", "ip": "192.168.56.10",
     "color": ORANGE, "roles": "common\nhardening\nhaproxy"},
    {"x": 240,  "y": 280, "w": 155, "h": 100,
     "label": "web-01", "sub": "Nginx + PHP", "ip": "192.168.56.11",
     "color": GREEN,  "roles": "common\nhardening\nnginx + php"},
    {"x": 420,  "y": 280, "w": 155, "h": 100,
     "label": "web-02", "sub": "Nginx + PHP", "ip": "192.168.56.12",
     "color": GREEN,  "roles": "common\nhardening\nnginx + php"},
    {"x": 600,  "y": 280, "w": 155, "h": 100,
     "label": "db-01", "sub": "MySQL", "ip": "192.168.56.13",
     "color": PURPLE, "roles": "common\nhardening\nmysql"},
]

def node_center(n):
    return (n["x"] + n["w"] // 2, n["y"] + n["h"] // 2)

def ctrl_center():
    return (CTRL["x"] + CTRL["w"] // 2, CTRL["y"] + CTRL["h"])

# ── Desenho de nodo ───────────────────────────────────────────────────────────
def draw_card(draw, n, alpha=1.0, status="pending", glow=0.0):
    x, y, w, h = n["x"], n["y"], n["w"], n["h"]
    col = n["color"]

    # Glow
    if glow > 0:
        for r in range(12, 0, -3):
            g_alpha = int(glow * 60 * (r / 12))
            draw.rounded_rectangle([x-r, y-r, x+w+r, y+h+r],
                                   radius=10+r,
                                   outline=(*col, g_alpha))

    # Card body
    a_bg  = int(alpha * 255)
    draw.rounded_rectangle([x, y, x+w, y+h],
                            radius=10,
                            fill=(*CARD_BG, a_bg),
                            outline=(*col, int(alpha * 200)))

    if alpha < 0.1: return

    # Label
    draw.text((x+12, y+10), n["label"], font=FONT_MD, fill=(*WHITE, a_bg))
    draw.text((x+12, y+26), n["sub"],   font=FONT_SM, fill=(*DIM,   a_bg))
    draw.text((x+12, y+41), n["ip"],    font=FONT_SM, fill=(*BLUE,  a_bg))

    # Status badge
    if status == "pending":
        bc, tc, label = CARD_BORDER, DIM, "PENDING"
    elif status == "configuring":
        bc, tc, label = ORANGE, ORANGE, "CONFIGURING"
    else:
        bc, tc, label = GREEN, GREEN, "READY"

    bx, by = x+12, y+60
    bw = draw.textlength(label, font=FONT_SM) + 18
    draw.rounded_rectangle([bx, by, bx+bw, by+16],
                            radius=8, fill=(*CARD_BG, a_bg),
                            outline=(*bc, a_bg))
    draw.ellipse([bx+6, by+5, bx+14, by+13], fill=(*bc, a_bg))
    draw.text((bx+18, by+2), label, font=FONT_SM, fill=(*tc, a_bg))

def draw_control(draw, alpha=1.0):
    x, y, w, h = CTRL["x"], CTRL["y"], CTRL["w"], CTRL["h"]
    a = int(alpha * 255)
    draw.rounded_rectangle([x, y, x+w, y+h],
                            radius=10, fill=(*CARD_BG, a),
                            outline=(*BLUE, a))
    draw.text((x+12, y+10), CTRL["label"], font=FONT_MD, fill=(*WHITE, a))
    draw.text((x+12, y+27), CTRL["sub"],   font=FONT_SM, fill=(*DIM,   a))
    draw.text((x+12, y+42), CTRL["ip"],    font=FONT_SM, fill=(*BLUE,  a))

    # Running badge
    bx, by = x+12, y+60
    label = "RUNNING"
    bw = draw.textlength(label, font=FONT_SM) + 18
    draw.rounded_rectangle([bx, by, bx+bw, by+16], radius=8,
                            fill=(*CARD_BG, a), outline=(*GREEN, a))
    draw.ellipse([bx+6, by+5, bx+14, by+13], fill=(*GREEN, a))
    draw.text((bx+18, by+2), label, font=FONT_SM, fill=(*GREEN, a))

# ── Linha SSH animada ─────────────────────────────────────────────────────────
def draw_ssh_line(draw, src, dst, progress, color, dash=True):
    if progress <= 0: return
    tx = lerp(src[0], dst[0], progress)
    ty = lerp(src[1], dst[1], progress)

    if dash:
        # desenha segmentos pontilhados
        steps = max(int(progress * 40), 2)
        for i in range(steps):
            t0 = i / steps
            t1 = (i + 0.5) / steps
            if i % 2 == 0:
                p0 = (lerp(src[0], dst[0], t0), lerp(src[1], dst[1], t0))
                p1 = (lerp(src[0], dst[0], min(t1, progress)),
                      lerp(src[1], dst[1], min(t1, progress)))
                draw.line([p0, p1], fill=(*color, 180), width=2)
    else:
        draw.line([src, (tx, ty)], fill=(*color, 200), width=2)

def draw_packet(draw, src, dst, t, label, color):
    if t <= 0 or t >= 1: return
    x = lerp(src[0], dst[0], t)
    y = lerp(src[1], dst[1], t)
    tw = draw.textlength(label, font=FONT_SM) + 12
    draw.rounded_rectangle([x-tw//2, y-8, x+tw//2, y+8],
                            radius=4, fill=(*CARD_BG, 220),
                            outline=(*color, 200))
    draw.text((x-tw//2+6, y-7), label, font=FONT_SM, fill=(*color, 220))

# ── Título ────────────────────────────────────────────────────────────────────
def draw_title(draw, alpha):
    a = int(alpha * 255)
    t1 = "Ansible Lab"
    t2 = "— Infraestrutura Web Segura"
    w1 = draw.textlength(t1, font=FONT_XL)
    w2 = draw.textlength(t2, font=FONT_XL)
    total = w1 + w2
    sx = (W - total) / 2

    draw.text((sx, 18), t1, font=FONT_XL, fill=(*WHITE, a))
    draw.text((sx + w1, 18), t2, font=FONT_XL, fill=(*ORANGE, a))

    sub = "Control Node  →  4 Managed Nodes via SSH  →  LAMP Stack + Hardening"
    sw = draw.textlength(sub, font=FONT_SM)
    draw.text(((W - sw) / 2, 44), sub, font=FONT_SM, fill=(*DIM, a))

# ── Terminal de log ────────────────────────────────────────────────────────────
LOGS = [
    (DIM,    "PLAY [Provisionar Load Balancer] ****************************"),
    (GREEN,  "ok: [lb-01]   "),
    (YELLOW, "changed: [haproxy installed, ufw enabled, fail2ban active]"),
    (DIM,    "PLAY [Provisionar Servidores Web] ***************************"),
    (GREEN,  "ok: [web-01] [web-02]   "),
    (YELLOW, "changed: [nginx, php-fpm, ssh hardening applied]"),
    (DIM,    "PLAY [Provisionar Banco de Dados] ***************************"),
    (GREEN,  "ok: [db-01]   "),
    (YELLOW, "changed: [mysql, bind restricted, ufw rules applied]"),
    (RED,    "PLAY RECAP — lb-01: ok=14 changed=12 | web-01: ok=17 changed=15 | web-02: ok=17 changed=15 | db-01: ok=16 changed=14 | failed=0"),
]

def draw_terminal(draw, log_progress, alpha):
    if alpha <= 0: return
    a = int(alpha * 255)
    tx, ty, tw, th = 30, 425, W - 60, 100
    draw.rounded_rectangle([tx, ty, tx+tw, ty+th], radius=8,
                            fill=(*CARD_BG, a), outline=(*CARD_BORDER, a))
    # bar
    draw.rounded_rectangle([tx, ty, tx+tw, ty+20], radius=8,
                            fill=(22, 27, 34, a), outline=(*CARD_BORDER, a))
    for i, c in enumerate([(248,81,73),(227,179,65),(63,185,80)]):
        draw.ellipse([tx+10+i*16, ty+5, tx+20+i*16, ty+15], fill=(*c, a))
    draw.text((tx+64, ty+3), "$ ansible-playbook playbook.yml",
              font=FONT_SM, fill=(*DIM, a))

    visible = int(log_progress * len(LOGS))
    for i in range(min(visible, len(LOGS))):
        col, txt = LOGS[i]
        # wrap simplista
        ly = ty + 24 + i * 14
        if ly > ty + th - 8: break
        draw.text((tx+10, ly), txt[:120], font=FONT_SM, fill=(*col, a))

# ── Render de um frame ────────────────────────────────────────────────────────
def render_frame(frame_idx):
    t = frame_idx / N_FRAMES               # 0..1 total

    img  = Image.new("RGBA", (W, H), BG + (255,))
    draw = ImageDraw.Draw(img)

    # ---- Tempos (em fração do total) ----
    T_TITLE   = (0.00, 0.10)   # título aparece
    T_CTRL    = (0.08, 0.18)   # nodo control aparece
    T_NODES   = (0.15, 0.32)   # nodos gerenciados aparecem
    T_LINES   = (0.30, 0.50)   # linhas SSH crescem
    T_PACKETS = (0.48, 0.65)   # packets viajam
    T_CFG     = (0.50, 0.65)   # status → configuring
    T_READY   = (0.62, 0.80)   # status → ready
    T_TERM    = (0.70, 1.00)   # terminal aparece e mostra logs

    def prog(start, end):
        return clamp((t - start) / (end - start), 0, 1)

    # Título
    draw_title(draw, ease_out(prog(*T_TITLE)))

    # Control node
    draw_control(draw, ease_out(prog(*T_CTRL)))

    # Nodos gerenciados
    node_delays = [0.00, 0.06, 0.12, 0.18]
    for i, node in enumerate(NODES):
        nd = node_delays[i]
        na = ease_out(prog(T_NODES[0] + nd, T_NODES[1] + nd))

        # Status
        cfg_p = prog(T_CFG[0] + nd*0.1, T_CFG[1])
        ready_p = prog(T_READY[0] + nd*0.1, T_READY[1])
        if ready_p > 0.5:
            status = "ready"
        elif cfg_p > 0.3:
            status = "configuring"
        else:
            status = "pending"

        glow = ease_out(prog(T_READY[0] + nd*0.1, T_READY[0] + nd*0.1 + 0.08)) if ready_p > 0.4 else 0
        draw_card(draw, node, na, status, glow)

    # Linhas SSH
    ctrl_cx, ctrl_cy = ctrl_center()
    line_delays = [0.00, 0.04, 0.08, 0.12]
    line_colors = [ORANGE, GREEN, GREEN, PURPLE]
    for i, node in enumerate(NODES):
        nd = line_delays[i]
        lp = ease_out(prog(T_LINES[0] + nd, T_LINES[1] + nd))
        nc = node_center(node)
        draw_ssh_line(draw, (ctrl_cx, ctrl_cy), nc, lp, line_colors[i])

    # Packets
    pkt_labels = ["haproxy", "nginx+php", "nginx+php", "mysql"]
    pkt_delays = [0.00, 0.04, 0.08, 0.12]
    for i, node in enumerate(NODES):
        nd = pkt_delays[i]
        pt = prog(T_PACKETS[0] + nd, T_PACKETS[1] + nd)
        if 0 < pt < 1:
            src = (ctrl_cx, ctrl_cy)
            dst = node_center(node)
            draw_packet(draw, src, dst, ease_in_out(pt),
                        pkt_labels[i], line_colors[i])

    # Terminal
    term_a = ease_out(prog(T_TERM[0], T_TERM[0] + 0.05))
    log_p  = prog(T_TERM[0] + 0.02, T_TERM[1] - 0.05)
    draw_terminal(draw, log_p, term_a)

    # Watermark
    draw.text((W - 150, H - 18), "fxshell | ansible lab",
              font=FONT_SM, fill=(*DIM, 150))

    return img.convert("RGB")

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print(f"Gerando {N_FRAMES} frames ({DURATION}s @ {FPS}fps)...")
    frames = []
    for i in range(N_FRAMES):
        if i % 10 == 0:
            print(f"  frame {i}/{N_FRAMES}")
        frames.append(render_frame(i))

    # Adiciona 2s de pausa no final
    pause = frames[-1]
    for _ in range(FPS * 2):
        frames.append(pause)

    frame_duration_ms = int(1000 / FPS)
    frames[0].save(
        OUT_FILE,
        save_all=True,
        append_images=frames[1:],
        optimize=False,
        duration=frame_duration_ms,
        loop=0,
    )
    size_kb = os.path.getsize(OUT_FILE) // 1024
    print(f"\n✔ GIF salvo em: {OUT_FILE}")
    print(f"  Tamanho: {size_kb} KB")
    print(f"  Resolução: {W}x{H}  |  Frames: {len(frames)}  |  Duração: ~{len(frames)//FPS}s")

if __name__ == "__main__":
    main()
