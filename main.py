import asyncio
import inspect
import json
import math
import threading
import time
import traceback
from datetime import datetime
from pathlib import Path
from tkinter import Tk, StringVar, END, Canvas
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from typing import Any, Dict, Tuple

from dotenv import load_dotenv


def _load_agent_factories() -> Tuple[Dict[str, Any], Dict[str, str]]:
  """Load agent classes lazily and capture import errors per provider."""
  factories: Dict[str, Any] = {}
  errors: Dict[str, str] = {}

  try:
    from agents.openai_agent import NeuralMemoryAgent

    factories["OpenAI (Neural Memory)"] = NeuralMemoryAgent
  except Exception as exc:
    errors["OpenAI (Neural Memory)"] = str(exc)

  try:
    from agents.anthropic_agent import MemoryContextAgent

    factories["Anthropic (Memory Context)"] = MemoryContextAgent
  except Exception as exc:
    errors["Anthropic (Memory Context)"] = str(exc)

  try:
    from agents.mistral_agent import MemoryGateAgent

    factories["Mistral (Memory Gate)"] = MemoryGateAgent
  except Exception as exc:
    errors["Mistral (Memory Gate)"] = str(exc)

  try:
    from agents.groq_agent import MemoryLayerAgent

    factories["Groq (Memory Layer)"] = MemoryLayerAgent
  except Exception as exc:
    errors["Groq (Memory Layer)"] = str(exc)

  try:
    from agents.gemini_agent import ExperimentalAgent

    factories["Gemini (Experimental)"] = ExperimentalAgent
  except Exception as exc:
    errors["Gemini (Experimental)"] = str(exc)

  try:
    from agents.cohere_agent import InnovationsAgent

    factories["Cohere (Innovations)"] = InnovationsAgent
  except Exception as exc:
    errors["Cohere (Innovations)"] = str(exc)

  try:
    from agents.emergence_agent import AnalysisAgent

    factories["Emergence (Analysis)"] = AnalysisAgent
  except Exception as exc:
    errors["Emergence (Analysis)"] = str(exc)

  return factories, errors


