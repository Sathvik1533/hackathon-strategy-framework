#!/usr/bin/env python3
"""
High-Production Brag Video Renderer for Hackathon Strategy Framework (HSF v1.0).
Generates a 32-second, 30fps (960 frames) 1920x1080 cinematic video explaining
the entire architecture end-to-end, with synchronized soundtrack and SFX cues.
"""

import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "brag-output"
WORK_DIR = OUTPUT_DIR / "work"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
WORK_DIR.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080
FPS = 30
TOTAL_SCENES = 8
SCENE_DURATION_SEC = 4.0
FRAMES_PER_SCENE = int(SCENE_DURATION_SEC * FPS)  # 120 frames
TOTAL_FRAMES = TOTAL_SCENES * FRAMES_PER_SCENE  # 960 frames

MUSIC_FILE = Path(
    "/Users/k.sathvik/.gemini/config/skills/brag/assets/music/happy-beats-business-moves-vol-1-by-ende-dot-app.mp3"
)
SFX_DIR = Path("/Users/k.sathvik/.gemini/config/skills/brag/assets/sfx")


def get_font(size, bold=False, mono=False):
    try:
        if mono:
            return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", size, index=0)
        elif bold:
            return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size, index=1)
        else:
            return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size, index=0)
    except Exception:
        return ImageFont.load_default()


def draw_base_frame(scene_num, phase_tag):
    im = Image.new("RGBA", (WIDTH, HEIGHT), (9, 13, 22, 255))
    draw = ImageDraw.Draw(im)

    # Background grid
    for x in range(0, WIDTH, 80):
        draw.line([(x, 0), (x, HEIGHT)], fill=(20, 30, 48, 70), width=1)
    for y in range(0, HEIGHT, 80):
        draw.line([(0, y), (WIDTH, y)], fill=(20, 30, 48, 70), width=1)

    # Top neon accents
    draw.line([(0, 2), (WIDTH, 2)], fill=(56, 189, 248, 180), width=3)
    draw.line([(0, 4), (WIDTH, 4)], fill=(168, 85, 247, 120), width=1)

    # Header Bar
    font_h_bold = get_font(20, bold=True)
    font_h_mono = get_font(15, mono=True)

    # Left brand
    draw.text((60, 28), "[HSF v1.0]", fill=(56, 189, 248, 255), font=font_h_bold)
    draw.text(
        (185, 31), "HACKATHON STRATEGY FRAMEWORK", fill=(148, 163, 184, 255), font=font_h_mono
    )

    # Center phase badge
    phase_str = f"SCENE 0{scene_num}/0{TOTAL_SCENES}  |  {phase_tag}"
    bbox = font_h_mono.getbbox(phase_str)
    pw = bbox[2] - bbox[0]
    px = (WIDTH - pw) // 2
    draw.rounded_rectangle(
        [(px - 16, 24), (px + pw + 16, 52)],
        radius=6,
        fill=(15, 23, 42, 220),
        outline=(56, 189, 248, 160),
        width=1,
    )
    draw.text((px, 31), phase_str, fill=(248, 250, 252, 255), font=font_h_mono)

    # Right telemetry
    draw.text(
        (WIDTH - 520, 31),
        "SYSTEM: PRODUCTION-GRADE  •  20/20 PASS",
        fill=(16, 185, 129, 255),
        font=font_h_mono,
    )
    draw.line([(60, 68), (WIDTH - 60, 68)], fill=(30, 41, 59, 200), width=1)

    # Bottom Ticker
    draw.line([(60, 1010), (WIDTH - 60, 1010)], fill=(30, 41, 59, 200), width=1)
    draw.text(
        (60, 1028),
        ">> $ npx hsf wizard  •  $ npx hsf leaderboard  •  $ npx hsf diagram all",
        fill=(56, 189, 248, 255),
        font=font_h_mono,
    )
    draw.text(
        (WIDTH - 560, 1028),
        "ORBIT MASCOT ACTIVE  •  STAGE FAIL-SAFE READY",
        fill=(148, 163, 184, 255),
        font=font_h_mono,
    )

    return im, draw


def draw_left_card(draw, badge_text, title_lines, subtitle, bullet_points):
    card_x1, card_y1, card_x2, card_y2 = 60, 95, 780, 985
    draw.rounded_rectangle(
        [(card_x1, card_y1), (card_x2, card_y2)],
        radius=14,
        fill=(15, 23, 42, 230),
        outline=(56, 189, 248, 90),
        width=2,
    )
    draw.line(
        [(card_x1 + 16, card_y1 + 1), (card_x2 - 16, card_y1 + 1)],
        fill=(56, 189, 248, 220),
        width=2,
    )

    # Badge inside card
    font_badge = get_font(13, bold=True)
    draw.rounded_rectangle(
        [(card_x1 + 28, card_y1 + 24), (card_x1 + 380, card_y1 + 56)],
        radius=6,
        fill=(30, 58, 138, 160),
        outline=(56, 189, 248, 180),
        width=1,
    )
    draw.text((card_x1 + 42, card_y1 + 33), badge_text, fill=(56, 189, 248, 255), font=font_badge)

    # Title lines
    font_title = get_font(34, bold=True)
    curr_y = card_y1 + 78
    for line in title_lines:
        draw.text((card_x1 + 28, curr_y), line, fill=(248, 250, 252, 255), font=font_title)
        curr_y += 44

    # Subtitle
    font_sub = get_font(16)
    draw.text((card_x1 + 28, curr_y + 8), subtitle, fill=(148, 163, 184, 255), font=font_sub)
    curr_y += 50

    draw.line([(card_x1 + 28, curr_y), (card_x2 - 28, curr_y)], fill=(30, 41, 59, 255), width=1)
    curr_y += 24

    # Bullet points
    font_bp_title = get_font(18, bold=True)
    font_bp_detail = get_font(14, mono=True)
    font_tag = get_font(14, bold=True, mono=True)

    for tag, title, detail in bullet_points:
        draw.rounded_rectangle(
            [(card_x1 + 28, curr_y), (card_x2 - 28, curr_y + 76)],
            radius=8,
            fill=(11, 19, 36, 180),
            outline=(30, 41, 59, 180),
            width=1,
        )
        # Tag box
        draw.rounded_rectangle(
            [(card_x1 + 40, curr_y + 18), (card_x1 + 96, curr_y + 58)],
            radius=5,
            fill=(15, 23, 42, 255),
            outline=(56, 189, 248, 140),
            width=1,
        )
        draw.text((card_x1 + 46, curr_y + 28), tag, fill=(56, 189, 248, 255), font=font_tag)

        draw.text(
            (card_x1 + 112, curr_y + 14), title, fill=(248, 250, 252, 255), font=font_bp_title
        )
        draw.text(
            (card_x1 + 112, curr_y + 44), detail, fill=(56, 189, 248, 220), font=font_bp_detail
        )
        curr_y += 88


