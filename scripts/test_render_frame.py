#!/usr/bin/env python3
"""
Test script to generate a rich, cybernetic 1920x1080 frame for Scene 1.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parent.parent
WORK_DIR = REPO_ROOT / "brag-output" / "work"


def get_font(size, bold=False, mono=False):
    if mono:
        return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", size, index=0)
    elif bold:
        return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size, index=1)
    else:
        return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size, index=0)


def draw_cyber_frame(
    scene_num, total_scenes, phase_tag, title_lines, subtitle, bullet_points, right_image_path=None
):
    W, H = 1920, 1080
    im = Image.new("RGBA", (W, H), (9, 13, 22, 255))
    draw = ImageDraw.Draw(im)

    # 1. Background grid & subtle glow lines
    for x in range(0, W, 80):
        draw.line([(x, 0), (x, H)], fill=(20, 30, 48, 80), width=1)
    for y in range(0, H, 80):
        draw.line([(0, y), (W, y)], fill=(20, 30, 48, 80), width=1)

    # Glowing radial / linear accent bar at top
    draw.line([(0, 2), (W, 2)], fill=(56, 189, 248, 180), width=3)
    draw.line([(0, 4), (W, 4)], fill=(168, 85, 247, 120), width=1)

    # 2. Header Bar (y: 20 to 80)
    font_header_title = get_font(20, bold=True)
    font_header_sub = get_font(16, mono=True)

    # Left brand
    draw.text((60, 32), "🚀 HSF v1.0", fill=(56, 189, 248, 255), font=font_header_title)
    draw.text(
        (195, 35),
        "•  HACKATHON STRATEGY FRAMEWORK",
        fill=(148, 163, 184, 255),
        font=font_header_sub,
    )

    # Center phase badge
    phase_str = f"SCENE 0{scene_num} / 0{total_scenes}  |  {phase_tag}"
    bbox_p = font_header_sub.getbbox(phase_str)
    pw = bbox_p[2] - bbox_p[0]
    px = (W - pw) // 2
    draw.rounded_rectangle(
        [(px - 16, 26), (px + pw + 16, 56)],
        radius=6,
        fill=(15, 23, 42, 220),
        outline=(56, 189, 248, 160),
        width=1,
    )
    draw.text((px, 35), phase_str, fill=(248, 250, 252, 255), font=font_header_sub)

    # Right telemetry chip
    telem_str = "SYSTEM: PRODUCTION-GRADE  •  20/20 PASS"
    draw.text((W - 520, 35), telem_str, fill=(16, 185, 129, 255), font=font_header_sub)

    # Separator
    draw.line([(60, 75), (W - 60, 75)], fill=(30, 41, 59, 200), width=1)

    # 3. Left Content Card (x: 60 to 780, y: 110 to 980)
    card_x1, card_y1, card_x2, card_y2 = 60, 110, 800, 980
    # Glass panel
    draw.rounded_rectangle(
        [(card_x1, card_y1), (card_x2, card_y2)],
        radius=16,
        fill=(15, 23, 42, 230),
        outline=(56, 189, 248, 90),
        width=2,
    )
    # Glowing top line on card
    draw.line(
        [(card_x1 + 16, card_y1 + 1), (card_x2 - 16, card_y1 + 1)],
        fill=(56, 189, 248, 200),
        width=2,
    )

    # Badge inside card
    font_badge = get_font(14, bold=True)
    draw.rounded_rectangle(
        [(card_x1 + 32, card_y1 + 32), (card_x1 + 380, card_y1 + 68)],
        radius=6,
        fill=(30, 58, 138, 160),
        outline=(56, 189, 248, 200),
        width=1,
    )
    draw.text(
        (card_x1 + 48, card_y1 + 43),
        "⚡ ENTERPRISE AGENTIC STACK",
        fill=(56, 189, 248, 255),
        font=font_badge,
    )

    # Title lines (Display font)
    font_title = get_font(38, bold=True)
    curr_y = card_y1 + 95
    for line in title_lines:
        draw.text((card_x1 + 32, curr_y), line, fill=(248, 250, 252, 255), font=font_title)
        curr_y += 48

    # Subtitle
    font_sub = get_font(18)
    draw.text((card_x1 + 32, curr_y + 10), subtitle, fill=(148, 163, 184, 255), font=font_sub)
    curr_y += 55

    # Divider inside card
    draw.line([(card_x1 + 32, curr_y), (card_x2 - 32, curr_y)], fill=(30, 41, 59, 255), width=1)
    curr_y += 30

    # Bullet points
    font_bp = get_font(19, bold=False)
    font_bp_icon = get_font(20, bold=True)
    for icon, text, highlight in bullet_points:
        # Bullet box
        draw.rounded_rectangle(
            [(card_x1 + 32, curr_y), (card_x2 - 32, curr_y + 80)],
            radius=10,
            fill=(11, 19, 36, 180),
            outline=(30, 41, 59, 180),
            width=1,
        )
        draw.text((card_x1 + 50, curr_y + 26), icon, fill=(56, 189, 248, 255), font=font_bp_icon)
        draw.text((card_x1 + 95, curr_y + 18), text, fill=(248, 250, 252, 255), font=font_bp)
        draw.text(
            (card_x1 + 95, curr_y + 46),
            highlight,
            fill=(56, 189, 248, 220),
            font=get_font(15, mono=True),
        )
        curr_y += 95

    # 4. Right Stage Area (x: 840 to 1860, y: 110 to 980)
    stage_x1, stage_y1, stage_x2, stage_y2 = 840, 110, 1860, 980
    draw.rounded_rectangle(
        [(stage_x1, stage_y1), (stage_x2, stage_y2)],
        radius=16,
        fill=(11, 18, 33, 240),
        outline=(168, 85, 247, 80),
        width=2,
    )
    # Glowing top line on stage
    draw.line(
        [(stage_x1 + 16, stage_y1 + 1), (stage_x2 - 16, stage_y1 + 1)],
        fill=(168, 85, 247, 200),
        width=2,
    )

    # Top stage label
    stage_header_font = get_font(15, mono=True)
    draw.text(
        (stage_x1 + 30, stage_y1 + 22),
        "ARCHIFY VERIFIED BLUEPRINT  |  SVG INTERACTIVE MATRIX",
        fill=(168, 85, 247, 240),
        font=stage_header_font,
    )
    draw.line(
        [(stage_x1 + 20, stage_y1 + 50), (stage_x2 - 20, stage_y1 + 50)],
        fill=(30, 41, 59, 200),
        width=1,
    )

    # Composite right blueprint image if provided
    if right_image_path and Path(right_image_path).exists():
        blueprint = Image.open(right_image_path).convert("RGBA")
        # Resize to fit within available stage area (max width 980, max height 780)
        max_w, max_h = 980, 770
        bw, bh = blueprint.size
        scale = min(max_w / bw, max_h / bh)
        new_w, new_h = int(bw * scale), int(bh * scale)
        blueprint_resized = blueprint.resize((new_w, new_h), Image.Resampling.LANCZOS)

        # Center inside stage
        dest_x = stage_x1 + (stage_x2 - stage_x1 - new_w) // 2
        dest_y = stage_y1 + 65 + (stage_y2 - stage_y1 - 65 - new_h) // 2
        im.alpha_composite(blueprint_resized, (dest_x, dest_y))

    # 5. Bottom Footer Ticker (y: 1010 to 1060)
    draw.line([(60, 1010), (W - 60, 1010)], fill=(30, 41, 59, 200), width=1)
    font_footer = get_font(15, mono=True)
    draw.text(
        (60, 1030),
        "⚡ $ npx hsf wizard  •  $ npx hsf leaderboard  •  $ npx hsf diagram all",
        fill=(56, 189, 248, 255),
        font=font_footer,
    )
    draw.text(
        (W - 550, 1030),
        "ORBIT MASCOT ACTIVE  •  STAGE FAIL-SAFE READY",
        fill=(148, 163, 184, 255),
        font=font_footer,
    )

    return im


if __name__ == "__main__":
    bullet_points = [
        ("⚡", "Zero-to-Production in 60s", "Automated init.sh bootstrap with Docker & Redis"),
        ("🛡️", "100% Type-Safe Architecture", "FastAPI 0.115+ with Pydantic v2 & OpenAPI 3.1"),
        ("🚀", "Sub-10ms P95 Responses", "Redis 7 Semantic Cache eliminates LLM bill shock"),
        ("🎯", "Zero-Hallucination Guardrails", "pgvector 16 hybrid RRF + RAGAS 0.94 faithfulness"),
    ]
    frame = draw_cyber_frame(
        scene_num=1,
        total_scenes=8,
        phase_tag="01. ZERO-TO-PRODUCTION FOUNDATION",
        title_lines=["HACKATHON STRATEGY", "FRAMEWORK (HSF v1.0)"],
        subtitle="The enterprise agentic blueprint built for hackathon victory.",
        bullet_points=bullet_points,
        right_image_path=WORK_DIR / "topology.png",
    )
    frame.save(WORK_DIR / "test_frame_1.png")
    print("Saved test_frame_1.png!")