class TitansDesktopApp:
  def __init__(self):
    load_dotenv()

    self.root = Tk()
    self.root.title("Titans Native Desktop")
    self.root.geometry("1100x760")

    self.factories, self.import_errors = _load_agent_factories()
    self.agents: Dict[str, Any] = {}
    self.agent_init_errors: Dict[str, str] = {}
    self.is_busy = False
    self.busy_started_at = 0.0

    self.visual_series_name = ""
    self.visual_series = []
    self.visual_index = 0
    self.visual_playing = False
    self.runtime_phase = 0.0
    self.runtime_after_id = None
    self.ui_state_path = Path(__file__).with_name("titans_ui_state.json")
    self.split_ratio = 0.5

    self._load_ui_state()

    self._initialize_agents()
    self._build_ui()
    self._refresh_agent_details()

  def _initialize_agents(self) -> None:
    for display_name, factory in self.factories.items():
      try:
        self.agents[display_name] = factory()
      except Exception as exc:
        self.agent_init_errors[display_name] = str(exc)

  def _build_ui(self) -> None:
    main = ttk.Frame(self.root, padding=12)
    main.pack(fill="both", expand=True)

    title = ttk.Label(
      main,
      text="Titans: Learning to Memorize at Test Time",
      font=("Segoe UI", 16, "bold"),
    )
    title.pack(anchor="w")

    subtitle = ttk.Label(
      main,
      text="Native desktop runner for demonstrations, metrics, and agent collaboration.",
      font=("Segoe UI", 10),
    )
    subtitle.pack(anchor="w", pady=(0, 12))

    controls = ttk.Frame(main)
    controls.pack(fill="x", pady=(0, 8))

    ttk.Label(controls, text="Agent:").grid(row=0, column=0, sticky="w")
    self.selected_agent = StringVar()
    self.agent_combo = ttk.Combobox(
      controls,
      textvariable=self.selected_agent,
      state="readonly",
      values=self._all_agent_names(),
      width=36,
    )
    self.agent_combo.grid(row=0, column=1, sticky="w", padx=(8, 12))
    if self._all_agent_names():
      self.agent_combo.current(0)
    self.agent_combo.bind("<<ComboboxSelected>>", lambda _e: self._refresh_agent_details())

    self.btn_demo = ttk.Button(controls, text="Run Demonstration", command=self._run_demonstration)
    self.btn_demo.grid(row=0, column=2, padx=4)

    self.btn_insights = ttk.Button(
      controls, text="Generate Collaborative Insights", command=self._run_insights
    )
    self.btn_insights.grid(row=0, column=3, padx=4)

    self.btn_metrics = ttk.Button(controls, text="Refresh Metrics", command=self._refresh_metrics)
    self.btn_metrics.grid(row=0, column=4, padx=4)

    self.status_var = StringVar(value="Ready")
    status = ttk.Label(main, textvariable=self.status_var)
    status.pack(anchor="w", pady=(0, 2))

    self.runtime_var = StringVar(value="Runtime: 0.0s")
    ttk.Label(main, textvariable=self.runtime_var).pack(anchor="w", pady=(0, 4))
    self.runtime_bar = ttk.Progressbar(main, mode="indeterminate")
    self.runtime_bar.pack(fill="x", pady=(0, 8))

    ttk.Label(main, text="Ask selected agent:").pack(anchor="w")
    self.input_box = ScrolledText(main, height=4, wrap="word")
    self.input_box.pack(fill="x", pady=(4, 6))

    self.btn_interact = ttk.Button(main, text="Send Query", command=self._run_interaction)
    self.btn_interact.pack(anchor="w", pady=(0, 8))

    content = ttk.Panedwindow(main, orient="horizontal")
    content.pack(fill="both", expand=True)
    self.content_pane = content

    left = ttk.Frame(content)
    content.add(left, weight=1)

    ttk.Label(left, text="Output").pack(anchor="w")
    self.output_box = ScrolledText(left, height=16, wrap="word")
    self.output_box.pack(fill="both", expand=True)

    ttk.Label(left, text="Agent Details").pack(anchor="w", pady=(8, 0))
    self.details_box = ScrolledText(left, height=8, wrap="word")
    self.details_box.pack(fill="x")

    right = ttk.Frame(content, padding=(8, 0, 0, 0))
    content.add(right, weight=1)

    ttk.Label(right, text="Visual Interaction (Real-Time)", font=("Segoe UI", 10, "bold")).pack(anchor="w")
    self.visual_subtitle_var = StringVar(value="Run a demonstration to stream visualized behavior.")
    ttk.Label(right, textvariable=self.visual_subtitle_var, wraplength=340).pack(anchor="w", pady=(2, 6))

    self.visual_canvas = Canvas(
      right,
      width=420,
      height=310,
      bg="#0f172a",
      highlightthickness=1,
      highlightbackground="#334155",
    )
    self.visual_canvas.pack(fill="both", expand=True, anchor="w")

    visual_controls = ttk.Frame(right)
    visual_controls.pack(fill="x", pady=(8, 0))
    visual_controls.columnconfigure(1, weight=1)
    self.play_btn = ttk.Button(visual_controls, text="Play", command=self._toggle_visual_play)
    self.play_btn.grid(row=0, column=0, padx=(0, 6))

    self.visual_slider = ttk.Scale(
      visual_controls,
      from_=0,
      to=1,
      orient="horizontal",
      command=self._on_visual_scrub,
    )
    self.visual_slider.grid(row=0, column=1, sticky="ew")

    # Start with last remembered split and save when user drags the pane divider.
    self.root.after(50, self._apply_split_ratio)
    self.content_pane.bind("<ButtonRelease-1>", self._remember_split_position)

    self._draw_runtime_visual()

  def _all_agent_names(self):
    names = set(self.factories.keys()) | set(self.import_errors.keys())
    return sorted(names)

  def _load_ui_state(self) -> None:
    try:
      if not self.ui_state_path.exists():
        return
      state = json.loads(self.ui_state_path.read_text(encoding="utf-8"))
      ratio = float(state.get("split_ratio", 0.5))
      if 0.1 <= ratio <= 0.9:
        self.split_ratio = ratio
    except Exception:
      # Ignore malformed state and keep defaults.
      self.split_ratio = 0.5

  def _save_ui_state(self) -> None:
    try:
      payload = {"split_ratio": round(float(self.split_ratio), 4)}
      self.ui_state_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    except Exception:
      pass

  def _apply_split_ratio(self) -> None:
    if not hasattr(self, "content_pane"):
      return
    total_width = self.content_pane.winfo_width()
    if total_width <= 2:
      return
    try:
      sash = int(total_width * self.split_ratio)
      self.content_pane.sashpos(0, sash)
    except Exception:
      pass

  def _remember_split_position(self, _event=None) -> None:
    if not hasattr(self, "content_pane"):
      return
    try:
      total_width = self.content_pane.winfo_width()
      if total_width <= 2:
        return
      sash = self.content_pane.sashpos(0)
      ratio = sash / total_width
      ratio = min(0.9, max(0.1, ratio))
      if abs(ratio - self.split_ratio) >= 0.001:
        self.split_ratio = ratio
        self._save_ui_state()
    except Exception:
      pass

  def _get_selected_name(self) -> str:
    return self.selected_agent.get().strip()

  def _append_output(self, title: str, payload: Any) -> None:
    timestamp = datetime.now().strftime("%H:%M:%S")
    self.output_box.insert(END, f"\n[{timestamp}] {title}\n")
    if isinstance(payload, str):
      self.output_box.insert(END, payload + "\n")
    else:
      self.output_box.insert(END, json.dumps(payload, indent=2, default=str) + "\n")
    self.output_box.see(END)

  def _draw_runtime_visual(self) -> None:
    if not hasattr(self, "visual_canvas"):
      return

    width = int(self.visual_canvas.winfo_width() or 360)
    height = int(self.visual_canvas.winfo_height() or 310)
    self.visual_canvas.delete("all")

    self.visual_canvas.create_rectangle(10, 10, width - 10, height - 10, outline="#334155")

    if self.visual_series:
      self._draw_series_visual(width, height)
      return

    baseline = height // 2
    points = []
    for x in range(20, width - 20, 8):
      phase = (x / 32.0) + self.runtime_phase
      y = baseline + math.sin(phase) * 22
      points.extend([x, y])

    color = "#22d3ee" if self.is_busy else "#64748b"
    # During initial layout passes Tk can report tiny widths; skip line draw until enough points exist.
    if len(points) >= 4:
      self.visual_canvas.create_line(points, fill=color, width=2, smooth=True)
    label = "Streaming runtime telemetry..." if self.is_busy else "Idle - start an action to see live signal"
    self.visual_canvas.create_text(20, 24, text=label, anchor="w", fill="#cbd5e1", font=("Segoe UI", 10))
    self.visual_canvas.create_text(
      20,
      height - 22,
      text="This wave updates live while Titans operations are running.",
      anchor="w",
      fill="#94a3b8",
      font=("Segoe UI", 9),
    )

  def _draw_series_visual(self, width: int, height: int) -> None:
    chart_left = 24
    chart_top = 42
    chart_right = width - 22
    chart_bottom = height - 30

    self.visual_canvas.create_text(
      20,
      20,
      text=f"Series: {self.visual_series_name}",
      anchor="w",
      fill="#cbd5e1",
      font=("Segoe UI", 10, "bold"),
    )
    self.visual_canvas.create_rectangle(chart_left, chart_top, chart_right, chart_bottom, outline="#334155")

    if len(self.visual_series) < 2:
      self.visual_canvas.create_text(
        chart_left + 6,
        chart_top + 18,
        text="Need at least two points to animate.",
        anchor="w",
        fill="#94a3b8",
        font=("Segoe UI", 9),
      )
      return

    values = [float(v) for v in self.visual_series]
    min_v = min(values)
    max_v = max(values)
    span = max(max_v - min_v, 1e-9)

    points = []
    for idx, value in enumerate(values):
      x = chart_left + (idx / (len(values) - 1)) * (chart_right - chart_left)
      y = chart_bottom - ((value - min_v) / span) * (chart_bottom - chart_top)
      points.extend([x, y])

    self.visual_canvas.create_line(points, fill="#22d3ee", width=2, smooth=True)

    play_idx = max(0, min(self.visual_index, len(values) - 1))
    play_x = chart_left + (play_idx / (len(values) - 1)) * (chart_right - chart_left)
    play_y = chart_bottom - ((values[play_idx] - min_v) / span) * (chart_bottom - chart_top)

    self.visual_canvas.create_line(play_x, chart_top, play_x, chart_bottom, fill="#334155")
    self.visual_canvas.create_oval(play_x - 5, play_y - 5, play_x + 5, play_y + 5, fill="#f97316", outline="")

    self.visual_canvas.create_text(
      chart_left,
      chart_bottom + 12,
      text=f"t={play_idx} value={values[play_idx]:.4f}",
      anchor="w",
      fill="#cbd5e1",
      font=("Segoe UI", 9),
    )
    self.visual_canvas.create_text(
      chart_right,
      chart_top - 12,
      text=f"min={min_v:.4f} max={max_v:.4f}",
      anchor="e",
      fill="#94a3b8",
      font=("Segoe UI", 9),
    )

  def _tick_runtime(self) -> None:
    if not self.is_busy:
      self.runtime_after_id = None
      return

    elapsed = max(0.0, time.time() - self.busy_started_at)
    self.runtime_var.set(f"Runtime: {elapsed:.1f}s")
    self.runtime_phase += 0.35
    if not self.visual_series:
      self._draw_runtime_visual()

    self.runtime_after_id = self.root.after(120, self._tick_runtime)

  def _set_visual_data(self, series_name: str, series_values) -> None:
    self.visual_series_name = series_name
    self.visual_series = [float(v) for v in series_values]
    self.visual_index = 0
    self.visual_playing = False
    self.play_btn.config(text="Play")

    if self.visual_series:
      self.visual_slider.configure(to=max(1, len(self.visual_series) - 1))
      self.visual_slider.set(0)
      self.visual_subtitle_var.set("Scrub or Play to inspect the signal over time.")
    else:
      self.visual_slider.configure(to=1)
      self.visual_slider.set(0)
      self.visual_subtitle_var.set("No numeric sequence found in this result.")

    self._draw_runtime_visual()

  def _on_visual_scrub(self, value: str) -> None:
    if not self.visual_series:
      return
    self.visual_index = int(round(float(value)))
    self._draw_runtime_visual()

  def _toggle_visual_play(self) -> None:
    if not self.visual_series:
      return
    self.visual_playing = not self.visual_playing
    self.play_btn.config(text="Pause" if self.visual_playing else "Play")
    if self.visual_playing:
      self._play_visual_step()

  def _play_visual_step(self) -> None:
    if not self.visual_playing or not self.visual_series:
      return

    self.visual_index += 1
    if self.visual_index >= len(self.visual_series):
      self.visual_index = len(self.visual_series) - 1
      self.visual_playing = False
      self.play_btn.config(text="Play")

    self.visual_slider.set(self.visual_index)
    self._draw_runtime_visual()

    if self.visual_playing:
      self.root.after(180, self._play_visual_step)

  def _extract_numeric_series(self, payload: Any) -> Dict[str, list]:
    series: Dict[str, list] = {}

    def walk(node: Any, prefix: str = "") -> None:
      if isinstance(node, (int, float)):
        key = prefix or "value"
        series.setdefault(key, []).append(float(node))
        return

      if isinstance(node, list):
        if node and all(isinstance(item, (int, float)) for item in node):
          key = prefix or "values"
          series[key] = [float(item) for item in node]
          return

        if node and all(isinstance(item, dict) for item in node):
          numeric_keys = set()
          for item in node:
            for key, value in item.items():
              if isinstance(value, (int, float)):
                numeric_keys.add(key)
          for key in numeric_keys:
            values = [item[key] for item in node if isinstance(item.get(key), (int, float))]
            if values:
              name = f"{prefix}.{key}" if prefix else key
              series[name] = [float(v) for v in values]

        for idx, item in enumerate(node):
          walk(item, f"{prefix}[{idx}]" if prefix else f"[{idx}]")
        return

      if isinstance(node, dict):
        for key, value in node.items():
          next_prefix = f"{prefix}.{key}" if prefix else key
          walk(value, next_prefix)

    walk(payload)
    return {k: v for k, v in series.items() if len(v) >= 2}

  def _choose_visual_series(self, payload: Any) -> Tuple[str, list]:
    series = self._extract_numeric_series(payload)
    if not series:
      return "", []

    preferred_terms = ["strength", "score", "efficiency", "accuracy", "time", "memory", "throughput"]

    def rank(item):
      name, values = item
      score = len(values)
      lowered = name.lower()
      for idx, term in enumerate(preferred_terms):
        if term in lowered:
          score += 100 - idx * 10
      return score

    best_name, best_values = max(series.items(), key=rank)
    return best_name, best_values

  def _update_visual_from_result(self, label: str, result: Any) -> None:
    name, values = self._choose_visual_series(result)
    if values:
      self._set_visual_data(name, values)
      if label in {"Demonstration", "Collaborative Insights"}:
        self.visual_playing = True
        self.play_btn.config(text="Pause")
        self._play_visual_step()
    else:
      self._set_visual_data("", [])

  def _set_busy(self, busy: bool, message: str = "") -> None:
    self.is_busy = busy
    state = "disabled" if busy else "normal"
    for btn in [self.btn_demo, self.btn_insights, self.btn_metrics, self.btn_interact]:
      btn.config(state=state)
    self.status_var.set(message if message else ("Working..." if busy else "Ready"))

    if busy:
      self.busy_started_at = time.time()
      self.runtime_bar.start(10)
      if self.runtime_after_id is None:
        self._tick_runtime()
    else:
      self.runtime_bar.stop()
      self.runtime_var.set("Runtime: 0.0s")
      if self.runtime_after_id is not None:
        self.root.after_cancel(self.runtime_after_id)
        self.runtime_after_id = None
      self._draw_runtime_visual()

  def _run_background(self, label: str, func, *args) -> None:
    if self.is_busy:
      return

    self._set_busy(True, f"Running: {label}")

    def worker():
      try:
        result = func(*args)
        self.root.after(0, lambda: self._append_output(label, result))
        self.root.after(0, lambda: self._update_visual_from_result(label, result))
      except Exception as exc:
        self.root.after(
          0,
          lambda: self._append_output(
            f"{label} failed", f"{exc}\n{traceback.format_exc()}"
          ),
        )
      finally:
        self.root.after(0, lambda: self._set_busy(False, "Ready"))

    threading.Thread(target=worker, daemon=True).start()

  def _refresh_agent_details(self) -> None:
    name = self._get_selected_name()
    self.details_box.delete("1.0", END)
    if not name:
      self.details_box.insert(END, "No agent selected.")
      return

    if name in self.import_errors:
      self.details_box.insert(
        END,
        f"Status: Unavailable (import failure)\nReason: {self.import_errors[name]}\n",
      )
      return

    if name in self.agent_init_errors:
      self.details_box.insert(
        END,
        f"Status: Unavailable (initialization failure)\nReason: {self.agent_init_errors[name]}\n",
      )
      return

    self.details_box.insert(END, "Status: Available\n")
    agent = self.agents.get(name)
    if agent:
      try:
        metrics = agent.get_metrics()
        self.details_box.insert(END, "Current metrics:\n")
        self.details_box.insert(END, json.dumps(metrics, indent=2, default=str))
      except Exception as exc:
        self.details_box.insert(END, f"Could not load metrics: {exc}")

  def _get_available_agent(self):
    name = self._get_selected_name()
    if not name:
      raise ValueError("Select an agent first.")
    if name not in self.agents:
      reason = self.import_errors.get(name) or self.agent_init_errors.get(name) or "Unknown error"
      raise RuntimeError(f"Selected agent is unavailable: {reason}")
    return self.agents[name], name

  def _invoke_agent_method(self, method, *args):
    """Call agent methods safely regardless of sync/async implementation."""
    result = method(*args)
    if inspect.isawaitable(result):
      return asyncio.run(result)
    return result

  def _run_demonstration(self) -> None:
    def task():
      agent, name = self._get_available_agent()
      result = self._invoke_agent_method(agent.demonstrate)
      return {"agent": name, "demonstration": result}

    self._run_background("Demonstration", task)

  def _run_interaction(self) -> None:
    user_input = self.input_box.get("1.0", END).strip()
    if not user_input:
      self._append_output("Validation", "Enter a question before sending.")
      return

    def task():
      agent, name = self._get_available_agent()
      result = self._invoke_agent_method(agent.interact, user_input)
      return {"agent": name, "query": user_input, "response": result}

    self._run_background("Interaction", task)

  def _run_insights(self) -> None:
    def task():
      selected, selected_name = self._get_available_agent()
      demo_result = self._invoke_agent_method(selected.demonstrate)

      insights = []
      for name, agent in self.agents.items():
        if name == selected_name:
          continue
        try:
          insight = self._invoke_agent_method(agent.collaborate, demo_result)
          insights.append({"from_agent": name, "insight": insight})
        except Exception as exc:
          insights.append({"from_agent": name, "error": str(exc)})

      return {"selected_agent": selected_name, "insights": insights}

    self._run_background("Collaborative Insights", task)

  def _refresh_metrics(self) -> None:
    def task():
      available = {}
      for name, agent in self.agents.items():
        try:
          available[name] = agent.get_metrics()
        except Exception as exc:
          available[name] = {"error": str(exc)}

      unavailable = {
        **{name: f"Import failure: {msg}" for name, msg in self.import_errors.items()},
        **{name: f"Init failure: {msg}" for name, msg in self.agent_init_errors.items()},
      }

      return {
        "available_agent_metrics": available,
        "unavailable_agents": unavailable,
      }

    self._run_background("Metrics", task)

  def run(self) -> None:
    self.root.mainloop()


if __name__ == "__main__":
  TitansDesktopApp().run()