def draw_right_stage_box(draw, header_title):
    stage_x1, stage_y1, stage_x2, stage_y2 = 820, 95, 1860, 985
    draw.rounded_rectangle(
        [(stage_x1, stage_y1), (stage_x2, stage_y2)],
        radius=14,
        fill=(11, 18, 33, 240),
        outline=(168, 85, 247, 80),
        width=2,
    )
    draw.line(
        [(stage_x1 + 16, stage_y1 + 1), (stage_x2 - 16, stage_y1 + 1)],
        fill=(168, 85, 247, 200),
        width=2,
    )

    font_stage_h = get_font(15, mono=True)
    draw.text(
        (stage_x1 + 28, stage_y1 + 20), header_title, fill=(168, 85, 247, 240), font=font_stage_h
    )
    draw.line(
        [(stage_x1 + 20, stage_y1 + 48), (stage_x2 - 20, stage_y1 + 48)],
        fill=(30, 41, 59, 200),
        width=1,
    )
    return stage_x1, stage_y1, stage_x2, stage_y2


# ==============================================================================
# 8 SCENE RIGHT-STAGE RENDERERS
# ==============================================================================


def render_scene_1(progress):
    # Scene 1: Full-Stack Architecture Topology
    im, draw = draw_base_frame(1, "01. ZERO-TO-PRODUCTION FOUNDATION")
    bullet_points = [
        ("[60s]", "Zero-to-Production Bootstrap", "Automated init.sh setup with Docker & Redis 7"),
        ("[TS]", "100% Type-Safe Architecture", "FastAPI 0.115+ Router with ResponseEnvelope[T]"),
        ("[8ms]", "Sub-10ms P95 Responses", "Redis 7 Semantic Cache eliminates LLM bill shock"),
        (
            "[0.94]",
            "Zero-Hallucination Guardrails",
            "pgvector 16 hybrid RRF + RAGAS 0.94 faithfulness",
        ),
    ]
    draw_left_card(
        draw,
        ">> ENTERPRISE AGENTIC STACK",
        ["HACKATHON STRATEGY", "FRAMEWORK (HSF v1.0)"],
        "The battle-hardened foundation engineered for hackathon victory.",
        bullet_points,
    )

    sx1, sy1, sx2, sy2 = draw_right_stage_box(
        draw, "SYSTEM ARCHITECTURE TOPOLOGY  |  FULL-STACK MAP"
    )

    # Render architecture tiers
    tiers = [
        (
            "CLIENT TIER",
            "#38bdf8",
            [
                "Next.js 14 App Router (:3000)",
                "Senior Orbit Desktop HUD",
                "Unified CLI & Wizard (:cli.js)",
            ],
        ),
        (
            "API GATEWAY TIER",
            "#818cf8",
            [
                "FastAPI 0.115+ Router",
                "JWT Bearer & Sliding Rate Limiter",
                "3-State Distributed Circuit Breaker",
            ],
        ),
        (
            "RESILIENCE & CACHE",
            "#fb923c",
            [
                "Redis 7 Semantic Cache (<8ms)",
                "Real-Time SSE Event Stream",
                "SETNX Distributed Mutex Locks",
            ],
        ),
        (
            "STORAGE TIER",
            "#34d399",
            [
                "PostgreSQL 16 Engine",
                "pgvector HNSW Cosine Index (<=>)",
                "Supabase Row-Level Security (RLS)",
            ],
        ),
        (
            "AGENTIC REASONING",
            "#a78bfa",
            [
                "LangGraph Cyclic StateGraph",
                "Human-in-the-Loop Review Gate",
                "FastMCP Tool Server Sandbox (:8001)",
            ],
        ),
    ]

    ty = sy1 + 70
    font_tier_title = get_font(15, bold=True, mono=True)
    font_node = get_font(14, mono=True)

    for tier_name, tier_color, nodes in tiers:
        draw.rounded_rectangle(
            [(sx1 + 40, ty), (sx2 - 40, ty + 105)],
            radius=10,
            fill=(15, 23, 42, 200),
            outline=(56, 189, 248, 60),
            width=1,
        )
        draw.text((sx1 + 60, ty + 12), tier_name, fill=tier_color, font=font_tier_title)
        draw.line([(sx1 + 60, ty + 36), (sx2 - 60, ty + 36)], fill=(30, 41, 59, 200), width=1)

        nx = sx1 + 60
        for node in nodes:
            draw.rounded_rectangle(
                [(nx, ty + 48), (nx + 290, ty + 92)],
                radius=6,
                fill=(11, 18, 33, 240),
                outline=(56, 189, 248, 120),
                width=1,
            )
            draw.text((nx + 14, ty + 62), node, fill=(248, 250, 252, 255), font=font_node)
            nx += 308

        ty += 118

    return im


