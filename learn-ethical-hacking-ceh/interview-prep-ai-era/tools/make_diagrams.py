#!/usr/bin/env python3
"""New diagrams for the AI-agent-era edition (SVG into ../images). Usage: python3 make_diagrams.py
Diagrams reused from the two earlier books are copied by hand and not regenerated here."""
import os
from diagram_lib import S, wrap, OUT, NAVY, TEAL, RED, GREEN, AMBER, INK, MUTE, GREY, WHITE, PINK, MINT, SKY, SAND, FONT, MONO


def bullets(s, x, y, items, width, size=11.5, color=INK, dot=MUTE, gap=7):
    for it in items:
        lines = wrap(it, width, size, False)
        s.text(x, y, "•", size, dot, "bold")
        s.text(x + 14, y, "\n".join(lines), size, color, lh=1.28)
        y += len(lines) * size * 1.28 + gap
    return y


def agent_trust():
    s = S(880, 470, "What a coding agent reads, and what it can do", "Anything it reads can steer it; anything it can do, an attacker steering it can do")
    s.rect(20, 78, 250, 290, PINK, RED, 12, dash=True); s.text(145, 100, "INPUTS (some hostile)", 13, RED, "bold", "middle")
    bullets(s, 34, 124, ["Your prompt (trusted)", "Repo files, README, comments", "Issues, PRs, commit messages", "Web pages and docs it fetches", "MCP server and tool output", "Package READMEs and install output"], 222, 11.5, INK, RED)
    s.box(310, 150, 260, 130, "AI coding agent\n(model + tools)\n\nCannot reliably tell\ndata from instructions", SKY, TEAL, INK, 13, "bold")
    s.arrow(272, 215, 308, 215, RED); s.arrow(572, 215, 608, 215, AMBER)
    s.rect(610, 78, 250, 290, SAND, AMBER, 12); s.text(735, 100, "CAPABILITIES", 13, AMBER, "bold", "middle")
    bullets(s, 624, 124, ["Run shell commands", "Read and write files", "Install packages", "Use tokens and env secrets", "Network calls, git push", "Call other tools (MCP)"], 222, 11.5, INK, AMBER)
    s.rect(20, 385, 840, 70, MINT, GREEN, 10)
    s.ctext(440, 420, "Defence: least privilege, a sandbox, no secrets in the environment, human approval for risky actions, and review of every diff.", 12.5, INK, "bold", width=800)
    s.save("agent-trust-boundary")


def permission_ladder():
    s = S(880, 400, "Agent permission ladder: start low, raise on purpose", "Match the autonomy to the blast radius")
    rungs = [("1  Read-only", "Explain, search, plan", GREEN, MINT), ("2  Edit with approval", "You approve each write and command", TEAL, SKY),
             ("3  Auto in a sandbox", "Container or VM, no real secrets, no prod network", AMBER, SAND), ("4  Full auto on your machine", "Your files, your tokens, your shell", RED, PINK)]
    x = 20
    for i, (t, b, c, f) in enumerate(rungs):
        y = 285 - i * 62
        s.rect(x + i * 20, y, 380 + i * 20, 52, f, c, 10); s.text(x + i * 20 + 14, y + 22, t, 13, c, "bold"); s.text(x + i * 20 + 14, y + 41, b, 11, INK)
    s.rect(540, 90, 320, 150, WHITE, NAVY, 12)
    s.text(556, 114, "Rules of thumb", 13, NAVY, "bold")
    bullets(s, 556, 136, ["Rungs 3 and 4 are where incidents happen", "Never run rung 4 on a machine with prod or cloud credentials", "Treat 'allow always' as a permanent grant"], 290, 11.5, INK, NAVY)
    s.rect(20, 345, 840, 42, SKY, TEAL, 10)
    s.ctext(440, 366, "Tool names differ (permission modes, sandboxes, 'yolo' or auto-approve settings), the idea is the same.", 12, INK, "bold", width=800)
    s.save("agent-permission-ladder")


def injection_flow():
    s = S(880, 430, "Indirect prompt injection against a coding agent", "The attacker never talks to the agent; they plant text where the agent will read it")
    steps = [("1  Plant", "Hidden instruction in an issue, a README, a web page or a package", RED, PINK), ("2  Read", "Agent opens the content as part of a normal task", AMBER, SAND),
             ("3  Obey", "Model treats the text as a command", AMBER, SAND), ("4  Act", "Agent runs a command, edits a file or sends data out", RED, PINK)]
    x = 20
    for i, (t, b, c, f) in enumerate(steps):
        s.rect(x + i * 215, 85, 195, 120, f, c, 10); s.text(x + i * 215 + 12, 110, t, 14, c, "bold"); s.text(x + i * 215 + 12, 134, "\n".join(wrap(b, 172, 11.5, False)), 11.5, INK, lh=1.3)
        if i < 3:
            s.arrow(x + i * 215 + 197, 145, x + i * 215 + 213, 145, MUTE)
    s.rect(20, 225, 840, 190, MINT, GREEN, 12); s.text(36, 250, "Where you break the chain", 14, GREEN, "bold")
    bullets(s, 36, 274, ["Before 'Read': treat all fetched content as untrusted; do not point agents at untrusted issues or pages with write access.",
                         "Before 'Act': human approval for shell, network, and file writes outside the project; allowlist commands.",
                         "Limit the damage: no secrets in the environment, scoped short-lived tokens, a sandbox with no route to production.",
                         "After: review the diff and the commands the agent ran; CI gates catch what slips through."], 800, 12, INK, GREEN, 8)
    s.save("prompt-injection-agent-flow")


def review_loop():
    s = S(880, 390, "The review loop when an agent writes the code", "The agent is fast; the safety comes from what you check after")
    items = [("Prompt", "State the constraints: authz, validation, no new deps", SKY, TEAL), ("Agent writes", "Diff + tests", GREY, MUTE), ("You review", "5 questions: who, allowed, controlled, destination, failure", SAND, AMBER),
             ("Automated gates", "Tests, SAST, secret scan, dependency check", MINT, GREEN), ("Merge", "Small PRs, human approval, CODEOWNERS", SKY, TEAL)]
    for i, (t, b, f, c) in enumerate(items):
        x = 20 + i * 170
        s.rect(x, 90, 155, 150, f, c, 10); s.text(x + 10, 114, t, 13, c, "bold"); s.text(x + 10, 138, "\n".join(wrap(b, 135, 11, False)), 11, INK, lh=1.3)
        if i < 4:
            s.arrow(x + 156, 165, x + 169, 165, MUTE)
    s.rect(20, 265, 840, 105, WHITE, NAVY, 12); s.text(36, 290, "What to check hardest in AI-written code", 13, NAVY, "bold")
    bullets(s, 36, 312, ["Authorization on every object and action (agents often add only login checks)", "New dependencies: does the package exist, is it the real one, is it needed?",
                         "Secrets, tokens and example keys; shell and SQL built from strings; permissive CORS and CSP"], 800, 11.5, INK, NAVY, 5)
    s.save("ai-review-loop")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for f in (agent_trust, permission_ladder, injection_flow, review_loop):
        f()
    print("ok")
