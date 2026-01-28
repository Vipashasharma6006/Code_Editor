import tkinter as tk
import main

def start_main_editor():
    
    splash_root.destroy()
    main.main()       # Run the editor

# Create splash window
splash_root = tk.Tk()
splash_root.overrideredirect(True)
splash_root.geometry("500x300+500+200")
splash_root.configure(bg="#1e1e1e")

# Splash content
title = tk.Label(splash_root, text="CODE EDITOR", fg="#569CD6", bg="#1e1e1e",
                 font=("Consolas", 26, "bold"))
title.pack(pady=(80, 10))

subtitle = tk.Label(splash_root, text="with Autocompletion & Snippets", fg="#CE9178",
                    bg="#1e1e1e", font=("Consolas", 14))
subtitle.pack()

name = tk.Label(splash_root, text="Developed by Vipasha, Khushi, Abhilasha", fg="#9CDCFE",
                bg="#1e1e1e", font=("Consolas", 12, "italic"))
name.pack(pady=(40, 0))

# Use after() to run safely in the main thread
splash_root.after(3000, start_main_editor)

splash_root.mainloop()