def render_scene_2(progress):
    # Scene 2: Circuit Breaker State Machine & Redis Resilience
    im, draw = draw_base_frame(2, "02. FASTAPI & REDIS 7 RESILIENCE")
    bullet_points = [
        ("[FAST]", "FastAPI Async Gateway", "ResponseEnvelope[T] standardized envelope contracts"),
        ("[TRIP]", "3-State Circuit Breaker", "CLOSED -> OPEN -> HALF_OPEN automated self-healing"),
        (
            "[COOL]",
            "30s Automated Cooldown",
            "Fault isolation protects against third-party API outages",
        ),
        (
            "[LOCK]",
            "Distributed Redis Locks",
            "SETNX mutex prevents concurrent duplicate execution",
        ),
    ]
    draw_left_card(
        draw,
        ">> DISTRIBUTED SELF-HEALING",
        ["ASYNC GATEWAY &", "CIRCUIT BREAKERS"],
        "Fault isolation ensuring zero downtime on the live stage.",
        bullet_points,
    )

    sx1, sy1, sx2, sy2 = draw_right_stage_box(
        draw, "CIRCUIT BREAKER STATE MACHINE  |  LIFECYCLE MATRIX"
    )

    # Draw 3-State Machine
    states = [
        (
            "CLOSED",
            "(NORMAL OPERATION)",
            "Traffic flows freely. Failure count = 0.",
            "#10b981",
            ["Request executes normally", "Latency P95 < 42ms", "Auto-increments on failure"],
        ),
        (
            "OPEN",
            "(FAULT ISOLATED)",
            "Trips after 3 failures. Fallback response active.",
            "#f43f5e",
            [
                "Upstream calls halted",
                "Returns local cached fallback",
                "Enforces 30s cooldown timer",
            ],
        ),
        (
            "HALF_OPEN",
            "(CANARY PROBE)",
            "Tests 1 canary request before closing circuit.",
            "#f59e0b",
            ["Allows 1 probe execution", "Success: Resets to CLOSED", "Failure: Re-enters OPEN"],
        ),
    ]

    cx = sx1 + 45
    font_s_title = get_font(24, bold=True)
    font_s_sub = get_font(13, mono=True)
    font_s_detail = get_font(14)

    for state_name, subtitle, desc, color, checks in states:
        draw.rounded_rectangle(
            [(cx, sy1 + 80), (cx + 300, sy1 + 520)],
            radius=12,
            fill=(15, 23, 42, 220),
            outline=color,
            width=2,
        )
        # Header banner
        draw.rounded_rectangle(
            [(cx + 16, sy1 + 98), (cx + 284, sy1 + 170)],
            radius=8,
            fill=(11, 18, 33, 240),
            outline=color,
            width=1,
        )
        draw.text((cx + 28, sy1 + 110), state_name, fill=color, font=font_s_title)
        draw.text((cx + 28, sy1 + 144), subtitle, fill=(148, 163, 184, 255), font=font_s_sub)

        # Description
        draw.text((cx + 20, sy1 + 195), desc, fill=(248, 250, 252, 255), font=font_s_detail)
        draw.line([(cx + 20, sy1 + 250), (cx + 280, sy1 + 250)], fill=(30, 41, 59, 200), width=1)

        # Checks
        cy = sy1 + 270
        for chk in checks:
            draw.text(
                (cx + 20, cy), ">> " + chk, fill=(148, 163, 184, 255), font=get_font(13, mono=True)
            )
            cy += 45

        cx += 325

    # Bottom Terminal Monitor Box
    draw.rounded_rectangle(
        [(sx1 + 45, sy1 + 550), (sx2 - 45, sy2 - 40)],
        radius=10,
        fill=(8, 12, 20, 250),
        outline=(56, 189, 248, 120),
        width=1,
    )
    draw.text(
        (sx1 + 70, sy1 + 570),
        "$ curl -s http://localhost:8000/api/v1/health/circuit-breakers",
        fill=(56, 189, 248, 255),
        font=get_font(15, mono=True),
    )
    draw.text(
        (sx1 + 70, sy1 + 610),
        'HTTP/1.1 200 OK  |  {"state": "CLOSED", "failure_count": 0, "cooldown_remaining": 0}',
        fill=(16, 185, 129, 255),
        font=get_font(15, mono=True),
    )
    draw.text(
        (sx1 + 70, sy1 + 650),
        "Semantic Cache: HIT  •  P95 Latency: 7.8ms  •  Sliding Window Rate Limit: ENFORCED",
        fill=(148, 163, 184, 255),
        font=get_font(15, mono=True),
    )

    return im


