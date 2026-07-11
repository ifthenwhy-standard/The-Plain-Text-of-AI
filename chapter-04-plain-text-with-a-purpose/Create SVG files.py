import os
import math

os.makedirs("output", exist_ok=True)

svg_width = 3300
svg_height = 3600  # Canvas height scaled to cleanly map all three pipelines

svg_content = []
svg_content.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="100%" height="100%">')
svg_content.append('<rect width="100%" height="100%" fill="#FFFFFF"/>')

svg_content.append('''
<style>
    .title { font-family: "Segoe UI", Arial, sans-serif; font-size: 64px; font-weight: bold; fill: #1E293B; text-anchor: middle; }
    .node-text { font-family: "Segoe UI", Arial, sans-serif; font-size: 36px; fill: #1E293B; text-anchor: middle; dominant-baseline: middle; }
    .label-text { font-family: "Segoe UI", Arial, sans-serif; font-size: 32px; fill: #64748B; text-anchor: middle; dominant-baseline: middle; }
    .label-pass { font-family: "Segoe UI", Arial, sans-serif; font-size: 32px; font-weight: bold; fill: #10B981; text-anchor: left; dominant-baseline: middle; }
    .label-stop { font-family: "Segoe UI", Arial, sans-serif; font-size: 32px; font-weight: bold; fill: #EF4444; text-anchor: middle; dominant-baseline: middle; }
    .stop-sign-text { font-family: "Segoe UI", Arial, sans-serif; font-size: 30px; font-weight: bold; fill: #FFFFFF; text-anchor: middle; dominant-baseline: middle; }
</style>
''')

svg_content.append('<defs>')
svg_content.append('  <marker id="arrow-gray" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">')
svg_content.append('    <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#64748B"/>')
svg_content.append('  </marker>')
svg_content.append('  <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">')
svg_content.append('    <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#10B981"/>')
svg_content.append('  </marker>')
svg_content.append('  <marker id="arrow-red" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">')
svg_content.append('    <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#EF4444"/>')
svg_content.append('  </marker>')
svg_content.append('</defs>')

def make_node(text, cx, cy, w, h, rx, bg, border, text_color):
    x = cx - w / 2
    y = cy - h / 2
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{bg}" stroke="{border}" stroke-width="4"/><text x="{cx}" y="{cy}" class="node-text" fill="{text_color}">{text}</text>'

def make_arrow_down(x, y_start, y_end, color="#64748B", marker="url(#arrow-gray)"):
    return f'<line x1="{x}" y1="{y_start}" x2="{x}" y2="{y_end}" stroke="{color}" stroke-width="6" marker-end="{marker}"/>'

def make_arrow_right(x_start, x_end, y, color="#64748B", marker="url(#arrow-gray)"):
    return f'<line x1="{x_start}" y1="{y}" x2="{x_end}" y2="{y}" stroke="{color}" stroke-width="6" marker-end="{marker}"/>'

def make_elbow_right_down(x_start, x_end, y_start, y_end, color="#64748B", marker="url(#arrow-gray)"):
    return f'<path d="M {x_start} {y_start} L {x_end} {y_start} L {x_end} {y_end}" fill="none" stroke="{color}" stroke-width="6" marker-end="{marker}"/>'

def make_elbow_down_left_down(x_start, y_start, x_mid, y_mid, x_end, y_end, color="#64748B", marker="url(#arrow-gray)"):
    return f'<path d="M {x_start} {y_start} L {x_start} {y_mid} L {x_mid} {y_mid} L {x_mid} {y_end}" fill="none" stroke="{color}" stroke-width="6" marker-end="{marker}"/>'

