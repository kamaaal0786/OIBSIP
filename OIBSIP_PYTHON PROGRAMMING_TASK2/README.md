# **⚖️ Simple BMI Calculator**

A streamlined, user-friendly desktop application for calculating Body Mass Index built with Python.

I created this project to explore **GUI Development** and **Data Visualization** using Tkinter. Unlike basic command-line calculators, this tool features a dynamic graphical interface with a visual scale to provide immediate, clear feedback on health metrics.

## **🚀 Key Features**

* **Dual Unit Support:** Seamlessly switch between **Metric** (kg, meters/cm) and **Imperial** (lb, inches) systems.  
* **Visual Health Scale:** A custom-drawn color-coded bar that visually indicates where the calculated BMI falls (Underweight, Normal, Overweight, Obesity).  
* **Smart Validation:** logic that prevents calculation errors by enforcing realistic height and weight ranges.  
* **Actionable Feedback:** Provides context-aware health tips based on the specific BMI category.  
* **Interactive UI:** Built with tkinter.ttk for a clean, modern look, featuring a dynamic marker that moves along the scale.

## **🛠️ Tech Stack**

* **Language:** Python 3.x  
* **Interface:** Tkinter (Standard Library)  
* **Graphics:** Tkinter Canvas (used for the custom BMI scale rendering)

## **💻 How to Run This Project**

1. **Clone the repository** or download the files.  
2. **Install dependencies:** This project uses Python's standard libraries, so **no external installation is required**.  
   *Note: Just ensure you have Python installed on your system.*  
3. **Run the app:** python bmi.py

## **📂 Project Structure**

* bmi.py \- The main entry point. Contains the GUI setup, calculation logic, and custom canvas drawing code.  
* README.md \- Documentation.

## **🔮 Future Improvements**

If I continue working on this, I plan to add:

* **History Tracking:** Saving previous calculations to a local JSON or CSV file to track progress.  
* **User Profiles:** Support for multiple users to save their specific stats.  
* **Trend Analysis:** Using matplotlib to graph weight changes over time.

*Built for my Internship Portfolio.*