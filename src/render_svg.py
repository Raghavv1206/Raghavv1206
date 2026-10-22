# src/render_svg.py
import re

PIECES_DARK = """
    <!-- Piece Definitions Dark -->
    <g id="w-P">
      <circle cx="20" cy="14" r="5" fill="#e0e7ff" fill-opacity="0.94" stroke="#be5bf6" stroke-width="1.35" stroke-linejoin="round"/>
      <path d="M13 20h14l-2 8 7 10h-24l7-10z" fill="#e0e7ff" fill-opacity="0.94" stroke="#be5bf6" stroke-width="1.35" stroke-linejoin="round"/>
      <path d="M8 39h24" fill="none" stroke="#be5bf6" stroke-width="1.35" stroke-linejoin="round"/>
    </g>
    <g id="w-R">
      <path d="M8 10h5v5h4v-5h5v5h4v-5h5v10h-4v15h4v5h-28v-5h4v-15h-4z" fill="#e0e7ff" fill-opacity="0.94" stroke="#be5bf6" stroke-width="1.35" stroke-linejoin="round"/>
    </g>
    <g id="w-N">
      <path d="M10 30h24l-3-6h-7l6-8c3-4 1-13-6-17l-4 5-6-4-3 5 5 7-5 8z" fill="#e0e7ff" fill-opacity="0.94" stroke="#be5bf6" stroke-width="1.35" stroke-linejoin="round"/>
      <path d="M17 3l8 4" fill="none" stroke="#be5bf6" stroke-width="1.35" stroke-linejoin="round"/>
    </g>
    <g id="w-B">
      <path d="M20 7a5 5 0 1 1 0 10a8 8 0 0 0-5 8l-7 8h24l-7-8a8 8 0 0 0-5-8a5 5 0 0 1 0-10z" fill="#e0e7ff" fill-opacity="0.94" stroke="#be5bf6" stroke-width="1.35" stroke-linejoin="round"/>
      <path d="M8 33h24" fill="none" stroke="#be5bf6" stroke-width="1.35" stroke-linejoin="round"/>
    </g>
    <g id="w-Q">
      <path d="M8 15l3-11 6 6 3-9 3 9 6-6 3 11-3 13h-18z" fill="#e0e7ff" fill-opacity="0.94" stroke="#be5bf6" stroke-width="1.35" stroke-linejoin="round"/>
      <path d="M7 30h26l2 5h-30z" fill="#e0e7ff" fill-opacity="0.94" stroke="#be5bf6" stroke-width="1.35" stroke-linejoin="round"/>
    </g>
    <g id="w-K">
      <path d="M18 5h4v5h5v4h-5v4h7l3 10h-24l3-10h7v-4h-5v-4h5z" fill="#e0e7ff" fill-opacity="0.94" stroke="#be5bf6" stroke-width="1.35" stroke-linejoin="round"/>
    </g>
    
    <g id="b-P">
      <circle cx="20" cy="14" r="5" fill="#93a5f6" fill-opacity="0.94" stroke="#a5b4fc" stroke-width="1.35" stroke-linejoin="round"/>
      <path d="M13 20h14l-2 8 7 10h-24l7-10z" fill="#93a5f6" fill-opacity="0.94" stroke="#a5b4fc" stroke-width="1.35" stroke-linejoin="round"/>
      <path d="M8 39h24" fill="none" stroke="#a5b4fc" stroke-width="1.35" stroke-linejoin="round"/>
    </g>
    <g id="b-R">
      <path d="M8 10h5v5h4v-5h5v5h4v-5h5v10h-4v15h4v5h-28v-5h4v-15h-4z" fill="#93a5f6" fill-opacity="0.94" stroke="#a5b4fc" stroke-width="1.35" stroke-linejoin="round"/>
    </g>
    <g id="b-N">
      <path d="M10 30h24l-3-6h-7l6-8c3-4 1-13-6-17l-4 5-6-4-3 5 5 7-5 8z" fill="#93a5f6" fill-opacity="0.94" stroke="#a5b4fc" stroke-width="1.35" stroke-linejoin="round"/>
      <path d="M17 3l8 4" fill="none" stroke="#a5b4fc" stroke-width="1.35" stroke-linejoin="round"/>
    </g>
    <g id="b-B">
      <path d="M20 7a5 5 0 1 1 0 10a8 8 0 0 0-5 8l-7 8h24l-7-8a8 8 0 0 0-5-8a5 5 0 0 1 0-10z" fill="#93a5f6" fill-opacity="0.94" stroke="#a5b4fc" stroke-width="1.35" stroke-linejoin="round"/>
      <path d="M8 33h24" fill="none" stroke="#a5b4fc" stroke-width="1.35" stroke-linejoin="round"/>
    </g>
    <g id="b-Q">
      <path d="M8 15l3-11 6 6 3-9 3 9 6-6 3 11-3 13h-18z" fill="#93a5f6" fill-opacity="0.94" stroke="#a5b4fc" stroke-width="1.35" stroke-linejoin="round"/>
      <path d="M7 30h26l2 5h-30z" fill="#93a5f6" fill-opacity="0.94" stroke="#a5b4fc" stroke-width="1.35" stroke-linejoin="round"/>
    </g>
    <g id="b-K">
      <path d="M18 5h4v5h5v4h-5v4h7l3 10h-24l3-10h7v-4h-5v-4h5z" fill="#93a5f6" fill-opacity="0.94" stroke="#a5b4fc" stroke-width="1.35" stroke-linejoin="round"/>
    </g>
"""