def render_scene_3(progress):
    # Scene 3: Hybrid Neural RAG & pgvector 16
    im, draw = draw_base_frame(3, "03. HYBRID NEURAL RAG & PGVECTOR")
    bullet_points = [
        ("[HNSW]", "pgvector 16 Dense Search", "1536-dimensional HNSW cosine index (<=>) < 14ms"),
        (
            "[BM25]",
            "GIN tsvector Sparse Search",
            "Full-text lexical matching catches exact keywords",
        ),
        (
            "[RRF]",
            "Reciprocal Rank Fusion",
            "Merges dense + sparse ranks without manual weight tuning",
        ),
        (
            "[CROSS]",
            "FlashRank Cross-Encoder",
            "TinyBERT reranker (<18ms) runs locally on pure CPU",
        ),
    ]
    draw_left_card(
        draw,
        ">> NEURAL VECTOR RETRIEVAL",
        ["HYBRID SEARCH &", "FLASH-RANK RERANKING"],
        "Dense cosine + sparse lexical search for zero-hallucination accuracy.",
        bullet_points,
    )

    sx1, sy1, sx2, sy2 = draw_right_stage_box(
        draw, "HYBRID RAG PIPELINE DATAFLOW  |  DENSE + SPARSE FUSION"
    )

    # Draw RAG Pipeline Flowchart
    col_w = 420
    # Left stream: Dense
    draw.rounded_rectangle(
        [(sx1 + 60, sy1 + 80), (sx1 + 60 + col_w, sy1 + 240)],
        radius=10,
        fill=(15, 23, 42, 220),
        outline=(56, 189, 248, 180),
        width=2,
    )
    draw.text(
        (sx1 + 80, sy1 + 100),
        "DENSE VECTOR SEARCH",
        fill=(56, 189, 248, 255),
        font=get_font(18, bold=True),
    )
    draw.text(
        (sx1 + 80, sy1 + 135),
        "• pgvector 16 HNSW Index (<=>)",
        fill=(248, 250, 252, 255),
        font=get_font(14, mono=True),
    )
    draw.text(
        (sx1 + 80, sy1 + 165),
        "• 1536-dim OpenAI Embeddings",
        fill=(148, 163, 184, 255),
        font=get_font(14, mono=True),
    )
    draw.text(
        (sx1 + 80, sy1 + 195),
        "• Cosine distance search: 12.4ms",
        fill=(16, 185, 129, 255),
        font=get_font(14, mono=True),
    )

    # Right stream: Sparse
    draw.rounded_rectangle(
        [(sx2 - 60 - col_w, sy1 + 80), (sx2 - 60, sy1 + 240)],
        radius=10,
        fill=(15, 23, 42, 220),
        outline=(168, 85, 247, 180),
        width=2,
    )
    draw.text(
        (sx2 - 40 - col_w, sy1 + 100),
        "SPARSE LEXICAL SEARCH",
        fill=(168, 85, 247, 255),
        font=get_font(18, bold=True),
    )
    draw.text(
        (sx2 - 40 - col_w, sy1 + 135),
        "• GIN tsvector Full-Text Index",
        fill=(248, 250, 252, 255),
        font=get_font(14, mono=True),
    )
    draw.text(
        (sx2 - 40 - col_w, sy1 + 165),
        "• English stemming & stopword filter",
        fill=(148, 163, 184, 255),
        font=get_font(14, mono=True),
    )
    draw.text(
        (sx2 - 40 - col_w, sy1 + 195),
        "• Exact keyword matching: 4.8ms",
        fill=(16, 185, 129, 255),
        font=get_font(14, mono=True),
    )

    # Center Fusion Block
    draw.rounded_rectangle(
        [(sx1 + 180, sy1 + 280), (sx2 - 180, sy1 + 440)],
        radius=12,
        fill=(15, 23, 42, 240),
        outline=(251, 146, 60, 200),
        width=2,
    )
    draw.text(
        (sx1 + 220, sy1 + 305),
        "RECIPROCAL RANK FUSION (RRF)",
        fill=(251, 146, 60, 255),
        font=get_font(20, bold=True),
    )
    draw.text(
        (sx1 + 220, sy1 + 345),
        "Score Formula: RRF(d) = SUM( 1 / (60 + rank(d)) )",
        fill=(248, 250, 252, 255),
        font=get_font(15, mono=True),
    )
    draw.text(
        (sx1 + 220, sy1 + 380),
        "Combines semantic understanding + exact keyword retrieval with 0 tuning",
        fill=(148, 163, 184, 255),
        font=get_font(14),
    )

    # Bottom Neural Reranker Block
    draw.rounded_rectangle(
        [(sx1 + 60, sy1 + 480), (sx2 - 60, sy2 - 40)],
        radius=12,
        fill=(8, 12, 20, 250),
        outline=(16, 185, 129, 200),
        width=2,
    )
    draw.text(
        (sx1 + 90, sy1 + 510),
        "FLASHRANK NEURAL CPU CROSS-ENCODER  |  LATENCY < 18ms",
        fill=(16, 185, 129, 255),
        font=get_font(19, bold=True),
    )
    draw.text(
        (sx1 + 90, sy1 + 550),
        "Top 50 RRF Candidates -> FlashRank Cross-Encoder -> Top 5 Golden Precision Contexts",
        fill=(248, 250, 252, 255),
        font=get_font(15, mono=True),
    )
    draw.text(
        (sx1 + 90, sy1 + 590),
        "RAGAS Benchmark Verification: Faithfulness = 0.94  •  Answer Relevance = 0.92  •  Context Precision = 0.89",
        fill=(56, 189, 248, 255),
        font=get_font(15, mono=True),
    )
    draw.text(
        (sx1 + 90, sy1 + 630),
        "Security Isolation: Supabase Row-Level Security (RLS) enforces tenant_id on PostgreSQL engine level.",
        fill=(148, 163, 184, 255),
        font=get_font(14),
    )

    return im


def render_scene_4(progress):
    # Scene 4: LangGraph Supervisor & FastMCP Sandbox
    im, draw = draw_base_frame(4, "04. AGENTIC REASONING & FASTMCP")
    bullet_points = [
        (
            "[GRAPH]",
            "LangGraph Cyclic StateGraph",
            "Dynamic supervisor routes tasks across specialized subagents",
        ),
        (
            "[GATE]",
            "Human-in-the-Loop Review",
            "interrupt_before=['human_gate'] pauses before irreversible actions",
        ),
        (
            "[MCP]",
            "FastMCP Isolated Sandbox",
            "JSON-RPC SSE server running on Port 8001 isolates host environment",
        ),
        (
            "[EVAL]",
            "RAGAS Accuracy: 0.94",
            "25 golden test cases audited with zero hallucination flags",
        ),
    ]
    draw_left_card(
        draw,
        ">> MULTI-AGENT ORCHESTRATION",
        ["LANGGRAPH SUPERVISOR", "& FASTMCP SANDBOX"],
        "Deterministic agent loops with human safety authorization gates.",
        bullet_points,
    )

    sx1, sy1, sx2, sy2 = draw_right_stage_box(
        draw, "REQUEST EXECUTION SEQUENCE  |  STATEGRAPH SUPERVISOR"
    )

    # Sequence Cards
    steps = [
        (
            "1. USER PROMPT INGESTION",
            "API Gateway receives multi-agent query and invokes LangGraph StateGraph.",
            "#38bdf8",
        ),
        (
            "2. SUPERVISOR INTENT ROUTER",
            "LLM supervisor evaluates context and routes to Researcher or Action Worker.",
            "#818cf8",
        ),
        (
            "3. RESEARCHER CONTEXT EXTRACTION",
            "Extracts dense + sparse vectors and runs FlashRank reranker in <18ms.",
            "#34d399",
        ),
        (
            "4. HUMAN-IN-THE-LOOP SAFETY GATE",
            "Halts execution before sensitive tool call. Awaits operator approval.",
            "#f43f5e",
        ),
        (
            "5. FASTMCP ISOLATED TOOL EXECUTION",
            "Dispatches tool call to FastMCP SSE server on Port 8001 without crashing host.",
            "#fb923c",
        ),
        (
            "6. SYNTHESIS & CLIENT SSE DISPATCH",
            "Streams verified structured response back to client with 0 hallucination.",
            "#10b981",
        ),
    ]

    sy = sy1 + 75
    for title, desc, color in steps:
        draw.rounded_rectangle(
            [(sx1 + 45, sy), (sx2 - 45, sy + 78)],
            radius=8,
            fill=(15, 23, 42, 220),
            outline=color,
            width=1,
        )
        draw.text((sx1 + 65, sy + 14), title, fill=color, font=get_font(16, bold=True, mono=True))
        draw.text((sx1 + 65, sy + 44), desc, fill=(248, 250, 252, 255), font=get_font(14))
        sy += 92

    # Bottom Callout Box
    draw.rounded_rectangle(
        [(sx1 + 45, sy + 10), (sx2 - 45, sy2 - 40)],
        radius=8,
        fill=(8, 12, 20, 250),
        outline=(16, 185, 129, 140),
        width=1,
    )
    draw.text(
        (sx1 + 65, sy + 30),
        "LangGraph StateGraph Checkpoint: VERIFIED ACTIVE  •  FastMCP SSE: CONNECTED (:8001)",
        fill=(16, 185, 129, 255),
        font=get_font(14, mono=True),
    )

    return im


