
# 🧠 SMARTDREAM Gradio GUI Development Checklist

## 🎯 Goal: Build a cognitive dashboard to control, observe, and interact with SMARTDREAM agents + substrate

---

## 🧩 1. Problem Input Interface
- [ ] Add text input for `problem_prompt` (freeform problem or intent)
- [ ] Dropdown for `mode` selection (Drift, Mirror, Imaginarium, Market, Collapse)
- [ ] Input: number of agents
- [ ] Input: phase duration or tick count
- [ ] Slider: dark matter multiplier
- [ ] Slider or toggle: ghost symbol sensitivity

---

## 🔁 2. Simulation Control
- [ ] Button: `Run step`
- [ ] Button: `Run full cycle`
- [ ] Button: `Reset simulation`
- [ ] Display: current phase / time tick
- [ ] Checkbox: enable/disable `VisionChannel`
- [ ] Checkbox: enable/disable `Harvester`
- [ ] Checkbox: export output after phase

---

## 🧠 3. Live Symbolic Feedback
- [ ] Live display: seer scores
- [ ] Live display: agent energy + dose
- [ ] Live display: symbolic drift or schema change
- [ ] Live display: harvested insights (clarity, alignment, entropy)
- [ ] Download button for symbolic outputs (`.json`, `.txt`, `.md`)

---

## 🧪 4. Exploration Tools (Advanced, optional)
- [ ] Sandbox: define or load symbolic schema vector
- [ ] Slider: test dark mass against ghost symbol
- [ ] Button: force-collapse / white hole trigger
- [ ] Visualizer: orbit/collision of schema anchors
- [ ] Entropy heatmap or drift field plot (if feasible)

---

## 🔧 Backend Functions (support logic)
- [ ] `process_problem(prompt, params)` → symbolic schema config
- [ ] `run_simulation_step()` → execute one cycle
- [ ] `get_dashboard_state()` → return state for visualization
- [ ] `harvest_results()` → extract symbolic insights
- [ ] `reset_simulation()` → restart substrate + agents

---

## 🚀 Final Integration
- [ ] Add Gradio layout with `gr.Blocks`
- [ ] Link frontend inputs to backend calls
- [ ] Display real-time output logs
- [ ] Package `gradio_app.py` for CLI run

