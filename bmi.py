

import tkinter as tk
from tkinter import ttk, messagebox

APP_TITLE = "Simple BMI"


# Basic BMI ranges and labels (easy to explain in your report)
BMI_RANGES = [
    (0, 18.5, "Underweight", "#9ecae1"),
    (18.5, 24.9, "Normal", "#a1d99b"),
    (25.0, 29.9, "Overweight", "#fdd0a2"),
    (30.0, 100.0, "Obesity", "#f08a8a"),
]

def calculate_bmi_metric(weight_kg: float, height_m: float) -> float:
    if height_m <= 0:
        raise ValueError("Height must be greater than zero.")
    return round(weight_kg / (height_m ** 2), 2)

def calculate_bmi_imperial(weight_lb: float, height_in: float) -> float:
    # convert to metric and reuse formula
    kg = weight_lb * 0.45359237
    m = height_in * 0.0254
    return calculate_bmi_metric(kg, m)

def classify_bmi(bmi: float):
    for low, high, label, color in BMI_RANGES:
        if low <= bmi <= high:
            return label, color
    return "Unknown", "#cccccc"

def parse_height_input(val: str) -> float:
    # Accepts decimals. Caller decides whether it's meters, cm or inches, based on units.
    return float(val.strip())

def reasonable_metric_ranges(weight_kg, height_m):
    return (20 <= weight_kg <= 300) and (0.9 <= height_m <= 2.5)

def reasonable_imperial_ranges(weight_lb, height_in):
    return (44 <= weight_lb <= 660) and (35 <= height_in <= 98)  # approx 0.9m->35in, 2.5m->98in

class BMIApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("680x420")
        self.resizable(False, False)
        self.configure(padx=12, pady=12)
        self.create_widgets()

    def create_widgets(self):
        # Top: unit selection and screenshot hint
        topframe = ttk.Frame(self)
        topframe.pack(fill="x", pady=(0,8))

        self.unit_var = tk.StringVar(value="metric")
        ttk.Radiobutton(topframe, text="Metric (kg, m or cm)", variable=self.unit_var, value="metric",
                        command=self.on_unit_change).pack(side="left", padx=(0,8))
        ttk.Radiobutton(topframe, text="Imperial (lb, in)", variable=self.unit_var, value="imperial",
                        command=self.on_unit_change).pack(side="left")

        
       

        # Middle: inputs
        mid = ttk.Frame(self)
        mid.pack(fill="x", pady=(0,8))

        # Username (purely cosmetic)
        ttk.Label(mid, text="Name:").grid(row=0, column=0, sticky="w")
        self.name_var = tk.StringVar(value="guest")
        ttk.Entry(mid, textvariable=self.name_var, width=18).grid(row=0, column=1, sticky="w")

        # Weight
        ttk.Label(mid, text="Weight:").grid(row=1, column=0, sticky="w", pady=(8,0))
        self.weight_var = tk.StringVar()
        ttk.Entry(mid, textvariable=self.weight_var, width=18).grid(row=1, column=1, sticky="w", pady=(8,0))
        self.weight_hint = ttk.Label(mid, text="(kg)", foreground="#666")
        self.weight_hint.grid(row=1, column=2, sticky="w", padx=(6,0), pady=(8,0))

        # Height
        ttk.Label(mid, text="Height:").grid(row=2, column=0, sticky="w", pady=(8,0))
        self.height_var = tk.StringVar()
        ttk.Entry(mid, textvariable=self.height_var, width=18).grid(row=2, column=1, sticky="w", pady=(8,0))
        self.height_hint = ttk.Label(mid, text="(m or cm)", foreground="#666")
        self.height_hint.grid(row=2, column=2, sticky="w", padx=(6,0), pady=(8,0))

        # Buttons
        btn_frame = ttk.Frame(mid)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=(12,0))
        ttk.Button(btn_frame, text="Calculate BMI", command=self.on_calculate).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Reset", command=self.reset).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Quit", command=self.quit).pack(side="left", padx=6)

        # Right side: result & scale
        right = ttk.Frame(self)
        right.pack(fill="both", expand=True)

        result_box = ttk.Frame(right)
        result_box.pack(side="top", fill="x", pady=(6,12))
        self.result_var = tk.StringVar(value="Enter values and press Calculate")
        self.result_label = ttk.Label(result_box, textvariable=self.result_var, font=("TkDefaultFont", 12, "bold"))
        self.result_label.pack(anchor="w")

        self.detail_var = tk.StringVar(value="")
        ttk.Label(result_box, textvariable=self.detail_var, foreground="#333").pack(anchor="w", pady=(6,0))

        # Canvas for BMI scale
        canvas_frame = ttk.Frame(right)
        canvas_frame.pack(fill="both", expand=True)
        self.scale_canvas = tk.Canvas(canvas_frame, width=560, height=160, bg="#f7f7f7", highlightthickness=0)
        self.scale_canvas.pack(pady=(6,0))

        # draw static scale background
        self.draw_bmi_scale()

    def on_unit_change(self):
        unit = self.unit_var.get()
        if unit == "metric":
            self.weight_hint.config(text="(kg)")
            self.height_hint.config(text="(m or cm)")
        else:
            self.weight_hint.config(text="(lb)")
            self.height_hint.config(text="(in)")

    def on_calculate(self):
        unit = self.unit_var.get()
        name = self.name_var.get().strip() or "guest"
        try:
            w_raw = self.weight_var.get().strip()
            h_raw = self.height_var.get().strip()
            if not w_raw or not h_raw:
                raise ValueError("Please enter both weight and height.")

            weight = float(w_raw)
            # Height parsing: if metric and value >= 50 treat as cm
            if unit == "metric":
                # allow values like 175 or 1.75
                h_val = float(h_raw)
                height_m = h_val/100.0 if h_val >= 50 else h_val
                if not reasonable_metric_ranges(weight, height_m):
                    raise ValueError("Metric ranges: weight 20–300 kg, height 0.9–2.5 m.")
                bmi = calculate_bmi_metric(weight, height_m)
            else:
                # imperial: weight in lb, height in inches
                weight_lb = float(w_raw)
                height_in = float(h_raw)
                if not reasonable_imperial_ranges(weight_lb, height_in):
                    raise ValueError("Imperial ranges: weight 44–660 lb, height 35–98 in.")
                bmi = calculate_bmi_imperial(weight_lb, height_in)

            label, color = classify_bmi(bmi)
            self.result_var.set(f"{name} — BMI: {bmi} ({label})")
            self.detail_var.set(self.make_detail_text(bmi))
            self.update_scale_marker(bmi, color)
        except ValueError as e:
            messagebox.showerror("Input error", str(e))
        except Exception:
            messagebox.showerror("Input error", "Please enter valid numeric values for weight and height.")

    def reset(self):
        self.weight_var.set("")
        self.height_var.set("")
        self.result_var.set("Enter values and press Calculate")
        self.detail_var.set("")
        self.draw_bmi_scale()  # reset marker

    def make_detail_text(self, bmi: float) -> str:
        # Small helpful tips depending on BMI
        label, _ = classify_bmi(bmi)
        if label == "Underweight":
            return "Tip: Consider a balanced calorie surplus and strength training."
        if label == "Normal":
            return "Tip: Maintain with balanced diet and regular exercise."
        if label == "Overweight":
            return "Tip: Try mild calorie deficit and increased activity."
        if label == "Obesity":
            return "Tip: Consult a healthcare provider for a plan."
        return ""

    # ---------- Canvas drawing ----------
    def draw_bmi_scale(self):
        c = self.scale_canvas
        c.delete("all")
        width = 520
        height = 80
        left = 20
        top = 30
        right = left + width
        # Draw labelled segments using BMI_RANGES
        total_span = 50.0  # we'll map BMI 0..50 across the bar
        x = left
        for low, high, label, color in BMI_RANGES:
            seg_low = max(low, 0)
            seg_high = min(high, total_span)
            seg_width = (seg_high - seg_low) / total_span * width
            if seg_width > 0:
                c.create_rectangle(x, top, x + seg_width, top + height, fill=color, outline="#ddd")
                # put label centered in the segment if wide enough
                if seg_width > 60:
                    c.create_text(x + seg_width/2, top + height/2, text=label, fill="#222")
                x += seg_width

        # baseline
        c.create_line(left, top + height + 6, right, top + height + 6, fill="#888")
        c.create_text(left, top + height + 18, text="BMI 0", anchor="w", fill="#444")
        c.create_text(right, top + height + 18, text="BMI 50+", anchor="e", fill="#444")

        # initial marker (hidden until calculate)
        self.marker = c.create_line(left, top - 6, left, top + height + 12, fill="#333", width=2)
        self.marker_label = c.create_text(left, top - 14, text="", anchor="s", fill="#111", font=("TkDefaultFont", 10, "bold"))

    def update_scale_marker(self, bmi: float, color: str):
        c = self.scale_canvas
        width = 520
        left = 20
        total_span = 50.0
        # clamp BMI for display
        display_bmi = max(0.0, min(bmi, total_span))
        x_pos = left + (display_bmi / total_span) * width
        # move marker
        c.coords(self.marker, x_pos, 24, x_pos, 30 + 80 + 12)
        c.itemconfigure(self.marker, fill="#000")
        c.itemconfigure(self.marker_label, text=f"{bmi}", fill="#000")
        c.coords(self.marker_label, x_pos, 18)
        # subtle highlight: draw small circle at marker
        # remove old circle if any
        if hasattr(self, "_marker_circle_id"):
            try:
                c.delete(self._marker_circle_id)
            except Exception:
                pass
        self._marker_circle_id = c.create_oval(x_pos-6, 24+40-6, x_pos+6, 24+40+6, fill=color, outline="#444")

if __name__ == "__main__":
    app = BMIApp()
    app.mainloop()
