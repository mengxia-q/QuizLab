"""
save_figures.py
Saves all auto-generated report figures as PNG files into a 'figures/' folder.
Run: python3 save_figures.py
"""

import io
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(OUT_DIR, exist_ok=True)


def save(buf, filename):
    path = os.path.join(OUT_DIR, filename)
    with open(path, "wb") as f:
        f.write(buf.read())
    print(f"  Saved: figures/{filename}")


# ── Figure 2: System Architecture ─────────────────────────────────────────────
def fig_system_architecture():
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis("off")

    ax.add_patch(FancyBboxPatch((3.5, 6.0), 3.0, 0.7, boxstyle="round,pad=0.05",
                                facecolor="#D5F5E3", edgecolor="#27AE60", lw=1.5))
    ax.text(5, 6.35, "User (PDF upload + topic)", ha="center", va="center",
            fontsize=8.5, fontweight="bold")

    ax.add_patch(FancyBboxPatch((2.5, 4.7), 5.0, 0.85, boxstyle="round,pad=0.05",
                                facecolor="#D6EAF8", edgecolor="#2980B9", lw=1.5))
    ax.text(5, 5.13, "app.py (Streamlit UI)", ha="center", va="center",
            fontsize=8.5, fontweight="bold", color="#2980B9")
    ax.text(5, 4.83, "sanitize_topic() → session state → hybrid scoring → security tab",
            ha="center", va="center", fontsize=7.5)

    ax.add_patch(FancyBboxPatch((0.3, 3.3), 4.0, 0.85, boxstyle="round,pad=0.05",
                                facecolor="#FDEDEC", edgecolor="#E74C3C", lw=1.5))
    ax.text(2.3, 3.73, "security.py", ha="center", va="center",
            fontsize=8.5, fontweight="bold", color="#E74C3C")
    ax.text(2.3, 3.43, "scan_for_injection | sanitize_topic\nclassify_document | validate_topic_relevance",
            ha="center", va="center", fontsize=7)

    ax.add_patch(FancyBboxPatch((5.7, 3.3), 4.0, 0.85, boxstyle="round,pad=0.05",
                                facecolor="#F9F3FF", edgecolor="#8E44AD", lw=1.5))
    ax.text(7.7, 3.73, "backend.py", ha="center", va="center",
            fontsize=8.5, fontweight="bold", color="#8E44AD")
    ax.text(7.7, 3.43, "SECURITY_PREFIX | scan_documents_for_security\ngenerate_quiz_experiment | _coerce_quiz_structure",
            ha="center", va="center", fontsize=7)

    modes = [
        (1.5, 1.8, "Fine-tuned\nGPT-4.1-mini", "#D5F5E3", "#27AE60"),
        (5.0, 1.8, "Grounded RAG\nChromaDB + gpt-4o-mini", "#D6EAF8", "#2980B9"),
        (8.5, 1.8, "Experimental\nV1 / V2 / V3", "#FEF9E7", "#F39C12"),
    ]
    for (x, y, label, fc, ec) in modes:
        ax.add_patch(FancyBboxPatch((x - 1.2, y - 0.35), 2.4, 0.75,
                                    boxstyle="round,pad=0.05", facecolor=fc, edgecolor=ec, lw=1.2))
        ax.text(x, y, label, ha="center", va="center", fontsize=7.5, multialignment="center")

    ax.add_patch(FancyBboxPatch((2.5, 0.4), 5.0, 0.75, boxstyle="round,pad=0.05",
                                facecolor="#D5F5E3", edgecolor="#27AE60", lw=1.5))
    ax.text(5, 0.78, "Secure quiz + sources + quality metrics + security status",
            ha="center", va="center", fontsize=8)

    for (x1, y1, x2, y2) in [
        (5, 6.0, 5, 5.55), (2.5, 4.7, 2.3, 4.15), (7.5, 4.7, 7.7, 4.15),
        (2.3, 3.3, 1.5, 2.15), (7.7, 3.3, 5.0, 2.15),
        (7.7, 3.3, 8.5, 2.15), (5, 1.45, 5, 1.15),
    ]:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="#555555", lw=0.8))

    fig.tight_layout(pad=0.3)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf


