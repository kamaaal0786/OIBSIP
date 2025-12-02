import tkinter as tk
from tkinter import messagebox
import random
import string

# Theme Configuration
BG_COLOR = "#ffffff"
TEXT_COLOR = "#333333"
ACCENT_COLOR = "#007bff"
BORDER_COLOR = "#cccccc"

# Strength Colors
COLORS = {
    "weak": "#ff6b6b",
    "medium": "#feca57",
    "strong": "#1dd1a1"
}

def generate_password():
    try:
        length = int(entry_length.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")
        return

    if length < 4:
        messagebox.showwarning("Warning", "Password too short (min 4 chars).")
        return
    if length > 32:
        messagebox.showinfo("Note", "That's a very long password!")

    # Build character set
    chars = ""
    if var_upper.get(): chars += string.ascii_uppercase
    if var_lower.get(): chars += string.ascii_lowercase
    if var_nums.get():  chars += string.digits
    if var_syms.get():  chars += string.punctuation

    if not chars:
        messagebox.showwarning("Error", "Select at least one option.")
        return

    # Generate and display
    pwd = "".join(random.choice(chars) for _ in range(length))
    entry_pass.delete(0, tk.END)
    entry_pass.insert(0, pwd)
    
    check_strength(length)

def copy_pass():
    text = entry_pass.get()
    if text:
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()
        lbl_status.config(text="Copied to clipboard!", fg=COLORS["strong"])
        root.after(2000, lambda: lbl_status.config(text=""))
    else:
        messagebox.showinfo("Empty", "Nothing to copy.")

def check_strength(length):
    # Calculate score based on length and variety
    score = 0
    if length >= 8: score += 1
    if length >= 12: score += 1
    if var_upper.get(): score += 1
    if var_lower.get(): score += 1
    if var_nums.get(): score += 1
    if var_syms.get(): score += 1

    # Update meter UI
    if score < 3:
        strength_bar.config(bg=COLORS["weak"])
        lbl_strength.config(text="Weak", fg=COLORS["weak"])
    elif score < 5:
        strength_bar.config(bg=COLORS["medium"])
        lbl_strength.config(text="Moderate", fg=COLORS["medium"])
    else:
        strength_bar.config(bg=COLORS["strong"])
        lbl_strength.config(text="Strong", fg=COLORS["strong"])

# --- Main App Setup ---
root = tk.Tk()
root.title("PassGen Tool")
root.geometry("400x550")
root.resizable(False, False)
root.config(padx=25, pady=25, bg=BG_COLOR)

# Title
tk.Label(root, text="Password Generator", font=("Helvetica", 18, "bold"), 
         bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(0, 25))

# Options Section
frame_opts = tk.Frame(root, bg=BG_COLOR, highlightbackground=BORDER_COLOR, 
                      highlightthickness=1, padx=15, pady=15)
frame_opts.pack(fill="x", pady=5)

# Length Input
frame_len = tk.Frame(frame_opts, bg=BG_COLOR)
frame_len.pack(pady=(0, 15), anchor="w")
tk.Label(frame_len, text="Password Length:", font=("Helvetica", 10), 
         bg=BG_COLOR, fg=TEXT_COLOR).pack(side="left", padx=(0, 10))

entry_length = tk.Entry(frame_len, width=5, font=("Helvetica", 10), bd=1, relief="solid")
entry_length.insert(0, "12")
entry_length.pack(side="left")

# Variables
var_upper = tk.IntVar(value=1)
var_lower = tk.IntVar(value=1)
var_nums = tk.IntVar(value=1)
var_syms = tk.IntVar(value=0)

# Checkboxes (Loop for cleaner code)
options = [
    ("Include Uppercase (A-Z)", var_upper),
    ("Include Lowercase (a-z)", var_lower),
    ("Include Numbers (0-9)", var_nums),
    ("Include Symbols (!@#$)", var_syms)
]

for text, var in options:
    tk.Checkbutton(frame_opts, text=text, variable=var, font=("Helvetica", 10),
                   bg=BG_COLOR, fg=TEXT_COLOR, activebackground=BG_COLOR, selectcolor=BG_COLOR,
                   bd=0, highlightthickness=0).pack(anchor="w", pady=2)

# Generate Button
tk.Button(root, text="Generate Password", font=("Helvetica", 10), 
          bg=ACCENT_COLOR, fg="white", activebackground="#0056b3", activeforeground="white",
          bd=0, padx=10, pady=5, cursor="hand2", command=generate_password).pack(pady=20, fill="x")

# Password Output
entry_pass = tk.Entry(root, font=("Courier New", 14), justify="center", 
                      bd=1, relief="solid", fg=TEXT_COLOR)
entry_pass.pack(pady=5, fill="x", ipady=5)

# Copy Button
tk.Button(root, text="Copy to Clipboard", font=("Helvetica", 10), 
          bg="#f0f0f0", fg=TEXT_COLOR, activebackground="#e0e0e0",
          bd=0, padx=10, pady=5, cursor="hand2", command=copy_pass).pack(pady=10, fill="x")

# Status Message
lbl_status = tk.Label(root, text="", font=("Helvetica", 9), bg=BG_COLOR, fg=COLORS["strong"])
lbl_status.pack()

# Strength Meter
frame_str = tk.Frame(root, bg=BG_COLOR)
frame_str.pack(pady=15, fill="x")

tk.Label(frame_str, text="Strength:", font=("Helvetica", 10), 
         bg=BG_COLOR, fg=TEXT_COLOR).pack(side="left")

strength_bar = tk.Frame(frame_str, width=100, height=8, bg=BORDER_COLOR)
strength_bar.pack(side="left", padx=15)
strength_bar.pack_propagate(False)

lbl_strength = tk.Label(frame_str, text="---", font=("Helvetica", 10, "bold"), 
                        bg=BG_COLOR, fg=TEXT_COLOR)
lbl_strength.pack(side="left")

root.mainloop()