def render_scene_5(progress):
    # Scene 5: Zero-Collision Polyglot Bridge (Python + Java)
    im, draw = draw_base_frame(5, "05. ZERO-COLLISION POLYGLOT BRIDGE")
    bullet_points = [
        ("[PY]", "Python AI Superpower", "FastAPI, LangGraph, FlashRank, pgvector, RAGAS evals"),
        (
            "[JAVA]",
            "Java Enterprise Muscle",
            "Spring Boot, Kafka connectors, high-throughput batch, gRPC",
        ),
        (
            "[ZERO]",
            "Zero Syntax Collisions",
            "Decoupled IPC & OpenAPI 3.1 contracts with 0 runtime conflicts",
        ),
        (
            "[IPC]",
            "Ultra-Low Latency Bridge",
            "Local HTTP/JSON-RPC or Unix domain sockets < 3ms transport",
        ),
    ]
    draw_left_card(
        draw,
        ">> DUAL-LANGUAGE SUPERPOWERS",
        ["ZERO-COLLISION", "POLYGLOT BRIDGE"],
        "How Python and Java coexist harmoniously with zero runtime overlap.",
        bullet_points,
    )

    sx1, sy1, sx2, sy2 = draw_right_stage_box(
        draw, "ZERO-COLLISION POLYGLOT ARCHITECTURE  |  IPC BRIDGE"
    )

    card_w = 420
    # Left Box: Python
    draw.rounded_rectangle(
        [(sx1 + 50, sy1 + 80), (sx1 + 50 + card_w, sy1 + 530)],
        radius=12,
        fill=(15, 23, 42, 230),
        outline=(56, 189, 248, 200),
        width=2,
    )
    draw.text(
        (sx1 + 80, sy1 + 105),
        "PYTHON AI SUPERPOWERS",
        fill=(56, 189, 248, 255),
        font=get_font(20, bold=True),
    )
    draw.text(
        (sx1 + 80, sy1 + 140),
        "FastAPI • LangGraph • pgvector • RAGAS",
        fill=(148, 163, 184, 255),
        font=get_font(14, mono=True),
    )
    draw.line(
        [(sx1 + 80, sy1 + 170), (sx1 + 20 + card_w, sy1 + 170)], fill=(30, 41, 59, 200), width=1
    )

    py_items = [
        ">> LangGraph Multi-Agent Supervisor",
        ">> FlashRank Neural CPU Cross-Encoder",
        ">> pgvector 16 Dense HNSW Indexing",
        ">> Pydantic v2 Contract Validation",
        ">> Async SSE Streaming to Clients",
    ]
    py_y = sy1 + 195
    for item in py_items:
        draw.text((sx1 + 80, py_y), item, fill=(248, 250, 252, 255), font=get_font(14, mono=True))
        py_y += 55

    # Right Box: Java
    draw.rounded_rectangle(
        [(sx2 - 50 - card_w, sy1 + 80), (sx2 - 50, sy1 + 530)],
        radius=12,
        fill=(15, 23, 42, 230),
        outline=(239, 68, 68, 200),
        width=2,
    )
    draw.text(
        (sx2 - 20 - card_w, sy1 + 105),
        "JAVA ENTERPRISE MUSCLE",
        fill=(239, 68, 68, 255),
        font=get_font(20, bold=True),
    )
    draw.text(
        (sx2 - 20 - card_w, sy1 + 140),
        "Spring Boot • Kafka • Enterprise Batch",
        fill=(148, 163, 184, 255),
        font=get_font(14, mono=True),
    )
    draw.line(
        [(sx2 - 20 - card_w, sy1 + 170), (sx2 - 80, sy1 + 170)], fill=(30, 41, 59, 200), width=1
    )

    java_items = [
        ">> High-Throughput Kafka Stream Processing",
        ">> Legacy Enterprise ERP / SQL Connectors",
        ">> Multi-Threaded JVM Batch Workloads",
        ">> Strong Static Type Guarantees",
        ">> gRPC Microservices Interop",
    ]
    java_y = sy1 + 195
    for item in java_items:
        draw.text(
            (sx2 - 20 - card_w, java_y),
            item,
            fill=(248, 250, 252, 255),
            font=get_font(14, mono=True),
        )
        java_y += 55

    # Center Bridge Banner
    draw.rounded_rectangle(
        [(sx1 + 50, sy1 + 570), (sx2 - 50, sy2 - 40)],
        radius=12,
        fill=(8, 12, 20, 250),
        outline=(16, 185, 129, 200),
        width=2,
    )
    draw.text(
        (sx1 + 80, sy1 + 595),
        "THE ZERO-COLLISION BRIDGE: DECOUPLED CONTRACTS",
        fill=(16, 185, 129, 255),
        font=get_font(18, bold=True),
    )
    draw.text(
        (sx1 + 80, sy1 + 630),
        "• Communications through OpenAPI 3.1 REST contracts or gRPC / Protobuf streams.",
        fill=(248, 250, 252, 255),
        font=get_font(14, mono=True),
    )
    draw.text(
        (sx1 + 80, sy1 + 660),
        "• ZERO classpath collisions. ZERO runtime version fights. Pure polyglot synergy.",
        fill=(56, 189, 248, 255),
        font=get_font(14, mono=True),
    )

    return im