def generate_midnight_svg(board, last_move=None):
    # Determine board list 8x8 (row 0 is rank 8, row 7 is rank 1)
    lines = str(board).split('\\n') if '\\n' in str(board) else str(board).split('\n')
    board_grid = [line.strip().split() for line in lines if line.strip()]

    # Highlight squares from last_move (e.g. 'e2e4')
    hl_squares = []
    if last_move and len(last_move) >= 4:
        src_col = ord(last_move[0].lower()) - ord('a')
        src_row = int(last_move[1]) - 1
        dst_col = ord(last_move[2].lower()) - ord('a')
        dst_row = int(last_move[3]) - 1
        hl_squares.append((src_col, src_row))
        hl_squares.append((dst_col, dst_row))

    # Build squares SVG
    squares_svg = []
    for r in range(8):  # r=0 is rank 8, r=7 is rank 1
        rank = 8 - r
        row_idx = rank - 1
        y = 24 + r * 40
        for c in range(8):
            col_idx = c
            x = 40 + c * 40
            is_light = (c + r) % 2 == 0
            tile_fill = "#1a2748" if is_light else "#061246"
            
            # Check if highlighted
            if (col_idx, row_idx) in hl_squares:
                tile_fill = "#2e1065" if not is_light else "#3b0764"
                squares_svg.append(f'<rect x="{x}" y="{y}" width="40" height="40" fill="{tile_fill}" stroke="#c084fc" stroke-width="1.5"/>')
            else:
                squares_svg.append(f'<rect x="{x}" y="{y}" width="40" height="40" fill="{tile_fill}"/>')

    squares_content = "".join(squares_svg)

    # Build pieces SVG
    pieces_svg = []
    symbol_to_id = {
        'P': 'w-P', 'R': 'w-R', 'N': 'w-N', 'B': 'w-B', 'Q': 'w-Q', 'K': 'w-K',
        'p': 'b-P', 'r': 'b-R', 'n': 'b-N', 'b': 'b-B', 'q': 'b-Q', 'k': 'b-K',
    }

    for r in range(8):
        y = 24 + r * 40
        for c in range(8):
            x = 40 + c * 40
            sym = board_grid[r][c]
            if sym in symbol_to_id:
                piece_id = symbol_to_id[sym]
                pieces_svg.append(f'<use href="#{piece_id}" x="{x}" y="{y}"/>')

    pieces_content = "".join(pieces_svg)

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="400" height="380" viewBox="0 0 400 380" role="img" aria-label="Raghav Mishra Midnight Chess Board">
  <defs>
    <linearGradient id="gs-chess-raghavv1206-midnight-dark-bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="54%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#020617"/>
    </linearGradient>
    
    <radialGradient id="gs-chess-raghavv1206-midnight-dark-orb-0" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#818cf8" stop-opacity="0.72"/>
      <stop offset="58%" stop-color="#818cf8" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#818cf8" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="gs-chess-raghavv1206-midnight-dark-orb-1" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#be5bf6" stop-opacity="0.5"/>
      <stop offset="58%" stop-color="#be5bf6" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#be5bf6" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="gs-chess-raghavv1206-midnight-dark-orb-2" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#5beaf6" stop-opacity="0.72"/>
      <stop offset="58%" stop-color="#5beaf6" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#5beaf6" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="gs-chess-raghavv1206-midnight-dark-orb-3" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#f6665b" stop-opacity="0.5"/>
      <stop offset="58%" stop-color="#f6665b" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#f6665b" stop-opacity="0"/>
    </radialGradient>
    {PIECES_DARK}
  </defs>
  <style>
    #gs-chess-raghavv1206-midnight-dark .aura-orb-a {{ animation: float-a 9s ease-in-out infinite; }}
    #gs-chess-raghavv1206-midnight-dark .aura-orb-b {{ animation: float-b 11s ease-in-out infinite 1.1s; }}
    #gs-chess-raghavv1206-midnight-dark .aura-orb-c {{ animation: float-c 13s ease-in-out infinite 0.6s; }}
    @keyframes float-a {{ 0%,100% {{ transform: translate(0,0); opacity: .58; }} 50% {{ transform: translate(28px,-20px); opacity: .86; }} }}
    @keyframes float-b {{ 0%,100% {{ transform: translate(0,0); opacity: .42; }} 50% {{ transform: translate(-24px,18px); opacity: .72; }} }}
    @keyframes float-c {{ 0%,100% {{ transform: translate(0,0) scale(1); opacity: .34; }} 50% {{ transform: translate(18px,-12px) scale(1.18); opacity: .62; }} }}
  </style>
  <g id="gs-chess-raghavv1206-midnight-dark">
    <rect width="400" height="380" rx="20" fill="url(#gs-chess-raghavv1206-midnight-dark-bg)"/>
    
    <ellipse class="aura-orb-a" cx="64" cy="68" rx="96" ry="175" fill="url(#gs-chess-raghavv1206-midnight-dark-orb-0)"/>
    <ellipse class="aura-orb-b" cx="304" cy="84" rx="112" ry="160" fill="url(#gs-chess-raghavv1206-midnight-dark-orb-1)"/>
    <ellipse class="aura-orb-c" cx="232" cy="334" rx="144" ry="129" fill="url(#gs-chess-raghavv1206-midnight-dark-orb-2)"/>
    <ellipse class="aura-orb-b" cx="384" cy="296" rx="80" ry="160" fill="url(#gs-chess-raghavv1206-midnight-dark-orb-3)"/>
    <rect x="18" y="16" width="364" height="348" rx="24" fill="#0f172a" fill-opacity="0.8" stroke="#818cf8"/>
    <rect x="32" y="16" width="336" height="336" rx="16" fill="#020617" fill-opacity="0.52" stroke="#7884f7" stroke-opacity="0.38" stroke-width="2"/>
    <g>{squares_content}</g>
    <g opacity="0.85">
      <text x="60" y="359" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" text-anchor="middle" font-size="9.5" font-weight="800" fill="#a5b4fc">a</text>
      <text x="100" y="359" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" text-anchor="middle" font-size="9.5" font-weight="800" fill="#a5b4fc">b</text>
      <text x="140" y="359" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" text-anchor="middle" font-size="9.5" font-weight="800" fill="#a5b4fc">c</text>
      <text x="180" y="359" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" text-anchor="middle" font-size="9.5" font-weight="800" fill="#a5b4fc">d</text>
      <text x="220" y="359" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" text-anchor="middle" font-size="9.5" font-weight="800" fill="#a5b4fc">e</text>
      <text x="260" y="359" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" text-anchor="middle" font-size="9.5" font-weight="800" fill="#a5b4fc">f</text>
      <text x="300" y="359" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" text-anchor="middle" font-size="9.5" font-weight="800" fill="#a5b4fc">g</text>
      <text x="340" y="359" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" text-anchor="middle" font-size="9.5" font-weight="800" fill="#a5b4fc">h</text>
      <text x="27" y="44" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" text-anchor="middle" font-size="9.5" font-weight="800" fill="#a5b4fc">8</text>
      <text x="27" y="84" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" text-anchor="middle" font-size="9.5" font-weight="800" fill="#a5b4fc">7</text>
      <text x="27" y="124" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" text-anchor="middle" font-size="9.5" font-weight="800" fill="#a5b4fc">6</text>
      <text x="27" y="164" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" text-anchor="middle" font-size="9.5" font-weight="800" fill="#a5b4fc">5</text>
      <text x="27" y="204" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" text-anchor="middle" font-size="9.5" font-weight="800" fill="#a5b4fc">4</text>
      <text x="27" y="244" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" text-anchor="middle" font-size="9.5" font-weight="800" fill="#a5b4fc">3</text>
      <text x="27" y="284" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" text-anchor="middle" font-size="9.5" font-weight="800" fill="#a5b4fc">2</text>
      <text x="27" y="324" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" text-anchor="middle" font-size="9.5" font-weight="800" fill="#a5b4fc">1</text>
    </g>
    <g>{pieces_content}</g>
    <circle cx="350" cy="340" r="5" fill="#7884f7">
      <animate attributeName="opacity" values="1;.28;1" dur="1.6s" repeatCount="indefinite"/>
    </circle>
    <rect x="0.5" y="0.5" width="399" height="379" rx="19.5" fill="none" stroke="#818cf8" stroke-opacity="0.62"/>
  </g>
</svg>"""
    return svg
