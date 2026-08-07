from PIL import Image, ImageDraw, ImageFont

BG_DARK = (28, 45, 44)
ACCENT_GREEN = (121, 152, 63)
TEXT_WHITE = (242, 241, 236)
TEXT_TAUPE = (162, 143, 129)

FONT_HEADLINE = "assets/fonts/League_Spartan/static/LeagueSpartan-Bold.ttf"
FONT_MONO = "assets/fonts/Roboto_Mono/static/RobotoMono-Bold.ttf"


def generate_ranking_graphic(rankings_df, title="WEEKLY RANKINGS", subtitle=""):
    W, H = 1080, 1080
    img = Image.new("RGB", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)

    title_font = ImageFont.truetype(FONT_HEADLINE, 64)
    subtitle_font = ImageFont.truetype(FONT_HEADLINE, 28)
    row_font = ImageFont.truetype(FONT_HEADLINE, 34)
    rank_font = ImageFont.truetype(FONT_MONO, 34)
    mpi_font = ImageFont.truetype(FONT_MONO, 34)
    footer_font = ImageFont.truetype(FONT_HEADLINE, 22)

    draw.text((60, 60), "MAINE-YBALL", font=subtitle_font, fill=ACCENT_GREEN)
    draw.text((60, 100), title.upper(), font=title_font, fill=TEXT_WHITE)
    if subtitle:
        draw.text((60, 175), subtitle.upper(), font=subtitle_font, fill=TEXT_TAUPE)

    y = 250
    row_height = 72

    for _, team in rankings_df.head(10).iterrows():
        draw.text((60, y), f"#{int(team['Rank'])}", font=rank_font, fill=ACCENT_GREEN)
        draw.text((160, y), team["Team"], font=row_font, fill=TEXT_WHITE)
        mpi_text = f"{team['MPI']:.1f}"
        w = draw.textlength(mpi_text, font=mpi_font)
        draw.text((W - 60 - w, y), mpi_text, font=mpi_font, fill=TEXT_TAUPE)
        draw.line([(60, y + row_height - 12), (W - 60, y + row_height - 12)],
                   fill=(255, 255, 255, 20), width=1)
        y += row_height

    draw.text((60, H - 60), "MAINE-YBALL.COM", font=footer_font, fill=TEXT_TAUPE)

    return img

def generate_movers_graphic(movers, title="BIGGEST MOVERS"):
    W, H = 1080, 1080
    img = Image.new("RGB", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)

    title_font = ImageFont.truetype(FONT_HEADLINE, 64)
    subtitle_font = ImageFont.truetype(FONT_HEADLINE, 28)
    row_font = ImageFont.truetype(FONT_HEADLINE, 32)
    delta_font = ImageFont.truetype(FONT_MONO, 32)
    footer_font = ImageFont.truetype(FONT_HEADLINE, 22)

    RISER_GREEN = (121, 152, 63)
    FALLER_RED = (184, 92, 74)

    draw.text((60, 60), "MAINE-YBALL", font=subtitle_font, fill=ACCENT_GREEN)
    draw.text((60, 100), title.upper(), font=title_font, fill=TEXT_WHITE)
    draw.text((60, 175), f"CHANGE SINCE {movers['baseline_label'].upper()}", font=subtitle_font, fill=TEXT_TAUPE)

    col_width = (W - 120) // 2
    row_height = 65

    draw.text((60, 250), "RISERS", font=row_font, fill=RISER_GREEN)
    y = 310
    for _, row in movers["risers"].head(5).iterrows():
        draw.text((60, y), row["Team"], font=row_font, fill=TEXT_WHITE)
        delta_text = f"+{row['Delta']:.1f}"
        w = draw.textlength(delta_text, font=delta_font)
        draw.text((60 + col_width - 40 - w, y), delta_text, font=delta_font, fill=RISER_GREEN)
        y += row_height

    x2 = 60 + col_width + 40
    draw.text((x2, 250), "FALLERS", font=row_font, fill=FALLER_RED)
    y = 310
    for _, row in movers["fallers"].head(5).iterrows():
        draw.text((x2, y), row["Team"], font=row_font, fill=TEXT_WHITE)
        delta_text = f"{row['Delta']:.1f}"
        w = draw.textlength(delta_text, font=delta_font)
        draw.text((x2 + col_width - 40 - w - 40, y), delta_text, font=delta_font, fill=FALLER_RED)
        y += row_height

    draw.text((60, H - 60), "MAINE-YBALL.COM", font=footer_font, fill=TEXT_TAUPE)

    return img