def make_checkmark(cx, cy, radius=35):
    elements = []
    elements.append(f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="#10B981"/>')
    elements.append(f'<path d="M {cx - radius + 14} {cy} L {cx - 6} {cy + 14} L {cx + radius - 14} {cy - 12}" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')
    return "\n".join(elements)

def make_stopsign(cx, cy, radius=45):
    points = []
    for i in range(8):
        angle = math.radians(i * 45 + 22.5)
        px = cx + radius * math.cos(angle)
        py = cy + radius * math.sin(angle)
        points.append(f"{px},{py}")
    points_str = " ".join(points)
    return f'<polygon points="{points_str}" fill="#EF4444"/><text x="{cx}" y="{cy}" class="stop-sign-text">STOP</text>'

# ----------------------------------------------------
# PIPELINE 1: LIVE INTERCEPTION PIPELINE
# ----------------------------------------------------
svg_content.append('<text x="1650" y="150" class="title">1. The Live Interception Pipeline (Real-Time Gatekeeper)</text>')

c_x = 900
n_w, n_h = 600, 110

r1_y = 300
svg_content.append(make_node("[AI Agent Action / Output]", c_x, r1_y, n_w, n_h, 15, "#F8FAFC", "#94A3B8", "#1E293B"))
svg_content.append(make_arrow_down(c_x, r1_y + n_h / 2, r1_y + 130, color="#64748B", marker="url(#arrow-gray)"))

r2_y = r1_y + 135 + n_h / 2
svg_content.append(make_node("[BERT Semantic Gatekeeper]", c_x, r2_y, n_w, n_h, 15, "#EFF6FF", "#3B82F6", "#1E293B"))

# Path A: BERT If Pass (Green Line Routing)
svg_content.append(make_elbow_right_down(c_x + n_w / 2, c_x + 850, r2_y, r2_y + 180, color="#10B981", marker="url(#arrow-green)"))
svg_content.append(make_checkmark(c_x + n_w / 2 + 100, r2_y - 55, 35))
svg_content.append(f'<text x="{c_x + n_w / 2 + 155}" y="{r2_y - 55}" class="label-pass">If Pass</text>')

# Row 3: Logic Map Files Evaluation
r3_y = r2_y + 185 + n_h / 2
svg_content.append(make_node("[Evaluate Against Logic Map Files]", c_x + 850, r3_y, 850, n_h, 15, "#F5F3FF", "#8B5CF6", "#1E293B"))

# Sub-path A: Logic Map Files If Pass (Green Line &amp; Offset)
pass_arrow_x = c_x + 650
svg_content.append(make_arrow_down(pass_arrow_x, r3_y + n_h / 2, r3_y + 150, color="#10B981", marker="url(#arrow-green)"))
svg_content.append(make_checkmark(pass_arrow_x + 80, r3_y + n_h / 2 + 65, 30))
svg_content.append(f'<text x="{pass_arrow_x + 130}" y="{r3_y + n_h / 2 + 65}" class="label-pass">If Pass</text>')

# Row 4 Success: Execute Deterministic Action
r4_y = r3_y + 155 + n_h / 2
svg_content.append(make_node("[Execute Deterministic Action]", c_x + 700, r4_y, 680, n_h, 15, "#ECFDF5", "#10B981", "#065F46"))

# Sub-path B: Logic Map Files If Fail (Red Line Routing)
r4_fail_y = r4_y + 350
svg_content.append(make_elbow_down_left_down(c_x + 850 + 425, r3_y + n_h / 2, c_x, r4_y + 160, c_x, r4_fail_y - n_h / 2, color="#EF4444", marker="url(#arrow-red)"))
svg_content.append(make_stopsign(c_x + 850 + 540, r3_y + 130, 45))
svg_content.append(f'<text x="{c_x + 850 + 700}" y="{r3_y + 130}" class="label-stop">If Fail (Stop)</text>')

# Path B: BERT If Fail (Red Line Routing)
svg_content.append(make_arrow_down(c_x, r2_y + n_h / 2, r4_fail_y - n_h / 2, color="#EF4444", marker="url(#arrow-red)"))
svg_content.append(make_stopsign(c_x - 110, r2_y + 220, 45))
svg_content.append(f'<text x="{c_x - 280}" y="{r2_y + 220}" class="label-stop">If Fail (Stop)</text>')

# Row 5: Lowered Anomaly Log and Halt Nodes
svg_content.append(make_node("[Write to BERT Anomaly Log]", c_x, r4_fail_y, 600, n_h, 15, "#FEF2F2", "#EF4444", "#991B1B"))
svg_content.append(make_arrow_right(c_x + n_w / 2, c_x + n_w / 2 + 250, r4_fail_y, color="#64748B", marker="url(#arrow-gray)"))

svg_content.append(make_node("[Halt &amp; Notify User]", c_x + n_w / 2 + 550, r4_fail_y, 600, n_h, 15, "#FFF7ED", "#F97316", "#9A3412"))

svg_content.append('<line x1="150" y1="1380" x2="3150" y2="1380" stroke="#E2E8F0" stroke-width="8"/>')

# ----------------------------------------------------
# PIPELINE 2: CONTINUOUS ANOMALY AUDITING LAYER
# ----------------------------------------------------
svg_content.append('<text x="1650" y="1480" class="title">2. The Continuous Anomaly Auditing Layer</text>')

c_x2 = 1650
start_y2 = 1600

svg_content.append(make_node("[BERT Anomaly Log]", c_x2, start_y2, 750, n_h, 15, "#FEF2F2", "#EF4444", "#991B1B"))
svg_content.append(make_arrow_down(c_x2, start_y2 + n_h / 2, start_y2 + 120, color="#64748B", marker="url(#arrow-gray)"))

r2_y2 = start_y2 + 125 + n_h / 2
svg_content.append(make_node("[Scan BERT Anomaly Log for Co-Occurrence]", c_x2, r2_y2, 850, n_h, 15, "#F8FAFC", "#475569", "#1E293B"))
svg_content.append(make_arrow_down(c_x2, r2_y2 + n_h / 2, r2_y2 + 120, color="#64748B", marker="url(#arrow-gray)"))

r3_y2 = r2_y2 + 125 + n_h / 2
svg_content.append(make_node("[Calculate Frequency &amp; Recurrence Trends]", c_x2, r3_y2, 850, n_h, 15, "#F0FDFA", "#14B8A6", "#115E59"))
svg_content.append(make_arrow_down(c_x2, r3_y2 + n_h / 2, r3_y2 + 120, color="#64748B", marker="url(#arrow-gray)"))

r4_y2 = r3_y2 + 125 + n_h / 2
svg_content.append(make_node("[Route Prioritized Dashboard to Human-in-the-Loop]", c_x2, r4_y2, 1000, n_h, 15, "#FFFBEB", "#F59E0B", "#92400E"))

svg_content.append('<line x1="150" y1="2300" x2="3150" y2="2300" stroke="#E2E8F0" stroke-width="8"/>')

# ----------------------------------------------------
# PIPELINE 3: REAL-TIME ADAPTIVE GLOBAL LANDSCAPE AUDITING
# ----------------------------------------------------
svg_content.append('<text x="1650" y="2400" class="title">3. Real-Time Adaptive Global Landscape Auditing</text>')

start_y3 = 2520

# Box 1: Macro Environmental Scan Source
svg_content.append(make_node("[Global Environment Scan: Regulations, News, Legal Precedents &amp; Market Shifts]", c_x2, start_y3, 1600, n_h, 15, "#FFF1F2", "#F43F5E", "#881337"))
svg_content.append(make_arrow_down(c_x2, start_y3 + n_h / 2, start_y3 + 120, color="#64748B", marker="url(#arrow-gray)"))

# Box 2: Ingestion &amp; Structuring
r2_y3 = start_y3 + 125 + n_h / 2
svg_content.append(make_node("[Real-Time Policy Ingestion &amp; Signal Processing]", c_x2, r2_y3, 900, n_h, 15, "#F0FDF4", "#16A34A", "#14532D"))
svg_content.append(make_arrow_down(c_x2, r2_y3 + n_h / 2, r2_y3 + 120, color="#64748B", marker="url(#arrow-gray)"))

# Box 3: AI Impact Evaluation Engine
r3_y3 = r2_y3 + 125 + n_h / 2
svg_content.append(make_node("[AI Impact Engine: Evaluate Mismatches Against Current Logic Baseline]", c_x2, r3_y3, 1250, n_h, 15, "#EFF6FF", "#3B82F6", "#1E293B"))
svg_content.append(make_arrow_down(c_x2, r3_y3 + n_h / 2, r3_y3 + 120, color="#64748B", marker="url(#arrow-gray)"))

# Box 4: Execution / Adaptive Shift (UPDATED TEXT &amp; EXPANDED BOX WIDTH)
r4_y3 = r3_y3 + 125 + n_h / 2
svg_content.append(make_node("[Autonomous Baseline Adaptation: Audit &amp; Instantly Update Master Logic Map Files Without Code Deploy]", c_x2, r4_y3, 1750, n_h, 15, "#F5F3FF", "#8B5CF6", "#4C1D95"))

svg_content.append('</svg>')

with open("output/pipeline_architecture.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg_content))