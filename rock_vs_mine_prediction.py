import tkinter as tk
from tkinter import messagebox, filedialog
import numpy as np

# Function to load input data from a file
def load_input_data():
    # Open a dialog for the user to select the input file
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt")])
    
    if file_path:
        with open(file_path, 'r') as file:
            input_data = file.read().split(',')  # Split values by commas (for CSV or TXT)
            # Convert to float, ignoring non-numeric values
            input_data = []
            for item in input_data:
                try:
                    input_data.append(float(item.strip()))  # Convert to float after stripping whitespace
                except ValueError:
                    continue  # Ignore any items that cannot be converted to float
            
            # Check if we have enough values to fill the inputs
            if len(input_data) < 60:
                messagebox.showerror("Input Error", "Not enough valid data points. Please ensure the file contains at least 60 numeric values.")
                return
            
            # Fill the input fields with the first 60 valid values
            for i in range(60):
                inputs[i].delete(0, tk.END)  # Clear existing content
                inputs[i].insert(0, input_data[i])  # Insert new value

# Function to predict Rock or Mine based on user input
def predict_result():
    try:
        # Collect user input, ensure all inputs are floats
        input_data = [float(entry.get()) for entry in inputs]
        input_data_np = np.array(input_data).reshape(1, -1)  # Converting to numpy array
        
        # Use the model to predict (Make sure model.predict returns 'R' for Rock and 'M' for Mine)
        prediction = model.predict(input_data_np)[0]  # Get the first prediction result

        # Update the GUI background based on prediction result
        if prediction == 'R':  # 'R' stands for Rock
            result_label.config(text="It's a Rock!", bg="blue", fg="white")
        else:  # 'M' stands for Mine
            result_label.config(text="It's a Mine!", bg="red", fg="white")
    
    except ValueError:
        # If invalid input is provided (non-numeric data)
        messagebox.showerror("Invalid input", "Please enter valid numeric data for all fields.")

# GUI Setup
root = tk.Tk()
root.title("Sonar Rock vs Mine Prediction")
root.geometry("600x400")
root.configure(bg="#2c3e50")  # Stylish dark background

# Title label
title_label = tk.Label(root, text="Sonar Rock vs Mine Predictor", font=("Helvetica", 24, "bold"), bg="#2c3e50", fg="white")
title_label.pack(pady=20)

# Frame to hold the input fields
input_frame = tk.Frame(root, bg="#2c3e50")
input_frame.pack(pady=20)

# Input fields for user to enter sonar feature values
inputs = []
for i in range(60):  # Assuming 60 features as in your Sonar dataset
    entry = tk.Entry(input_frame, width=10, font=("Arial", 12), bg="#34495e", fg="white", borderwidth=2, relief="groove")
    entry.grid(row=i // 10, column=i % 10, padx=5, pady=5)  # Arranging in 6 rows of 10 inputs each
    inputs.append(entry)

# Button to load input data from a file
load_button = tk.Button(root, text="Load Input Data", command=load_input_data, font=("Arial", 14), bg="#3498db", fg="white", borderwidth=0)
load_button.pack(pady=10)

# Button to trigger the prediction
predict_button = tk.Button(root, text="Predict", command=predict_result, font=("Arial", 16), bg="#1abc9c", fg="white", borderwidth=0)
predict_button.pack(pady=20)

# Label to display the result (whether it's Rock or Mine)
result_label = tk.Label(root, text="", font=("Arial", 18, "bold"), width=30, height=2, bg="#2c3e50", fg="white")
result_label.pack(pady=20)

# Run the GUI main loop
root.mainloop()
