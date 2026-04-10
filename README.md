# human-skill

**Human behavior mechanism engine with 16 axes and 44 meta-principles — diagnose, predict, and design based on cognitive science, influence theory, motivation, and behavior design.**

## Prerequisites

- **Claude Cowork or Claude Code** environment

## Goal

Every product, policy, message, and interaction succeeds or fails based on human behavior. Human-Skill maps behavior across 16 axes from 6 scientific sources (Kahneman, Cialdini, SDT, Evolutionary Psychology, Emotion Theory, Behavior Design), providing three modes: Diagnose (why), Predict (what next), and Design (what triggers).

## When & How to Use

Use when optimizing for human behavior: product adoption, messaging, hiring, team dynamics, policy persuasion, UX. Choose mode — Diagnose, Predict, or Design. The skill maps across 16 behavioral axes and delivers output structured around 44 meta-principles.

## Use Cases

| Scenario | Prompt | What Happens |
|---|---|---|
| Conversion stuck at 3% | `"human-skill DESIGN: why won't people upgrade from free to paid?"` | Motivation axes→identifies barriers vs. triggers→design interventions |
| Team missing deadlines | `"human-skill DIAGNOSE: team commits then misses. What's happening?"` | Cognitive bias analysis→emotional factors→root causes→solutions |
| Policy adoption low | `"human-skill PREDICT: if we mandate this policy, how do people respond?"` | 16-axis prediction: autonomy threat→reactance risk→intervention points |

## Key Features

- 16-axis framework: Kahneman (7), Cialdini (3), SDT (2), Evolutionary (2), Emotion (1), Behavior Design (1)
- 44 meta-principles linking scientific sources to practical action
- Three modes: Diagnose, Predict, Design
- 6 integrated scientific sources
- Works across products, policies, marketing, hiring, operations, team dynamics

## Works With

- **[hit-skill](https://github.com/jasonnamii/hit-skill)** — hit-skill's 3-layer architecture is powered by human-skill diagnostics
- **[biz-skill](https://github.com/jasonnamii/biz-skill)** — strategies integrate human-skill behavior design
- **[ui-action-designer](https://github.com/jasonnamii/ui-action-designer)** — uses human-skill for user interaction design

## Installation

```bash
git clone https://github.com/jasonnamii/human-skill.git ~/.claude/skills/human-skill
```

## Update

```bash
cd ~/.claude/skills/human-skill && git pull
```

Skills placed in `~/.claude/skills/` are automatically available in Claude Code and Cowork sessions.

## Part of Cowork Skills

This is one of 25+ custom skills. See the full catalog: [github.com/jasonnamii/cowork-skills](https://github.com/jasonnamii/cowork-skills)

## License

MIT License — feel free to use, modify, and share.