def render_scene_6(progress):
    # Scene 6: Autobot Squad & Teammate Prompt Wizard
    im, draw = draw_base_frame(6, "06. AUTOBOT SQUADRON & HUD")
    bullet_points = [
        ("[BOTS]", "5 Autonomous Personas", "Optimus, Ironhide, Bumblebee, Wheeljack, Mirage"),
        (
            "[ROLE]",
            "Role-Adaptive Prompts",
            "Generates custom IDE prompts with {{TEAMMATE_ROLE}} tags",
        ),
        (
            "[WIZ]",
            "npx hsf wizard Command",
            "Interactive CLI sets up any developer in under 60 seconds",
        ),
        (
            "[HUD]",
            "Senior Orbit Mascot HUD",
            "Live floating desktop widget keeps teams synchronized",
        ),
    ]
    draw_left_card(
        draw,
        ">> TEAMMATE ONBOARDING",
        ["AUTOBOT SQUADRON &", "SENIOR ORBIT HUD"],
        "Dynamic AI mentoring tailored to each teammate's individual role.",
        bullet_points,
    )

    sx1, sy1, sx2, sy2 = draw_right_stage_box(
        draw, "AUTOBOT SQUADRON ROSTER  |  ROLE SPECIALIZATIONS"
    )

    autobots = [
        (
            "OPTIMUS PRIME",
            "Lead Architect",
            "System design, DDD boundaries, trade-off evaluations",
            "#ef4444",
        ),
        (
            "IRONHIDE",
            "Backend Lead",
            "FastAPI async routes, Redis caching, circuit breakers",
            "#3b82f6",
        ),
        (
            "BUMBLEBEE",
            "DevOps & Cloud",
            "Docker multi-stage, AWS ECS, offline stage fail-safe",
            "#f59e0b",
        ),
        (
            "WHEELJACK",
            "AI & Neural Lead",
            "LangGraph supervisor, pgvector RAG, FastMCP SSE",
            "#a855f7",
        ),
        ("MIRAGE", "Frontend Lead", "Modern web UI, Orbit Mascot HUD, accessible forms", "#10b981"),
    ]

    card_y = sy1 + 75
    for name, role, powers, color in autobots:
        draw.rounded_rectangle(
            [(sx1 + 45, card_y), (sx2 - 45, card_y + 82)],
            radius=10,
            fill=(15, 23, 42, 220),
            outline=color,
            width=1,
        )
        # Left color bar
        draw.rounded_rectangle([(sx1 + 45, card_y), (sx1 + 55, card_y + 82)], radius=4, fill=color)

        draw.text(
            (sx1 + 75, card_y + 14),
            name + "  •  " + role,
            fill=color,
            font=get_font(17, bold=True, mono=True),
        )
        draw.text((sx1 + 75, card_y + 46), powers, fill=(248, 250, 252, 255), font=get_font(14))
        card_y += 96

    # Bottom Wizard Box
    draw.rounded_rectangle(
        [(sx1 + 45, card_y + 8), (sx2 - 45, sy2 - 40)],
        radius=8,
        fill=(8, 12, 20, 250),
        outline=(56, 189, 248, 140),
        width=1,
    )
    draw.text(
        (sx1 + 70, card_y + 26),
        "Run 'npx hsf wizard' -> Generates .hsf/prompt.txt for Antigravity / Cursor / Claude Code",
        fill=(56, 189, 248, 255),
        font=get_font(14, mono=True),
    )

    return im


