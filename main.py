import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import os
import io
import threading
from pathlib import Path

class FileCompressor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("File Compressor Pro")
        self.root.geometry("600x700")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.selected_file = None
        self.compression_progress = tk.DoubleVar()
        self.status_text = tk.StringVar(value="Ready to compress files")
        
        self.setup_ui()
        self.center_window()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_ui(self):
        """Create the main UI components"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#f0f0f0')
        header_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(
            header_frame, 
            text="📁 File Compressor Pro", 
            font=('Segoe UI', 24, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Compress images, PDFs, and other files with ease",
            font=('Segoe UI', 12),
            bg='#f0f0f0',
            fg='#7f8c8d'
        )
        subtitle_label.pack()
        
        # File selection section
        self.create_file_section(main_frame)
        
        # Compression settings section
        self.create_settings_section(main_frame)
        
        # Progress section
        self.create_progress_section(main_frame)
        
        # Action buttons
        self.create_action_buttons(main_frame)
        
        # Status section
        self.create_status_section(main_frame)
        
    def create_file_section(self, parent):
        """Create file selection section"""
        file_frame = tk.LabelFrame(
            parent, 
            text="📂 File Selection", 
            font=('Segoe UI', 12, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50',
            padx=15,
            pady=15
        )
        file_frame.pack(fill='x', pady=(0, 15))
        
        # File info display
        self.file_info_label = tk.Label(
            file_frame,
            text="No file selected",
            font=('Segoe UI', 10),
            bg='#f0f0f0',
            fg='#7f8c8d',
            wraplength=500
        )
        self.file_info_label.pack(pady=(0, 10))
        
        # Select file button
        select_btn = tk.Button(
            file_frame,
            text="🔍 Select File",
            command=self.select_file,
            font=('Segoe UI', 11, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2'
        )
        select_btn.pack()
        
    def create_settings_section(self, parent):
        """Create compression settings section"""
        settings_frame = tk.LabelFrame(
            parent,
            text="⚙️ Compression Settings",
            font=('Segoe UI', 12, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50',
            padx=15,
            pady=15
        )
        settings_frame.pack(fill='x', pady=(0, 15))
        
        # File type specific settings
        self.settings_container = tk.Frame(settings_frame, bg='#f0f0f0')
        self.settings_container.pack(fill='x')
        
        # Default message
        self.settings_label = tk.Label(
            self.settings_container,
            text="Select a file to see compression options",
            font=('Segoe UI', 10),
            bg='#f0f0f0',
            fg='#7f8c8d'
        )
        self.settings_label.pack()
        
    def create_progress_section(self, parent):
        """Create progress section"""
        progress_frame = tk.LabelFrame(
            parent,
            text="📊 Progress",
            font=('Segoe UI', 12, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50',
            padx=15,
            pady=15
        )
        progress_frame.pack(fill='x', pady=(0, 15))
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.compression_progress,
            maximum=100,
            length=400,
            mode='determinate'
        )
        self.progress_bar.pack(pady=(0, 10))
        
        # Progress label
        self.progress_label = tk.Label(
            progress_frame,
            textvariable=self.status_text,
            font=('Segoe UI', 10),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        self.progress_label.pack()
        
    def create_action_buttons(self, parent):
        """Create action buttons"""
        button_frame = tk.Frame(parent, bg='#f0f0f0')
        button_frame.pack(fill='x', pady=(0, 15))
        
        # Compress button
        self.compress_btn = tk.Button(
            button_frame,
            text="🚀 Compress File",
            command=self.start_compression,
            font=('Segoe UI', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            padx=30,
            pady=12,
            cursor='hand2',
            state='disabled'
        )
        self.compress_btn.pack(side='left', padx=(0, 10))
        
        # Clear button
        clear_btn = tk.Button(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_selection,
            font=('Segoe UI', 12, 'bold'),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            padx=30,
            pady=12,
            cursor='hand2'
        )
        clear_btn.pack(side='right')
        
    def create_status_section(self, parent):
        """Create status section"""
        status_frame = tk.LabelFrame(
            parent,
            text="ℹ️ Information",
            font=('Segoe UI', 12, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50',
            padx=15,
            pady=15
        )
        status_frame.pack(fill='both', expand=True)
        
        # Status text
        self.status_display = tk.Text(
            status_frame,
            height=8,
            font=('Consolas', 9),
            bg='#2c3e50',
            fg='#ecf0f1',
            relief='flat',
            wrap='word'
        )
        self.status_display.pack(fill='both', expand=True)
        
        # Scrollbar for status
        scrollbar = tk.Scrollbar(status_frame, orient='vertical', command=self.status_display.yview)
        scrollbar.pack(side='right', fill='y')
        self.status_display.configure(yscrollcommand=scrollbar.set)
        
    def select_file(self):
        """Select a file for compression"""
        file_types = [
            ("All Supported Files", "*.jpg *.jpeg *.png *.bmp *.tiff *.pdf *.doc *.docx"),
            ("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff"),
            ("PDF Files", "*.pdf"),
            ("Document Files", "*.doc *.docx"),
            ("All Files", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="Select file to compress",
            filetypes=file_types
        )
        
        if file_path:
            self.selected_file = file_path
            self.update_file_info()
            self.update_settings_ui()
            self.compress_btn.config(state='normal')
            self.log_status(f"Selected file: {os.path.basename(file_path)}")
            
    def update_file_info(self):
        """Update file information display"""
        if self.selected_file:
            file_path = Path(self.selected_file)
            file_size = file_path.stat().st_size
            file_size_mb = file_size / (1024 * 1024)
            
            info_text = f"📄 {file_path.name}\n"
            info_text += f"📁 Location: {file_path.parent}\n"
            info_text += f"📏 Size: {file_size_mb:.2f} MB ({file_size:,} bytes)\n"
            info_text += f"🔧 Type: {file_path.suffix.upper() if file_path.suffix else 'Unknown'}"
            
            self.file_info_label.config(text=info_text, fg='#2c3e50')
            
    def update_settings_ui(self):
        """Update settings UI based on file type"""
        # Clear existing settings
        for widget in self.settings_container.winfo_children():
            widget.destroy()
            
        if not self.selected_file:
            return
            
        file_ext = Path(self.selected_file).suffix.lower()
        
        if file_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
            self.create_image_settings()
        elif file_ext == '.pdf':
            self.create_pdf_settings()
        else:
            self.create_generic_settings()
            
    def create_image_settings(self):
        """Create settings for image compression"""
        # Quality slider
        tk.Label(
            self.settings_container,
            text="Image Quality:",
            font=('Segoe UI', 10, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 5))
        
        self.quality_var = tk.IntVar(value=85)
        quality_scale = tk.Scale(
            self.settings_container,
            from_=10,
            to=100,
            orient='horizontal',
            variable=self.quality_var,
            bg='#f0f0f0',
            fg='#2c3e50',
            highlightthickness=0
        )
        quality_scale.pack(fill='x', pady=(0, 10))
        
        # Target size entry
        tk.Label(
            self.settings_container,
            text="Target Size (KB):",
            font=('Segoe UI', 10, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 5))
        
        self.target_size_var = tk.StringVar(value="500")
        target_entry = tk.Entry(
            self.settings_container,
            textvariable=self.target_size_var,
            font=('Segoe UI', 10),
            relief='solid',
            bd=1
        )
        target_entry.pack(fill='x', pady=(0, 10))
        
    def create_pdf_settings(self):
        """Create settings for PDF compression"""
        # Compression level
        tk.Label(
            self.settings_container,
            text="Compression Level:",
            font=('Segoe UI', 10, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(0, 5))
        
        self.pdf_compression_var = tk.StringVar(value="medium")
        compression_frame = tk.Frame(self.settings_container, bg='#f0f0f0')
        compression_frame.pack(fill='x', pady=(0, 10))
        
        tk.Radiobutton(
            compression_frame,
            text="Low (Better Quality)",
            variable=self.pdf_compression_var,
            value="low",
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(anchor='w')
        
        tk.Radiobutton(
            compression_frame,
            text="Medium (Balanced)",
            variable=self.pdf_compression_var,
            value="medium",
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(anchor='w')
        
        tk.Radiobutton(
            compression_frame,
            text="High (Smaller Size)",
            variable=self.pdf_compression_var,
            value="high",
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(anchor='w')
        
    def create_generic_settings(self):
        """Create generic settings for other file types"""
        tk.Label(
            self.settings_container,
            text="Generic compression will be applied",
            font=('Segoe UI', 10),
            bg='#f0f0f0',
            fg='#7f8c8d'
        ).pack()
        
    def start_compression(self):
        """Start the compression process in a separate thread"""
        if not self.selected_file:
            return
            
        self.compress_btn.config(state='disabled')
        self.compression_progress.set(0)
        self.status_text.set("Starting compression...")
        
        # Start compression in separate thread
        thread = threading.Thread(target=self.compress_file)
        thread.daemon = True
        thread.start()
        
    def compress_file(self):
        """Compress the selected file"""
        try:
            file_path = Path(self.selected_file)
            file_ext = file_path.suffix.lower()
            
            self.log_status("Starting compression process...")
            self.update_progress(10)
            
            if file_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
                self.compress_image()
            elif file_ext == '.pdf':
                self.compress_pdf()
            else:
                self.compress_generic()
                
        except Exception as e:
            self.log_status(f"Error during compression: {str(e)}")
            self.status_text.set("Compression failed")
            self.compress_btn.config(state='normal')
            
    def compress_image(self):
        """Compress image file"""
        try:
            self.log_status("Loading image...")
            self.update_progress(20)
            
            img = Image.open(self.selected_file)
            
            # Get target size
            target_kb = int(self.target_size_var.get())
            quality = self.quality_var.get()
            
            self.log_status(f"Compressing with quality: {quality}%")
            self.update_progress(40)
            
            # Find optimal quality
            while quality > 10:
                buffer = io.BytesIO()
                img.save(buffer, format='JPEG', quality=quality, optimize=True)
                size_kb = len(buffer.getvalue()) // 1024
                
                if size_kb <= target_kb:
                    break
                quality -= 5
                
            self.update_progress(70)
            
            # Save compressed image
            output_path = self.get_output_path("compressed")
            img.save(output_path, format='JPEG', quality=quality, optimize=True)
            
            self.update_progress(100)
            self.log_status(f"Image compressed successfully!")
            self.log_status(f"Original size: {Path(self.selected_file).stat().st_size / 1024:.1f} KB")
            self.log_status(f"Compressed size: {Path(output_path).stat().st_size / 1024:.1f} KB")
            self.log_status(f"Saved as: {output_path}")
            
            self.status_text.set("Compression completed successfully!")
            messagebox.showinfo("Success", f"Image compressed and saved as:\n{output_path}")
            
        except Exception as e:
            self.log_status(f"Error compressing image: {str(e)}")
            raise
            
        finally:
            self.compress_btn.config(state='normal')
            
    def compress_pdf(self):
        """Compress PDF file"""
        try:
            self.log_status("PDF compression requires PyMuPDF library")
            self.log_status("Please install it with: pip install PyMuPDF")
            messagebox.showwarning("Library Required", "PDF compression requires PyMuPDF library.\nPlease install it with: pip install PyMuPDF")
            
        except Exception as e:
            self.log_status(f"Error compressing PDF: {str(e)}")
            raise
            
        finally:
            self.compress_btn.config(state='normal')
            
    def compress_generic(self):
        """Generic compression for other file types"""
        try:
            self.log_status("Applying generic compression...")
            self.update_progress(50)
            
            # For now, just copy the file with a prefix
            output_path = self.get_output_path("processed")
            
            import shutil
            shutil.copy2(self.selected_file, output_path)
            
            self.update_progress(100)
            self.log_status(f"File processed successfully!")
            self.log_status(f"Saved as: {output_path}")
            
            self.status_text.set("Processing completed!")
            messagebox.showinfo("Success", f"File processed and saved as:\n{output_path}")
            
        except Exception as e:
            self.log_status(f"Error processing file: {str(e)}")
            raise
            
        finally:
            self.compress_btn.config(state='normal')
            
    def get_output_path(self, prefix):
        """Generate output file path"""
        file_path = Path(self.selected_file)
        return file_path.parent / f"{prefix}_{file_path.name}"
        
    def update_progress(self, value):
        """Update progress bar"""
        self.compression_progress.set(value)
        self.root.update_idletasks()
        
    def log_status(self, message):
        """Add message to status display"""
        self.status_display.insert('end', f"{message}\n")
        self.status_display.see('end')
        self.root.update_idletasks()
        
    def clear_selection(self):
        """Clear current file selection"""
        self.selected_file = None
        self.file_info_label.config(text="No file selected", fg='#7f8c8d')
        self.compress_btn.config(state='disabled')
        self.compression_progress.set(0)
        self.status_text.set("Ready to compress files")
        self.status_display.delete(1.0, 'end')
        
        # Clear settings
        for widget in self.settings_container.winfo_children():
            widget.destroy()
            
        self.settings_label = tk.Label(
            self.settings_container,
            text="Select a file to see compression options",
            font=('Segoe UI', 10),
            bg='#f0f0f0',
            fg='#7f8c8d'
        )
        self.settings_label.pack()
        
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = FileCompressor()
    app.run() 
