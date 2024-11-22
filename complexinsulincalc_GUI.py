import tkinter as tk
from tkinter import messagebox

# Constants for blood sugar correction
BLOOD_SUGAR_MIN = 4
BLOOD_SUGAR_MIN_CORRECTION = -1
BLOOD_SUGAR_MAX = 7
BLOOD_SUGAR_MAX_CORRECTION = 1

# Dosage ratios
DOSAGE_RATIO = {
    'breakfast': 2,
    'lunch': 1.5,
    'dinner': 1.5,
    'snack': 1.5,
}

def calculate_dose():
    try:
        # Get values from GUI inputs
        dose_type = dose_type_var.get()
        carbs = float(carbs_entry.get())
        ninety_mins = ninety_mins_var.get()
        blood_sugar_level = float(blood_sugar_entry.get())
        
        # Validate dose type
        if dose_type not in DOSAGE_RATIO:
            messagebox.showerror("Error", "Invalid dose type selected.")
            return
        
        ratio = DOSAGE_RATIO[dose_type]
        dose = ratio * carbs / 10
        
        if ninety_mins == "Yes":
            result_label.config(text=f"You need {dose:.1f} units of insulin (90-min adjustment).")
            return
        
        # Blood sugar correction logic
        multiplier = 0
        limit = 0
        
        if blood_sugar_level > BLOOD_SUGAR_MAX:
            multiplier = BLOOD_SUGAR_MAX_CORRECTION
            limit = BLOOD_SUGAR_MAX
        elif blood_sugar_level < BLOOD_SUGAR_MIN:
            multiplier = BLOOD_SUGAR_MIN_CORRECTION
            limit = BLOOD_SUGAR_MIN
        
        cordiff = blood_sugar_level - limit
        correction = cordiff * multiplier
        total_dose = round(dose + correction)
        
        result_label.config(text=f"You need {total_dose:.1f} units of insulin.")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric inputs.")

def clear_inputs():
    """Clear all input fields and the result label."""
    dose_type_var.set("breakfast")
    carbs_entry.delete(0, tk.END)
    ninety_mins_var.set("No")
    blood_sugar_entry.delete(0, tk.END)
    result_label.config(text="")

# Create the main window
root = tk.Tk()
root.title("Insulin Dose Calculator")

# Dose type
tk.Label(root, text="Type of dose:").grid(row=0, column=0, sticky="w")
dose_type_var = tk.StringVar(value="breakfast")
tk.OptionMenu(root, dose_type_var, *DOSAGE_RATIO.keys()).grid(row=0, column=1, sticky="w")

# Carbs input
tk.Label(root, text="Carbs (grams):").grid(row=1, column=0, sticky="w")
carbs_entry = tk.Entry(root)
carbs_entry.grid(row=1, column=1)

# 90-minute question
tk.Label(root, text="Insulin in last 90 mins?").grid(row=2, column=0, sticky="w")
ninety_mins_var = tk.StringVar(value="No")
tk.OptionMenu(root, ninety_mins_var, "Yes", "No").grid(row=2, column=1, sticky="w")

# Blood sugar level input
tk.Label(root, text="Current blood sugar level:").grid(row=3, column=0, sticky="w")
blood_sugar_entry = tk.Entry(root)
blood_sugar_entry.grid(row=3, column=1)

# Calculate button
calculate_button = tk.Button(root, text="Calculate", command=calculate_dose)
calculate_button.grid(row=4, column=0, pady=10)

# Clear button
clear_button = tk.Button(root, text="Clear", command=clear_inputs)
clear_button.grid(row=4, column=1, pady=10)

# Result label
result_label = tk.Label(root, text="", fg="blue")
result_label.grid(row=5, column=0, columnspan=2)

# Start the GUI event loop
root.mainloop()
