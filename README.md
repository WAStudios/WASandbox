# WAStudios

**WAStudios** is an ambitious, multi-stage toolset designed to revolutionize how World of Warcraft players develop and test WeakAuras for raid encounters—without needing to step into the game.

## Why WAStudios?

Developing advanced WeakAuras for raid bosses often requires testing under specific, real-time raid conditions. This typically means:

- Being in an actual raid encounter.
- Coordinating with other players, who may not be reliable or willing to reset fights for testing.
- Repeating specific boss mechanics under controlled conditions, which is impractical with live groups.
  
These constraints make rapid iteration and debugging of complex WeakAuras both time-consuming and frustrating.

WAStudios aims to solve that by enabling a local, sandboxed environment to create, test, and simulate WeakAuras—powered by real encounter data.

---

## Project Stages

### ✅ Stage 1: WeakAura Sandbox Engine
Build a Python 3 application with a user-friendly interface that mimics the in-game LUA engine and core Blizzard API components required to run WeakAuras. This engine will allow real-time editing, previewing, and testing of WeakAuras as if they were in-game.

> ✅ Goal: Fully run the actual [WeakAuras2 Addon](https://github.com/WeakAuras/WeakAuras2) in this simulated environment using live or custom data.

---

### 🔄 Stage 2: WoWCombatLog Simulation Engine
Parse and replay raid boss encounters using real WoWCombatLog data. This engine will:
- Extract accurate timing and event sequences from combat logs.
- Simulate raid boss mechanics and player responses.
- Feed those events into the sandboxed WeakAura engine to simulate full encounters offline.

> 🔁 Imagine watching your WeakAura react to a full Mythic boss fight—no raid group required.

---

### 🚧 Stage 3: Community-Driven Boss Library
Launch a public platform where players can submit their WoWCombatLogs. This crowdsourced approach will:
- Build a comprehensive library of real boss fights across difficulties.
- Provide a growing catalog of raid encounters to test and validate WeakAuras against.
- Help standardize WeakAura development with high-fidelity, real-world data.

---

## Vision

WAStudios is built to empower WeakAura creators with tools for **rapid iteration**, **deep testing**, and **high accuracy**, completely decoupled from the limitations of live raid environments. Whether you're debugging advanced logic or simulating Mythic encounters, WAStudios will bring the power of in-game addon development to your desktop.

---

### Stay Tuned

This project is in active development. Follow along for updates, or contribute to the development if you're passionate about WoW addon tooling, LUA emulation, or combat log parsing.