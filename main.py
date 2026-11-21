#!/usr/bin/env python3
"""
Passport spread generator for the Republic of Thaloria.
Draws an uncaptioned open passport spread (data page + stamps page) as a single PNG image
and saves it to /output/entry.png.
"""

import os
from PIL import Image, ImageDraw, ImageFont

def create_passport():
    # Ensure output directory exists
    os.makedirs("/output", exist_ok=True)
    
    # Image dimensions: 1000 x 700 pixels (within 1024x1024 limit)
    width, height = 1000, 700
    image = Image.new("RGB", (width, height), color="#f4f1ea") # Cream passport paper background
    draw = ImageDraw.Draw(image)
    
    # Colors (Restrained document palette)
    c_cover_spine = "#202c39" # Deep navy/charcoal spine shadow
    c_text = "#1a1a1a"
    c_muted = "#555555"
    c_accent = "#8b263e" # Burgundy stamp ink / security accent
    c_stamp_blue = "#1d3557" # Blue ink for arrival stamp
    c_grid = "#dcd6cd"
    
    # Draw center fold (spine shadow)
    fold_x = width // 2
    draw.rectangle([fold_x - 12, 0, fold_x + 12, height], fill="#eae4db")
    draw.line([(fold_x, 0), (fold_x, height)], fill="#b5ab9f", width=2)
    
    # Try loading fonts, fall back to default
    def get_font(size, bold=False):
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf" if bold else "/usr/share/fonts/truetype/freefont/FreeSans.ttf"
        ]
        for path in candidates:
            if os.path.exists(path):
                try:
                    return ImageFont.load_default() # Fallback safely or use truetype if available
                except Exception:
                    pass
        return ImageFont.load_default()

    font_title = get_font(16, True)
    font_body = get_font(12, False)
    font_bold = get_font(12, True)
    font_small = get_font(10, False)
    font_mrz = get_font(13, False)
    
    # ----------------------------------------------------
    # LEFT PAGE: DATA PAGE (Republic of Thaloria)
    # ----------------------------------------------------
    left_margin = 50
    
    # Header: Country Name and Document Type
    draw.text((left_margin, 40), "REPUBLIKEN THALORIA", fill=c_text, font=font_title)
    draw.text((left_margin, 62), "REPUBLIC OF THALORIA / PASSPORT / PASSEPORT", fill=c_muted, font=font_small)
    
    # Security guilloche header line
    draw.line([(left_margin, 85), (fold_x - 30, 85)], fill=c_accent, width=2)
    
    # Portrait Box
    photo_box = [left_margin, 110, left_margin + 160, 230]
    draw.rectangle(photo_box, outline=c_muted, width=2, fill="#e5dfd5")
    # Draw a stylized procedural portrait inside the photo box
    # Silhouette shoulders
    draw.ellipse([left_margin + 40, photo_box[3] - 45, left_margin + 120, photo_box[3] + 30], fill="#333333")
    # Head
    draw.ellipse([left_margin + 55, photo_box[1] + 35, left_margin + 105, photo_box[1] + 100], fill="#d0c0b0")
    # Hair
    draw.arc([left_margin + 52, photo_box[1] + 28, left_margin + 108, photo_box[1] + 90], start=180, end=360, fill="#222222", width=8)
    
    # Render holder identity fields in two-column layout with consistent vertical spacing
    details_x = left_margin + 185
    y_cursor = 105  # Adjusted starting y coordinate for balanced top margin alignment
    
    fields = [
        ("Type / Type", "P"),
        ("Country Code / Code", "THL"),
        ("Passport No. / No.", "AB1234567"),
        ("Surname / Nom", "VANE"),
        ("Given Names / Prenoms", "ASTRID LIND"),
        ("Nationality / Nationalite", "THALORIAN"),
        ("Date of birth / Date de naissance", "14 MAR 1985"),
        ("Sex / Sexe", "F"),
        ("Place of birth / Lieu de naissance", "PORT THALOR"),
        ("Date of issue / Date de delivrance", "14 MAR 2018"),
        ("Date of expiry / Date d'expiration", "13 MAR 2028"),
        ("Authority / Autorite", "MINISTRY OF INTERIOR")
    ]
    
    for label, val in fields:
        draw.text((details_x, y_cursor), label, fill=c_muted, font=font_small)
        draw.text((details_x, y_cursor + 12), val, fill=c_text, font=font_bold)
        y_cursor += 31  # Fine-tuned row pitch for perfect vertical rhythm
        
    # Machine Readable Zone (MRZ) at bottom of left page
    mrz_y = 600
    mrz_lines = [
        "P<THLVANE<<ASTRID<LIND<<<<<<<<<<<<<<<<<<<<<<",
        "AB12345678THL8503145F2803135<<<<<<<<<<<<<<0"
    ]
    for i, line in enumerate(mrz_lines):
        draw.text((left_margin, mrz_y + i * 20), line, fill=c_text, font=font_mrz)
        
    # ----------------------------------------------------
    # RIGHT PAGE: VISAS, STAMPS & TELLING PAPERWORK DETAIL
    # ----------------------------------------------------
    right_margin = fold_x + 40
    
    draw.text((right_margin, 40), "VISAS / ENTRY & EXIT ENDORSEMENTS", fill=c_muted, font=font_small)
    draw.line([(right_margin, 58), (width - 50, 58)], fill=c_grid, width=1)
    
    # Telling paperwork detail box: State Fisheries & Tallow Export Quota Certification
    # This reveals the character of Thaloria: a remote sub-arctic republic whose economy and border control revolve around strict maritime/fisheries quotas and salted goods inspection.
    detail_box = [right_margin, 75, width - 50, 220]
    draw.rectangle(detail_box, outline=c_accent, width=1, fill="#eae4db")
    draw.text((right_margin + 12, data_y := 87), "STATE MARITIME & FISHERIES INSPECTORATE", fill=c_accent, font=font_bold)
    endorsement_text = [
        "ARTICLE 42: Mandatory Tallow & Herring Export Transit Endorsement.",
        "Holder is certified exempt from coastal transit tariffs under the",
        "1994 North-Eastern Pelagic Treaty. All catches inspected and sealed.",
        "",
        "Issued at Port Thalor Customs House. Stamp fee: 40 Kronur."
    ]
    ey = data_y + 20
    for line in endorsement_text:
        draw.text((right_margin + 12, ey), line, fill=c_text, font=font_small)
        ey += 16
        
    # Official Embossed Seal / Fee Stamp on Right Page
    seal_center = (right_margin + 90, 310)
    draw.ellipse([seal_center[0] - 45, seal_center[1] - 45, seal_center[0] + 45, seal_center[1] + 45], outline=c_accent, width=2)
    draw.ellipse([seal_center[0] - 37, seal_center[1] - 37, seal_center[0] + 37, seal_center[1] + 37], outline=c_accent, width=1)
    draw.text((seal_center[0] - 28, seal_center[1] - 5), "SEAL", fill=c_accent, font=font_small)
    
    # Travel History Stamps (Border control arrival and departure stamps)
    # Stamp 1: Departure Port Thalor (Thaloria) - 12 JUN 2019
    s1_box = [right_margin + 170, 250, right_margin + 340, 370]
    draw.rectangle(s1_box, outline=c_accent, width=2)
    draw.text((s1_box[0] + 6, s1_box[1] + 6), "REP. THALORIA", fill=c_accent, font=font_small)
    draw.text((s1_box[0] + 6, s1_box[1] + 24), "PORT THALOR - DEP", fill=c_text, font=font_bold)
    draw.text((s1_box[0] + 6, s1_box[1] + 46), "DATE: 12 JUN 2019", fill=c_text, font=font_small)
    draw.text((s1_box[0] + 6, s1_box[1] + 64), "GATE 4 - MV NORTHWIND", fill=c_muted, font=font_small)
    
    # Stamp 2: Arrival Borealia (Neighboring country) - 13 JUN 2019
    s2_box = [right_margin + 20, 390, right_margin + 180, 510]
    draw.rectangle(s2_box, outline=c_stamp_blue, width=2)
    draw.text((s2_box[0] + 6, s2_box[1] + 6), "FED. REP. BOREALIA", fill=c_stamp_blue, font=font_small)
    draw.text((s2_box[0] + 6, s2_box[1] + 24), "PORT NORTH - ARR", fill=c_text, font=font_bold)
    draw.text((s2_box[0] + 6, s2_box[1] + 46), "DATE: 13 JUN 2019", fill=c_text, font=font_small)
    draw.text((s2_box[0] + 6, s2_box[1] + 64), "IMMIGRATION", fill=c_muted, font=font_small)
    
    # Stamp 3: Departure Borealia - 28 JUN 2019
    s3_box = [right_margin + 200, 390, right_margin + 360, 510]
    draw.rectangle(s3_box, outline=c_stamp_blue, width=2)
    draw.text((s3_box[0] + 6, s3_box[1] + 6), "FED. REP. BOREALIA", fill=c_stamp_blue, font=font_small)
    draw.text((s3_box[0] + 6, s3_box[1] + 24), "PORT NORTH - DEP", fill=c_text, font=font_bold)
    draw.text((s3_box[0] + 6, s3_box[1] + 46), "DATE: 28 JUN 2019", fill=c_text, font=font_small)
    draw.text((s3_box[0] + 6, s3_box[1] + 64), "CHECKPOINT B", fill=c_muted, font=font_small)
    
    # Save image
    image.save("/output/entry.png", "PNG")
    print("Passport spread generated successfully at /output/entry.png")

if __name__ == "__main__":
    create_passport()
