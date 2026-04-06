# PyHamiltonSteps

## What this is meant to do

PyHamiltonSteps provides a **direct, one-to-one Python interface to Hamilton Venus steps**.

Each Venus step is exposed as a Python function with all parameters preserved. There is no abstraction layer, no workflow logic, and no hidden behavior.

The purpose:

- Give complete, explicit control over the Hamilton STAR robot  
- Mirror Venus behavior as closely as possible  
- Avoid introducing opinionated layers between the user and the instrument  

---

## What this foundation provides

PyHamiltonSteps is designed as a **foundation layer**.

It establishes a deterministic, low-level interface that other systems can build on without interference.

### Core capabilities

- **1:1 mapping of Venus steps to Python functions**
- **Full parameter transparency** — nothing is hidden or inferred  
- **Single-step execution model** — only one command runs at a time  
- **Deterministic communication** via persistent serial connection  
- **Log-based validation** using Hamilton’s native output as the source of truth  
- **Strict liquid class constraints** using defined enumerations  

### Communication model

- JSON command/response protocol  
- Persistent serial connection (no HTTP polling)  
- Blocking execution (no asynchronous ambiguity)  
- Designed to minimize log noise and avoid flooding  

---

## What this enables

Because this library does not abstract or interpret behavior, it becomes a great foundation for higher level systems.

### AI-driven protocol composition

AI systems can:

- Call Venus steps directly as tools  
- Compose complex protocols step-by-step  
- Operate without guessing or reverse-engineering behavior  

There is no hidden logic to conflict with.

---

### REST-based orchestration (FastAPI layer)

A FastAPI layer can expose this local control interface over a network.

This enables:

- Coordination across multiple Hamilton instruments  
- Remote execution of liquid handling steps  
- Multi-machine orchestration without modifying the core system  

---

### Model-driven control (MCP layer)

A Model Context Protocol (MCP) wrapper exposes Hamilton control as structured tools.

This allows:

- LLMs to reason about and execute real laboratory actions  
- Tool-based interaction with the instrument  
- Safe, bounded execution through explicit step calls  

---

## Architecture

- **PyHamiltonSteps (core)**  
  Local Python library communicating directly with Venus via a persistent serial JSON protocol  

- **FastAPI layer**  
  Network-accessible REST interface for orchestration across systems  

- **MCP layer**  
  AI-facing interface exposing Hamilton control as tools  

---

This system is intentionally minimal so higher-level systems can build on it cleanly.