# ── Figure 3: Threat Model ─────────────────────────────────────────────────────
def fig_threat_model():
    fig, ax = plt.subplots(figsize=(7, 3.8))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")

    rows = [
        ("Topic field", "User-supplied quiz topic", "Injection via topic text"),
        ("PDF upload", "Lecture content fed into LLM", "Indirect injection in document"),
        ("System prompts", "Instructions sent to GPT", "Jailbreak / override attempts"),
        ("Short-answer scoring", "LLM judge evaluates free text", "Manipulation via crafted answers"),
    ]
    col_x = [0.2, 3.2, 6.5]
    headers = ["Component", "Role", "Attack Surface"]
    for j, (hdr, x) in enumerate(zip(headers, col_x)):
        ax.text(x, 4.6, hdr, fontsize=9, fontweight="bold", va="center")

    colors = ["#EAF4FB", "#FEF9E7", "#FDEDEC", "#E9F7EF"]
    for i, (comp, role, atk) in enumerate(rows):
        y = 3.8 - i * 0.9
        ax.add_patch(plt.Rectangle((0, y - 0.35), 9.8, 0.7,
                                   color=colors[i], ec="#CCCCCC", lw=0.5))
        ax.text(col_x[0], y, comp, fontsize=8.5, va="center")
        ax.text(col_x[1], y, role, fontsize=8.5, va="center")
        ax.text(col_x[2], y, atk, fontsize=8.5, va="center")

    fig.tight_layout(pad=0.3)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf


# ── Figure 4: Attack 1 Flow ────────────────────────────────────────────────────
def fig_attack1_flow():
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")

    boxes = [
        (5, 5.3, "Attacker enters malicious topic string", "#E8F8F5", "#1ABC9C"),
        (5, 4.2, "Topic field passed to LLM prompt\n(pre-hardening: unsanitized)", "#FEF9E7", "#F39C12"),
        (2.0, 2.8, "No system prompt\nPartial compliance / refusal", "#FDEDEC", "#E74C3C"),
        (5.0, 2.8, "V1 minimal prompt\nGPT safety resists", "#FEF9E7", "#F39C12"),
        (8.0, 2.8, "sanitize_topic()\nBLOCKED before LLM", "#E8F8F5", "#1ABC9C"),
        (5, 1.4, "SECURITY_PREFIX\nExplicit refusal, structured JSON", "#E8F8F5", "#2ECC71"),
    ]
    for (x, y, label, fc, ec) in boxes:
        ax.add_patch(FancyBboxPatch((x - 1.5, y - 0.4), 3.0, 0.8,
                                    boxstyle="round,pad=0.05", facecolor=fc, edgecolor=ec, lw=1.2))
        ax.text(x, y, label, ha="center", va="center", fontsize=7.5, multialignment="center")

    for (x1, y1, x2, y2) in [
        (5, 4.9, 5, 4.6), (5, 3.8, 2.0, 3.2), (5, 3.8, 5.0, 3.2),
        (5, 3.8, 8.0, 3.2), (8.0, 2.4, 5, 1.8),
    ]:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="#555555", lw=1))

    ax.text(1.2, 3.6, "Scenario A", fontsize=7, color="#888")
    ax.text(4.2, 3.6, "Scenario B", fontsize=7, color="#888")
    ax.text(6.8, 3.6, "Defense", fontsize=7, color="#2ECC71", fontweight="bold")

    fig.tight_layout(pad=0.3)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf


# ── Figure 5: Attack 2 Flow ────────────────────────────────────────────────────
def fig_attack2_flow():
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6.5); ax.axis("off")
    ax.text(5, 6.2, "Attack 2: Malicious Document Injection", ha="center",
            fontsize=9, fontweight="bold")

    col_data = [
        (1.8, "Obvious injection\n[SYSTEM OVERRIDE]", "#FDEDEC", "#E74C3C"),
        (5.0, "Subtle injection\n'Instructor note: QUIZ LOG:'", "#FEF9E7", "#F39C12"),
        (8.2, "Language-switch\n'respond only in French'", "#FEF9E7", "#F39C12"),
    ]
    for (x, label, fc, ec) in col_data:
        ax.add_patch(FancyBboxPatch((x - 1.4, 5.0), 2.8, 0.8,
                                    boxstyle="round,pad=0.05", facecolor=fc, edgecolor=ec, lw=1.2))
        ax.text(x, 5.4, label, ha="center", va="center", fontsize=7.5, multialignment="center")

    pre_results = [
        (1.8, "GPT resisted", "#2ECC71"),
        (5.0, "Model complied\n'QUIZ LOG:' prefix", "#E74C3C"),
        (8.2, "Model complied\nFrench quiz", "#E74C3C"),
    ]
    ax.text(5, 4.35, "Pre-defense (V2 baseline)", ha="center", fontsize=8, color="#888888")
    for (x, result, color) in pre_results:
        ax.add_patch(FancyBboxPatch((x - 1.4, 3.5), 2.8, 0.65,
                                    boxstyle="round,pad=0.05", facecolor="#F8F9FA", edgecolor=color, lw=1.5))
        ax.text(x, 3.83, result, ha="center", va="center", fontsize=7.5,
                color=color, multialignment="center")
        ax.annotate("", xy=(x, 3.5), xytext=(x, 4.9),
                    arrowprops=dict(arrowstyle="->", color="#555", lw=0.8))

    ax.add_patch(FancyBboxPatch((2.0, 2.3), 6.0, 0.8, boxstyle="round,pad=0.05",
                                facecolor="#E8F8F5", edgecolor="#1ABC9C", lw=1.5))
    ax.text(5, 2.7, "scan_for_injection()  ✓ Detects all 3 variants\n"
            "17 regex patterns | risk: high → blocked | risk: medium → warning",
            ha="center", va="center", fontsize=7.5, multialignment="center")

    for x, tx in zip([1.8, 5.0, 8.2], [3.0, 5.0, 7.0]):
        ax.annotate("", xy=(tx, 3.1), xytext=(x, 3.15),
                    arrowprops=dict(arrowstyle="->", color="#1ABC9C", lw=0.8,
                                   connectionstyle="arc3,rad=0.0"))

    ax.add_patch(FancyBboxPatch((2.0, 1.1), 6.0, 0.8, boxstyle="round,pad=0.05",
                                facecolor="#E8F8F5", edgecolor="#2ECC71", lw=1.5))
    ax.text(5, 1.5, "SECURITY_PREFIX in all system prompts\n"
            "Second line of defense if document passes the scanner",
            ha="center", va="center", fontsize=7.5, multialignment="center")
    ax.annotate("", xy=(5, 1.5), xytext=(5, 2.3),
                arrowprops=dict(arrowstyle="->", color="#2ECC71", lw=0.8))

    fig.tight_layout(pad=0.3)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf


# ── Figure 6: Attack Success Rate Bar Chart ────────────────────────────────────
def fig_security_results():
    fig, ax = plt.subplots(figsize=(6.5, 3.5))
    attacks = ["Attack 1\n(Topic Injection)", "Attack 2\n(Doc Injection)", "Attack 3\n(Jailbreak)"]
    pre = [0, 2, 0]
    post = [0, 0, 0]
    total = [3, 3, 3]
    x = [0, 2, 4]
    w = 0.7

    ax.bar([xi - w / 2 for xi in x], [p / t * 100 for p, t in zip(pre, total)],
           w, label="Pre-hardening (% successful attacks)", color="#E74C3C", alpha=0.8)
    ax.bar([xi + w / 2 for xi in x], [p / t * 100 for p, t in zip(post, total)],
           w, label="Post-hardening (% successful attacks)", color="#27AE60", alpha=0.8)
    ax.text(2 - w / 2, pre[1] / total[1] * 100 + 2, "2/3 subtypes\ncomplied",
            ha="center", fontsize=7, color="#E74C3C")

    ax.set_xticks(x)
    ax.set_xticklabels(attacks, fontsize=9)
    ax.set_ylabel("Attack Success Rate (%)", fontsize=9)
    ax.set_ylim(0, 100)
    ax.legend(fontsize=8)
    ax.set_title("Attack Success Rate: Pre-Hardening vs. Post-Hardening", fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout(pad=0.5)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf


# ── Figure 7: Defense Layers ───────────────────────────────────────────────────
def fig_defense_layers():
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis("off")

    layers = [
        (1, "Defense 1: Input Sanitization (sanitize_topic)",
         "Topic field blocked before LLM call — 17 patterns", "#E8F8F5", "#1ABC9C"),
        (2, "Defense 2: Document Scanning (scan_for_injection)",
         "PDF content scanned — high risk blocked, medium risk warned", "#EAF4FB", "#2980B9"),
        (3, "Defense 3: Hardened System Prompts (SECURITY_PREFIX)",
         "All prompts (V1/V2/V3/FT) include explicit injection-resistance", "#EBF5FB", "#3498DB"),
        (4, "Defense 4: Topic Relevance Validation",
         "LLM checks topic coverage in document — warns if < 50%", "#F9F3FF", "#8E44AD"),
        (5, "Defense 5: Schema Coercion (_coerce_quiz_structure)",
         "Output always forced to valid schema — prevents hijacked responses", "#FEF9E7", "#F39C12"),
    ]
    for (i, title, desc, fc, ec) in layers:
        y = 6.5 - i * 1.15
        ax.add_patch(FancyBboxPatch((0.3, y - 0.35), 9.4, 0.75,
                                    boxstyle="round,pad=0.05", facecolor=fc, edgecolor=ec, lw=1.5))
        ax.text(0.7, y + 0.05, f"Layer {i}", fontsize=8, fontweight="bold", color=ec, va="center")
        ax.text(2.0, y + 0.05, title.split(": ", 1)[1], fontsize=8.5, fontweight="bold", va="center")
        ax.text(2.0, y - 0.2, desc, fontsize=7.5, color="#555555", va="center")

    fig.tight_layout(pad=0.3)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf


# ── Figure 8: Defense Pipeline ─────────────────────────────────────────────────
def fig_defense_pipeline():
    fig, ax = plt.subplots(figsize=(6.5, 5.0))
    ax.set_xlim(0, 10); ax.set_ylim(0, 8); ax.axis("off")

    steps = [
        (5, 7.3, "User submits topic + PDF", "#D5F5E3", "#27AE60"),
        (5, 6.2, "Step 1: sanitize_topic()\nHigh risk → BLOCKED", "#D5F5E3", "#27AE60"),
        (5, 5.1, "Step 2: scan_documents_for_security()\nHigh risk → BLOCKED | Medium → Warning",
         "#D6EAF8", "#2980B9"),
        (5, 4.0, "Step 3: classify_document()\nWebsite/Article → Warning shown to user",
         "#D6EAF8", "#2980B9"),
        (5, 2.9, "Step 4: generate_quiz_experiment()\nAll prompts include SECURITY_PREFIX",
         "#F9F3FF", "#8E44AD"),
        (5, 1.8, "Step 5: validate_topic_relevance()\nCoverage < 50% → Warning",
         "#FEF9E7", "#F39C12"),
        (5, 0.7, "Secure quiz delivered to user", "#D5F5E3", "#27AE60"),
    ]
    for (x, y, label, fc, ec) in steps:
        ax.add_patch(FancyBboxPatch((x - 3.5, y - 0.38), 7.0, 0.78,
                                    boxstyle="round,pad=0.05", facecolor=fc, edgecolor=ec, lw=1.2))
        ax.text(x, y, label, ha="center", va="center", fontsize=8, multialignment="center")

    for i in range(len(steps) - 1):
        y1 = steps[i][1] - 0.38
        y2 = steps[i + 1][1] + 0.40
        ax.annotate("", xy=(5, y2), xytext=(5, y1),
                    arrowprops=dict(arrowstyle="->", color="#555555", lw=1))

    for (y, label) in [(6.2, "BLOCKED"), (5.1, "BLOCKED")]:
        ax.add_patch(FancyBboxPatch((8.0, y - 0.25), 1.6, 0.5,
                                    boxstyle="round,pad=0.05",
                                    facecolor="#FDEDEC", edgecolor="#E74C3C", lw=1.2))
        ax.text(8.8, y, label, ha="center", va="center", fontsize=7.5,
                color="#E74C3C", fontweight="bold")
        ax.annotate("", xy=(8.0, y), xytext=(6.5, y),
                    arrowprops=dict(arrowstyle="->", color="#E74C3C", lw=0.8))

    fig.tight_layout(pad=0.3)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf


# ── Figure 10: Assignment Evolution ───────────────────────────────────────────
def fig_assignment_evolution():
    fig, ax = plt.subplots(figsize=(6.5, 3.5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")

    items = [
        (0.5, 4.3, "A3: System prompt setup",
         "Zero-shot, few-shot, CoT, self-consistency, self-criticism", "#D5F5E3", "#27AE60"),
        (0.5, 3.3, "A4: Fine-tuning + RAG pipeline",
         "Prompt sensitivity, dataset curation, fine-tuned GPT-4.1-mini, ChromaDB", "#D6EAF8", "#2980B9"),
        (0.5, 2.3, "A5: LangChain + Azure Prompt Flow",
         "V1/V2/V3 variants, automated evaluation, DAG orchestration", "#F9F3FF", "#8E44AD"),
        (0.5, 1.3, "A6: Test and refinement",
         "4-file pytest, 17 iterations, hybrid scoring, full-text groundedness", "#FEF9E7", "#F39C12"),
        (0.5, 0.3, "A7: Prompt Hacking & Security",
         "5-layer defense, injection scanning, hardened prompts, topic validation, num_questions",
         "#FDEDEC", "#E74C3C"),
    ]
    for (x, y, title, desc, fc, ec) in items:
        ax.add_patch(FancyBboxPatch((x, y - 0.35), 9.0, 0.75,
                                    boxstyle="round,pad=0.05", facecolor=fc, edgecolor=ec, lw=1.5))
        ax.text(x + 0.1, y + 0.05, title, fontsize=8.5, fontweight="bold", va="center", color=ec)
        ax.text(x + 0.1, y - 0.2, desc, fontsize=7.5, va="center", color="#555555")

    for i in range(len(items) - 1):
        y1 = items[i][1] - 0.35
        y2 = items[i + 1][1] + 0.40
        ax.annotate("", xy=(0.1, y2), xytext=(0.1, y1),
                    arrowprops=dict(arrowstyle="->", color="#888888", lw=1))

    fig.tight_layout(pad=0.3)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf


# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Saving figures to: {OUT_DIR}\n")

    save(fig_system_architecture(),  "Figure_02_System_Architecture.png")
    save(fig_threat_model(),          "Figure_03_Threat_Model.png")
    save(fig_attack1_flow(),          "Figure_04_Attack1_Flow.png")
    save(fig_attack2_flow(),          "Figure_05_Attack2_Flow.png")
    save(fig_security_results(),      "Figure_06_Attack_Success_Rate.png")
    save(fig_defense_layers(),        "Figure_07_Defense_Layers.png")
    save(fig_defense_pipeline(),      "Figure_08_Defense_Pipeline.png")
    save(fig_assignment_evolution(),  "Figure_10_Assignment_Evolution.png")

    print(f"\nDone. Open the 'figures' folder in Finder to view all images.")
    print("Insert each PNG into your Word doc at the corresponding Figure location.")
