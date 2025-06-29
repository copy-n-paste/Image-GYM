import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageEnhance
import os
import io

STANDARD_MIN_SIZE_KB = 100  # Minimum size allowed for compression

def load_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
    if file_path:
        app.image_path = file_path
        messagebox.showinfo("Image Loaded", f"Loaded:\n{os.path.basename(file_path)}")

def shorten_image():
    if not hasattr(app, 'image_path'):
        messagebox.showerror("Error", "No image loaded.")
        return

    try:
        target_kb = int(size_entry.get())
        if target_kb < STANDARD_MIN_SIZE_KB:
            messagebox.showerror("Too Small", f"Minimum allowed size is {STANDARD_MIN_SIZE_KB} KB.")
            return
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid size in KB.")
        return

    img = Image.open(app.image_path)
    quality = 95
    while quality > 10:
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=quality)
        size_kb = len(buffer.getvalue()) // 1024
        if size_kb <= target_kb:
            break
        quality -= 5

    filename = os.path.basename(app.image_path)
    new_path = f"shortened_{filename}"
    img.save(new_path, quality=quality)
    messagebox.showinfo("Done", f"Compressed to ~{size_kb} KB\nSaved as: {new_path}")

def enhance_image():
    if not hasattr(app, 'image_path'):
        messagebox.showerror("Error", "No image loaded.")
        return

    img = Image.open(app.image_path)
    sharpener = ImageEnhance.Sharpness(img)
    brightener = ImageEnhance.Brightness(sharpener.enhance(2.0))
    enhanced_img = brightener.enhance(1.2)

    filename = os.path.basename(app.image_path)
    new_path = f"enhanced_{filename}"
    enhanced_img.save(new_path)
    messagebox.showinfo("Done", f"Enhanced image saved as:\n{new_path}")

# GUI setup
app = tk.Tk()
app.title("Image Shorten & Enhance Tool")
app.geometry("350x250")

tk.Button(app, text="📂 Load Image", command=load_image, width=30).pack(pady=10)

tk.Label(app, text="Enter target size in KB (min 100 KB):").pack()
size_entry = tk.Entry(app)
size_entry.pack(pady=5)

tk.Button(app, text="🔽 Shorten Image", command=shorten_image, width=30).pack(pady=5)
tk.Button(app, text="✨ Enhance Image", command=enhance_image, width=30).pack(pady=5)

app.mainloop()
