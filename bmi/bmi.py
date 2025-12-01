import tkinter as tk
from tkinter import ttk, messagebox

APP_TITLE = "Simple BMI"


BMI_RANGES = [
    (0, 18.5, "Underweight", "#9ecae1"),
    (18.5, 24.9, "Normal", "#a1d99b"),
    (25.0, 29.9, "Overweight", "#fdd0a2"),
    (30.0, 100.0, "Obesity", "#f08a8a"),
]

def calc_bmi_metric(kg: float, meters: float) -> float:
    if meters <= 0:
        raise ValueError("Height must be greater than zero.")
    return round(kg / (meters ** 2), 2)

def calc_bmi_imperial(lb: float, inches: float) -> float:
    kg = lb * 0.45359237
    meters = inches * 0.0254
    return calc_bmi_metric(kg, meters)

def get_bmi_label(bmi: float):
    for low, high, label, color in BMI_RANGES:
        if low <= bmi <= high:
            return label, color
    return "Unknown", "#cccccc"

def metric_ok(weight_kg, height_m):
    return (20 <= weight_kg <= 300) and (0.9 <= height_m <= 2.5)

def imperial_ok(weight_lb, height_in):
    return (44 <= weight_lb <= 660) and (35 <= height_in <= 98)

class BMIApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("680x420")
        self.resizable(False, False)
        self.configure(padx=12, pady=12)
        self._build_ui()

    def _build_ui(self):
        # Unit selection and screenshot hint
        top = ttk.Frame(self)
        top.pack(fill="x", pady=(0,8))

        self.unit_var = tk.StringVar(value="metric")
        ttk.Radiobutton(top, text="Metric (kg, m or cm)", variable=self.unit_var, value="metric",
                        command=self._on_unit_change).pack(side="left", padx=(0,8))
        ttk.Radiobutton(top, text="Imperial (lb, in)", variable=self.unit_var, value="imperial",
                        command=self._on_unit_change).pack(side="left")


        # Inputs
        mid = ttk.Frame(self)
        mid.pack(fill="x", pady=(0,8))

        ttk.Label(mid, text="Name:").grid(row=0, column=0, sticky="w")
        self.name_var = tk.StringVar(value="guest")
        ttk.Entry(mid, textvariable=self.name_var, width=18).grid(row=0, column=1, sticky="w")

        ttk.Label(mid, text="Weight:").grid(row=1, column=0, sticky="w", pady=(8,0))
        self.weight_var = tk.StringVar()
        w_entry = ttk.Entry(mid, textvariable=self.weight_var, width=18)
        w_entry.grid(row=1, column=1, sticky="w", pady=(8,0))
        self.weight_hint = ttk.Label(mid, text="(kg)", foreground="#666")
        self.weight_hint.grid(row=1, column=2, sticky="w", padx=(6,0), pady=(8,0))

        ttk.Label(mid, text="Height:").grid(row=2, column=0, sticky="w", pady=(8,0))
        self.height_var = tk.StringVar()
        h_entry = ttk.Entry(mid, textvariable=self.height_var, width=18)
        h_entry.grid(row=2, column=1, sticky="w", pady=(8,0))
        self.height_hint = ttk.Label(mid, text="(m or cm)", foreground="#666")
        self.height_hint.grid(row=2, column=2, sticky="w", padx=(6,0), pady=(8,0))

        # Buttons
        btn_frame = ttk.Frame(mid)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=(12,0))
        ttk.Button(btn_frame, text="Calculate BMI", command=self._on_calculate).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Reset", command=self._reset).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Quit", command=self.quit).pack(side="left", padx=6)

        # Results and scale canvas
        right = ttk.Frame(self)
        right.pack(fill="both", expand=True)

        result_box = ttk.Frame(right)
        result_box.pack(side="top", fill="x", pady=(6,12))
        self.result_var = tk.StringVar(value="Enter values and press Calculate")
        ttk.Label(result_box, textvariable=self.result_var, font=("TkDefaultFont", 12, "bold")).pack(anchor="w")

        self.detail_var = tk.StringVar(value="")
        ttk.Label(result_box, textvariable=self.detail_var, foreground="#333").pack(anchor="w", pady=(6,0))

        canvas_frame = ttk.Frame(right)
        canvas_frame.pack(fill="both", expand=True)
        self.scale_canvas = tk.Canvas(canvas_frame, width=560, height=160, bg="#f7f7f7", highlightthickness=0)
        self.scale_canvas.pack(pady=(6,0))

        # draw static scale and focus weight entry
        self._draw_scale()
        w_entry.focus_set()

        # Enter key triggers calculate
        self.bind("<Return>", lambda e: self._on_calculate())

    def _on_unit_change(self):
        if self.unit_var.get() == "metric":
            self.weight_hint.config(text="(kg)")
            self.height_hint.config(text="(m or cm)")
        else:
            self.weight_hint.config(text="(lb)")
            self.height_hint.config(text="(in)")

    def _on_calculate(self):
        unit = self.unit_var.get()
        name = self.name_var.get().strip() or "guest"
        try:
            w_text = self.weight_var.get().strip()
            h_text = self.height_var.get().strip()
            if not w_text or not h_text:
                raise ValueError("Please enter both weight and height.")

            if unit == "metric":
                weight = float(w_text)
                h_val = float(h_text)
                height_m = h_val / 100.0 if h_val >= 50 else h_val
                if not metric_ok(weight, height_m):
                    raise ValueError("Metric ranges: weight 20–300 kg, height 0.9–2.5 m.")
                bmi = calc_bmi_metric(weight, height_m)
            else:
                weight_lb = float(w_text)
                height_in = float(h_text)
                if not imperial_ok(weight_lb, height_in):
                    raise ValueError("Imperial ranges: weight 44–660 lb, height 35–98 in.")
                bmi = calc_bmi_imperial(weight_lb, height_in)

            label, color = get_bmi_label(bmi)
            self.result_var.set(f"{name} — BMI: {bmi} ({label})")
            self.detail_var.set(self._detail_for(bmi))
            self._place_marker(bmi, color)
        except ValueError as e:
            messagebox.showerror("Input error", str(e))
        except Exception:
            messagebox.showerror("Input error", "Please enter valid numeric values for weight and height.")

    def _reset(self):
        self.weight_var.set("")
        self.height_var.set("")
        self.result_var.set("Enter values and press Calculate")
        self.detail_var.set("")
        self._draw_scale()

    def _detail_for(self, bmi: float) -> str:
        label, _ = get_bmi_label(bmi)
        if label == "Underweight":
            return "Tip: Balanced calorie surplus and strength training can help."
        if label == "Normal":
            return "Tip: Keep up balanced diet and regular activity."
        if label == "Overweight":
            return "Tip: Mild calorie deficit plus activity recommended."
        if label == "Obesity":
            return "Tip: Consider consulting a healthcare professional."
        return ""

    # Canvas helpers
    def _draw_scale(self):
        c = self.scale_canvas
        c.delete("all")
        width = 520
        height = 80
        left = 20
        top = 30
        total_span = 50.0
        x = left
        for low, high, label, color in BMI_RANGES:
            seg_low = max(low, 0)
            seg_high = min(high, total_span)
            seg_width = (seg_high - seg_low) / total_span * width
            if seg_width > 0:
                c.create_rectangle(x, top, x + seg_width, top + height, fill=color, outline="#ddd")
                if seg_width > 60:
                    c.create_text(x + seg_width/2, top + height/2, text=label, fill="#222")
                x += seg_width
        c.create_line(left, top + height + 6, left + width, top + height + 6, fill="#888")
        c.create_text(left, top + height + 18, text="BMI 0", anchor="w", fill="#444")
        c.create_text(left + width, top + height + 18, text="BMI 50+", anchor="e", fill="#444")
        self.marker = c.create_line(left, top - 6, left, top + height + 12, fill="#333", width=2)
        self.marker_label = c.create_text(left, top - 14, text="", anchor="s", fill="#111", font=("TkDefaultFont", 10, "bold"))

    def _place_marker(self, bmi: float, color: str):
        c = self.scale_canvas
        width = 520
        left = 20
        total_span = 50.0
        display_bmi = max(0.0, min(bmi, total_span))
        x_pos = left + (display_bmi / total_span) * width
        c.coords(self.marker, x_pos, 24, x_pos, 30 + 80 + 12)
        c.itemconfigure(self.marker, fill="#000")
        c.itemconfigure(self.marker_label, text=f"{bmi}", fill="#000")
        c.coords(self.marker_label, x_pos, 18)
        if hasattr(self, "_marker_circle_id"):
            try:
                c.delete(self._marker_circle_id)
            except Exception:
                pass
        self._marker_circle_id = c.create_oval(x_pos-6, 24+40-6, x_pos+6, 24+40+6, fill=color, outline="#444")

if __name__ == "__main__":
    app = BMIApp()
    app.mainloop()