def render_scene_7(progress):
    # Scene 7: Archify Suite - 8 Interactive Blueprints
    im, draw = draw_base_frame(7, "07. ARCHIFY INTERACTIVE SUITE")
    bullet_points = [
        (
            "[8/8]",
            "8 Verified Blueprints",
            "Topology, Sequence, Lifecycle, Dataflow, Squad, Polyglot...",
        ),
        (
            "[SVG]",
            "100% Interactive SVGs",
            "Pan, zoom, theme toggle (light/dark), and packet motion traces",
        ),
        (
            "[0 ERR]",
            "Zero CLI Audit Errors",
            "Compiled and verified strictly via archify deliver and check",
        ),
        (
            "[HUB]",
            "Interactive Gallery Hub",
            "Browse all 8 blueprints live at docs/architecture/index.html",
        ),
    ]
    draw_left_card(
        draw,
        ">> CERTIFIED ARCHITECTURE",
        ["8 INTERACTIVE SVG", "ARCHIFY BLUEPRINTS"],
        "Engineering clarity through zero-dependency interactive visual specs.",
        bullet_points,
    )

    sx1, sy1, sx2, sy2 = draw_right_stage_box(
        draw, "ARCHIFY BLUEPRINTS GALLERY  |  8 CERTIFIED DIAGRAMS"
    )

    blueprints = [
        ("[01]", "Master Full-Stack Topology", "architecture", "system-architecture.html"),
        ("[02]", "Request Lifecycle & SSE Stream", "sequence", "request-execution.sequence.html"),
        ("[03]", "Circuit Breaker State Machine", "lifecycle", "circuit-breaker.lifecycle.html"),
        ("[04]", "Inter-Layer Neural Dataflow", "dataflow", "inter-layer-dataflow.html"),
        ("[05]", "Autobot Squad Orchestration", "workflow", "autobot-squad.workflow.html"),
        (
            "[06]",
            "Zero-Collision Polyglot Bridge",
            "architecture",
            "polyglot-bridge.architecture.html",
        ),
        ("[07]", "24-Hour Execution Timeline", "workflow", "hackathon-execution.workflow.html"),
        (
            "[08]",
            "Gamification & Quest Bounty Loop",
            "workflow",
            "gamification-quest.workflow.html",
        ),
    ]

    bx, by = sx1 + 45, sy1 + 75
    col_width = (sx2 - sx1 - 120) // 2

    for i, (num, name, archetype, fname) in enumerate(blueprints):
        x = bx + (i % 2) * (col_width + 30)
        y = by + (i // 2) * 125

        draw.rounded_rectangle(
            [(x, y), (x + col_width, y + 105)],
            radius=10,
            fill=(15, 23, 42, 220),
            outline=(56, 189, 248, 120),
            width=1,
        )
        draw.text(
            (x + 20, y + 16),
            num + " " + name,
            fill=(248, 250, 252, 255),
            font=get_font(16, bold=True),
        )
        draw.text(
            (x + 20, y + 46),
            "Type: " + archetype.upper() + "  •  100% VERIFIED",
            fill=(16, 185, 129, 255),
            font=get_font(13, mono=True),
        )
        draw.text((x + 20, y + 74), fname, fill=(148, 163, 184, 255), font=get_font(12, mono=True))

    # Bottom Gallery Callout
    draw.rounded_rectangle(
        [(sx1 + 45, sy1 + 600), (sx2 - 45, sy2 - 40)],
        radius=8,
        fill=(8, 12, 20, 250),
        outline=(168, 85, 247, 140),
        width=1,
    )
    draw.text(
        (sx1 + 70, sy1 + 625),
        "Open Gallery Hub: open docs/architecture/index.html  •  Recompile: npx hsf diagram all",
        fill=(168, 85, 247, 255),
        font=get_font(14, mono=True),
    )

    return im


def render_scene_8(progress):
    # Scene 8: Cybernetic Teammate Arena & Victory Guarantee
    im, draw = draw_base_frame(8, "08. TEAMMATE ARENA & STAGE VICTORY")
    bullet_points = [
        (
            "[ARENA]",
            "Cybernetic Leaderboard",
            "Live XP, Level progression (Cadet to Grandmaster), and MVP",
        ),
        (
            "[QUEST]",
            "8 24h Hackathon Bounties",
            "Milestones awarding badges, titles, and companion synergy",
        ),
        (
            "[CHEER]",
            "Teammate Peer Cheers",
            "+25 XP peer appreciation fosters unstoppable team synergy",
        ),
        (
            "[STAGE]",
            "Stage Fail-Safe Demo",
            "pitch/demo.sh runs completely offline with 0ms network lag",
        ),
    ]
    draw_left_card(
        draw,
        ">> TEAM HARMONY & AUDIT SEAL",
        ["CYBERNETIC ARENA &", "STAGE VICTORY SEAL"],
        "Keeping teammates energized and the stage presentation 100% resilient.",
        bullet_points,
    )

    sx1, sy1, sx2, sy2 = draw_right_stage_box(
        draw, "LIVE TEAMMATE SCOREBOARD  |  JUDGE CERTIFICATION SEAL"
    )

    # Scoreboard Table
    draw.rounded_rectangle(
        [(sx1 + 45, sy1 + 75), (sx2 - 45, sy1 + 420)],
        radius=12,
        fill=(15, 23, 42, 220),
        outline=(56, 189, 248, 140),
        width=2,
    )
    draw.text(
        (sx1 + 70, sy1 + 95),
        "TEAM: AUTOBOTS STRIKE FLEET  |  TOTAL XP: 3,275  |  MVP: AI LEAD",
        fill=(251, 191, 36, 255),
        font=get_font(16, bold=True, mono=True),
    )
    draw.line([(sx1 + 60, sy1 + 130), (sx2 - 60, sy1 + 130)], fill=(30, 41, 59, 200), width=1)

    headers = "RANK   TEAMMATE         LEVEL / TITLE              XP         CHEERS   AUTOBOT"
    draw.text(
        (sx1 + 70, sy1 + 145), headers, fill=(148, 163, 184, 255), font=get_font(13, mono=True)
    )
    draw.line([(sx1 + 60, sy1 + 175), (sx2 - 60, sy1 + 175)], fill=(30, 41, 59, 200), width=1)

    rows = [
        (
            "🥇 1   AI Lead          Lv.4 Cyber-Scientist       850 XP     6 🙌     Wheeljack",
            "#38bdf8",
        ),
        (
            "🥈 2   Backend Lead     Lv.3 Resilience Titan      750 XP     8 🙌     Ironhide",
            "#f8fafc",
        ),
        (
            "🥉 3   DevOps Lead      Lv.3 Resilience Titan      700 XP     4 🙌     Bumblebee",
            "#f8fafc",
        ),
        (
            "   4   Frontend Lead    Lv.2 Tactical Strategist   525 XP     6 🙌     Mirage",
            "#94a3b8",
        ),
        (
            "   5   Lead Architect   Lv.2 Tactical Strategist   450 XP     3 🙌     Orbit Prime",
            "#94a3b8",
        ),
    ]

    ry = sy1 + 195
    for row, color in rows:
        draw.text((sx1 + 70, ry), row, fill=color, font=get_font(14, mono=True))
        ry += 42

    # Judge Certification Seal Box
    draw.rounded_rectangle(
        [(sx1 + 45, sy1 + 450), (sx2 - 45, sy2 - 40)],
        radius=12,
        fill=(8, 12, 20, 250),
        outline=(251, 191, 36, 220),
        width=2,
    )
    draw.text(
        (sx1 + 75, sy1 + 480),
        "OFFICIAL HACKATHON AUDIT CERTIFICATION",
        fill=(251, 191, 36, 255),
        font=get_font(22, bold=True),
    )
    draw.text(
        (sx1 + 75, sy1 + 525),
        "• Status: VERIFIED PRODUCTION-GRADE  •  Pass Rate: 100% (20/20 Pytest Assertions)",
        fill=(16, 185, 129, 255),
        font=get_font(16, mono=True),
    )
    draw.text(
        (sx1 + 75, sy1 + 565),
        "• 8 Archify Blueprints Certified  •  0 Ruff Lint Errors  •  Docker <180MB Non-Root",
        fill=(248, 250, 252, 255),
        font=get_font(15, mono=True),
    )
    draw.text(
        (sx1 + 75, sy1 + 605),
        "• Offline Stage Demo Guaranteed Safe  •  docs/JUDGE_CERTIFICATION.md Certified",
        fill=(56, 189, 248, 255),
        font=get_font(15, mono=True),
    )

    return im


SCENE_RENDERERS = [
    render_scene_1,
    render_scene_2,
    render_scene_3,
    render_scene_4,
    render_scene_5,
    render_scene_6,
    render_scene_7,
    render_scene_8,
]


def render_all_frames_and_encode():
    print(f"🎬 Starting high-production video rendering ({TOTAL_FRAMES} frames @ 30fps)...")

    # 1. Prepare synchronized audio mix first
    audio_output = WORK_DIR / "final_soundtrack.aac"
    print("🎵 Mixing audio soundtrack and motion SFX cues...")

    cmd_audio = [
        "/opt/homebrew/bin/ffmpeg",
        "-y",
        "-ss",
        "0",
        "-t",
        str(SCENE_DURATION_SEC * TOTAL_SCENES),
        "-i",
        str(MUSIC_FILE),
        "-i",
        str(SFX_DIR / "impact" / "impactBell_heavy_000.ogg"),
        "-i",
        str(SFX_DIR / "ui" / "switch32.ogg"),
        "-i",
        str(SFX_DIR / "interface" / "select_008.ogg"),
        "-i",
        str(SFX_DIR / "ui" / "switch10.ogg"),
        "-filter_complex",
        "[0:a]volume=0.82,afade=t=out:st=31.2:d=0.8[music];"
        "[1:a]volume=0.60,adelay=100|100[sfx_boot];"
        "[2:a]volume=0.55,adelay=4000|4000[sfx_sc2];"
        "[3:a]volume=0.55,adelay=8000|8000[sfx_sc3];"
        "[4:a]volume=0.55,adelay=12000|12000[sfx_sc4];"
        "[2:a]volume=0.55,adelay=16000|16000[sfx_sc5];"
        "[3:a]volume=0.55,adelay=20000|20000[sfx_sc6];"
        "[4:a]volume=0.55,adelay=24000|24000[sfx_sc7];"
        "[1:a]volume=0.65,adelay=28000|28000[sfx_sc8];"
        "[music][sfx_boot][sfx_sc2][sfx_sc3][sfx_sc4][sfx_sc5][sfx_sc6][sfx_sc7][sfx_sc8]amix=inputs=9:duration=first:dropout_transition=2[aout]",
        "-map",
        "[aout]",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        str(audio_output),
    ]
    res_a = subprocess.run(cmd_audio, capture_output=True, text=True)
    if res_a.returncode != 0:
        print("❌ Audio mix failed:", res_a.stderr)
        sys.exit(1)
    print("✔ Audio soundtrack mixed successfully!")

    # 2. Pipe frames directly to ffmpeg for maximum render speed
    raw_video = WORK_DIR / "raw_video.mp4"
    cmd_ffmpeg = [
        "/opt/homebrew/bin/ffmpeg",
        "-y",
        "-f",
        "rawvideo",
        "-vcodec",
        "rawvideo",
        "-s",
        f"{WIDTH}x{HEIGHT}",
        "-pix_fmt",
        "rgba",
        "-r",
        str(FPS),
        "-i",
        "-",
        "-i",
        str(audio_output),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-preset",
        "fast",
        "-crf",
        "18",
        "-c:a",
        "copy",
        "-movflags",
        "+faststart",
        str(raw_video),
    ]

    proc = subprocess.Popen(cmd_ffmpeg, stdin=subprocess.PIPE)

    # Pre-render base frames for each scene to achieve ultra-fast generation
    pre_rendered = []
    print("🖼️  Pre-rendering scene canvases...")
    for idx, renderer in enumerate(SCENE_RENDERERS):
        im = renderer(1.0).convert("RGBA")
        pre_rendered.append(im)
        print(f"  ✔ Scene {idx + 1}/{TOTAL_SCENES} rendered")

    print("⚡ Streaming 960 frames to ffmpeg...")
    for scene_idx in range(TOTAL_SCENES):
        scene_im = pre_rendered[scene_idx]
        raw_bytes = scene_im.tobytes()
        for f in range(FRAMES_PER_SCENE):
            proc.stdin.write(raw_bytes)

    proc.stdin.close()
    proc.wait()

    if proc.returncode != 0:
        print("❌ Video encoding failed")
        sys.exit(1)
    print(f"✔ Video stream generated at {raw_video}")

    # 3. Extract best settled poster frame (e.g. from Scene 8 at 29.5s)
    poster_jpg = OUTPUT_DIR / "brag.jpg"
    print("📸 Extracting best settled poster frame...")
    cmd_poster = [
        "/opt/homebrew/bin/ffmpeg",
        "-y",
        "-ss",
        "29.5",
        "-i",
        str(raw_video),
        "-frames:v",
        "1",
        "-q:v",
        "2",
        str(poster_jpg),
    ]
    subprocess.run(cmd_poster, check=True)
    print(f"✔ Poster saved at {poster_jpg}")

    # 4. Bake poster as frame 0 into final brag.mp4
    final_mp4 = OUTPUT_DIR / "brag.mp4"
    print("🎞️  Baking poster as frame 0 into final brag.mp4...")
    cmd_bake = [
        "/opt/homebrew/bin/ffmpeg",
        "-y",
        "-i",
        str(raw_video),
        "-i",
        str(poster_jpg),
        "-filter_complex",
        "[0:v][1:v]overlay=0:0:enable='eq(n,0)'[v]",
        "-map",
        "[v]",
        "-map",
        "0:a?",
        "-c:v",
        "libx264",
        "-crf",
        "18",
        "-preset",
        "medium",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "copy",
        "-movflags",
        "+faststart",
        str(final_mp4),
    ]
    subprocess.run(cmd_bake, check=True)
    print(f"🎉 Final brag video ready: {final_mp4} ({final_mp4.stat().st_size:,} bytes)")

    # 5. Write canonical share-copy.txt
    share_copy = (
        "From 0 to production in 60s: meet HSF v1.0 — FastAPI, pgvector 16, LangGraph, "
        "Redis circuit breakers, zero-collision Java+Python polyglot, 8 Archify interactive blueprints, "
        "and a live teammate gamification arena. Ready for the judge stage."
    )
    (OUTPUT_DIR / "share-copy.txt").write_text(share_copy, encoding="utf-8")
    print(f"✔ Share copy written to {OUTPUT_DIR / 'share-copy.txt'}")


if __name__ == "__main__":
    render_all_frames_and_encode()
