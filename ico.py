from PIL import Image, ImageDraw, ImageFilter

# ---------------------------
# CONFIGURAÇÃO
# ---------------------------
size = 512
img = Image.new("RGBA", (size, size), (20, 25, 35, 255))  # fundo escuro azulado visível
draw = ImageDraw.Draw(img)
center = size // 2

# ---------------------------
# GLOW EXTERNO (halo azul)
# ---------------------------
glow = Image.new("RGBA", img.size, (0, 5, 2, 0))
gdraw = ImageDraw.Draw(glow)
for i in range(80, 180, 5):
    alpha = max(0, 255 - (i - 80) * 3)
    gdraw.ellipse(
        [(center - i, center - i), (center + i, center + i)],
        fill=(0, 160, 255, alpha)
    )
glow = glow.filter(ImageFilter.GaussianBlur(25))
img = Image.alpha_composite(img, glow)

# ---------------------------
# FORMATO DA CABEÇA DO LYNX (simples e geométrico)
# ---------------------------
points = [
    (center - 180, center - 80),
    (center - 100, center - 220),
    (center - 20, center - 80),
    (center + 20, center - 80),
    (center + 100, center - 220),
    (center + 180, center - 80),
    (center + 130, center + 180),
    (center, center + 220),
    (center - 130, center + 180),
]
draw.polygon(points, fill=(25, 90, 150, 255), outline=(130, 220, 255, 255))

# ---------------------------
# OLHO CENTRAL
# ---------------------------
radius_outer = 70
radius_inner = 30

# anel externo do olho
draw.ellipse(
    [(center - radius_outer, center - radius_outer),
     (center + radius_outer, center + radius_outer)],
    fill=(60, 180, 255, 255),
    outline=(255, 255, 255, 200),
    width=5
)

# pupila
draw.ellipse(
    [(center - radius_inner, center - radius_inner),
     (center + radius_inner, center + radius_inner)],
    fill=(15, 35, 60, 255)
)

# reflexo branco
draw.ellipse(
    [(center - 12, center - 28), (center + 10, center - 10)],
    fill=(255, 255, 255, 180)
)

# brilho de energia interno
inner_glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
ig = ImageDraw.Draw(inner_glow)
for i in range(25, 90, 3):
    alpha = int(180 - (i - 25) * 2)
    ig.ellipse(
        [(center - i, center - i), (center + i, center + i)],
        fill=(80, 220, 255, alpha)
    )
inner_glow = inner_glow.filter(ImageFilter.GaussianBlur(8))
img = Image.alpha_composite(img, inner_glow)

# ---------------------------
# SUAVIZAÇÃO FINAL
# ---------------------------
img = img.filter(ImageFilter.GaussianBlur(0.5))

# ---------------------------
# SALVAR ÍCONE
# ---------------------------
img.save(
    "icon.ico",
    format="ICO",
    sizes=[(16, 16), (32, 32), (64, 64), (128, 128), (256, 256), (512, 512)]
)

print("✅ Ícone 'icon.ico' criado com sucesso! (visível e detalhado)")
