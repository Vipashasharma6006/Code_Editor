import tkinter as tk
from tkinter import filedialog
import autocomplete  # Import your autocomplete logic
import runner
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name
from pygments.token import Token

color_map = {
    Token.Keyword: "#569CD6",
    Token.Name: "#9CDCFE",
    Token.Comment: "#6A9955",
    Token.String: "#CE9178",
    Token.Number: "#B5CEA8",
    Token.Operator: "#D4D4D4",
    Token.Function: "#DCDCAA",
}
def highlight_syntax():
    code = text_area.get(1.0, tk.END)
    text_area.tag_remove("Token", "1.0", tk.END)

    for token, content in lex(code, PythonLexer()):
        tag_name = str(token)
        if token in color_map:
            text_area.tag_config(tag_name, foreground=color_map[token])
            start = "1.0"
            while True:
                pos = text_area.search(content, start, tk.END)
                if not pos:
                    break
                end = f"{pos}+{len(content)}c"
                text_area.tag_add(tag_name, pos, end)
                start = end
def update_line_numbers(event=None):
    line_numbers.config(state="normal")
    line_numbers.delete(1.0, tk.END)

    line_count = text_area.index("end-1c").split(".")[0]
    lines = "\n".join(str(i) for i in range(1, int(line_count) + 1))
    line_numbers.insert(1.0, lines)
    line_numbers.config(state="disabled")
def auto_save():
    try:
        with open("autosave.py", "w") as f:
            f.write(text_area.get(1.0, tk.END))
        print("Auto-saved successfully.")
    except Exception as e:
        print("Auto-save error:", e)
    
    root.after(10000, auto_save)  # every 10 seconds




# Step 1: Create main window
root = tk.Tk()
root.title("Code Editor with Autocompletion")
root.geometry("800x600")

# Step 2: Add Text Area

# Create a frame to hold both line numbers and text area
editor_frame = tk.Frame(root)
editor_frame.pack(fill="both", expand=1)

# Line number widget
line_numbers = tk.Text(editor_frame, width=4, padx=4, takefocus=0, border=0,
                       background="#2b2b2b", foreground="#C586C0", state="disabled")
line_numbers.pack(side="left", fill="y")

# Main text area
text_area = tk.Text(editor_frame, font=("Consolas", 14), bg="#1e1e1e", fg="#ffffff",
                    insertbackground="white", undo=True)
text_area.pack(side="right", fill="both", expand=1)
text_area.tag_configure("error_line", background="#512020")  # Dark red


#output_label = tk.Label(root, text="Output:", bg="#1e1e1e", fg="white")
output_label = tk.Label(root, text="Output Console", bg="#1e1e1e", fg="#CE9178", font=("Consolas", 12, "bold"))
#output_label.pack(anchor="w")
output_label.pack(anchor="w", padx=10, pady=(5, 0))
#output_box = tk.Text(root, height=10, font=("Consolas", 12), bg="#252526", fg="white")
output_box = tk.Text(root, height=10, font=("Consolas", 12), bg="#1e1e1e", fg="#569CD6", insertbackground="white")

#output_box.pack(fill="x")
output_box.pack(fill="x", padx=10, pady=(0, 10))
status_label = tk.Label(root, text="Ready", anchor="w", fg="white", bg="#1e1e1e", font=("Consolas", 10, "italic"))
status_label.pack(fill="x", padx=10, pady=(0, 5))
cursor_status = tk.Label(root, text="Line 1, Col 1", anchor="e", fg="white", bg="#1e1e1e", font=("Consolas", 10))
cursor_status.pack(fill="x", side="bottom", padx=10)



# Step 3: Add Suggestion Box (Listbox)
suggestion_box = tk.Listbox(root, height=5)
suggestion_box.place_forget()  # Hide initially

# Step 4: Create Menu Bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Step 5: Add File Menu and Functions
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)

def new_file():
    text_area.delete(1.0, tk.END)

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, content)

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_area.get(1.0, tk.END))
def run_current_code():
    code = text_area.get(1.0, tk.END)

    # Popup for multiple inputs
    input_popup = tk.Toplevel(root)
    input_popup.title("User Input")
    input_popup.geometry("350x250")
    input_popup.configure(bg="#1e1e1e")

    tk.Label(input_popup, text="Enter all inputs (one per line):", bg="#1e1e1e", fg="white", font=("Consolas", 10)).pack(pady=10)

    input_field = tk.Text(input_popup, height=5, font=("Consolas", 10))
    input_field.pack(pady=5, padx=10)

    def execute_code():
        user_input = input_field.get(1.0, tk.END)
        output = runner.run_code(code, user_input)
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, output)
        input_popup.destroy()

    run_btn = tk.Button(input_popup, text="Run Code", command=execute_code,
                        bg="#007acc", fg="white", font=("Consolas", 10))
    run_btn.pack(pady=10)

def show_stats():
    content = text_area.get("1.0", tk.END)
    words = len(content.split())
    lines = int(text_area.index('end-1c').split('.')[0])
    
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, f"📝 Total Words: {words}\n📏 Total Lines: {lines}")
def open_search_replace():
    popup = tk.Toplevel(root)
    popup.title("Search and Replace")
    popup.geometry("350x180")
    popup.configure(bg="#1e1e1e")

    # Find label and entry
    find_label = tk.Label(popup, text="Find:", bg="#1e1e1e", fg="white", font=("Consolas", 10))
    find_label.pack(pady=(10, 0))
    find_entry = tk.Entry(popup, width=30, font=("Consolas", 10))
    find_entry.pack(pady=5)

    # Replace label and entry
    replace_label = tk.Label(popup, text="Replace with:", bg="#1e1e1e", fg="white", font=("Consolas", 10))
    replace_label.pack(pady=(10, 0))
    replace_entry = tk.Entry(popup, width=30, font=("Consolas", 10))
    replace_entry.pack(pady=5)

    # Replace function
    def replace_text():
        find_text = find_entry.get()
        replace_text = replace_entry.get()
        content = text_area.get("1.0", tk.END)
        new_content = content.replace(find_text, replace_text)
        text_area.delete("1.0", tk.END)
        text_area.insert("1.0", new_content)
        popup.destroy()

    # Replace All Button
    replace_btn = tk.Button(popup, text="Replace All", command=replace_text,
                            bg="#007acc", fg="white", font=("Consolas", 10), padx=10, pady=5)
    replace_btn.pack(pady=15)
def auto_close(event):
    pairs = {
        '(': ')',
        '[': ']',
        '{': '}',
        '"': '"',
        "'": "'"
    }

    char = event.char
    if char in pairs:
        cursor_pos = text_area.index(tk.INSERT)
        text_area.insert(cursor_pos, pairs[char])
        text_area.mark_set(tk.INSERT, f"{cursor_pos}")  # Move cursor back between the pair



file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
def toggle_theme():
    current_bg = text_area["bg"]
    if current_bg == "#1e1e1e":
        text_area.config(bg="white", fg="black", insertbackground="black")
    else:
        text_area.config(bg="#1e1e1e", fg="white", insertbackground="white")

theme_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Theme", menu=theme_menu)
theme_menu.add_command(label="Toggle Dark/Light", command=toggle_theme)
run_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Run", menu=run_menu)
search_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Search", menu=search_menu)
search_menu.add_command(label="Search and Replace", command=open_search_replace)
tools_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Tools", menu=tools_menu)
tools_menu.add_command(label="Word & Line Count", command=show_stats)
snippets_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Snippets", menu=snippets_menu)

# Add snippet options
snippets_menu.add_command(label="For Loop", command=lambda: insert_snippet("For Loop"))
snippets_menu.add_command(label="If-Else", command=lambda: insert_snippet("If-Else"))
snippets_menu.add_command(label="Function", command=lambda: insert_snippet("Function"))
snippets_menu.add_command(label="While Loop", command=lambda: insert_snippet("While Loop"))
snippets_menu.add_command(label="Input-Print", command=lambda: insert_snippet("Input-Print"))




#tools_menu.add_command(label="Search and Replace", command=open_search_replace)
run_menu.add_command(label="Run Python Code", command=run_current_code)


# Step 6: Autocomplete Logic Functions

def current_prefix():
    index = text_area.index(tk.INSERT)
    line = text_area.get(f"{index} linestart", index)
    return line.split()[-1] if line.split() else ""

def show_suggestions(event):
    prefix = current_prefix()
    suggestions = autocomplete.get_suggestions(prefix)

    if suggestions:
        suggestion_box.delete(0, tk.END)
        for word in suggestions:
            suggestion_box.insert(tk.END, word)

        try:
            x, y, _, _ = text_area.bbox(tk.INSERT)
            suggestion_box.place(x=x+10, y=y+40)
        except:
            pass
    else:
        suggestion_box.place_forget()
    suggestions = autocomplete.get_suggestions(prefix)


def insert_suggestion(event):
    try:
        selected = suggestion_box.get(suggestion_box.curselection())
        prefix = current_prefix()
        text_area.insert(tk.INSERT, selected[len(prefix):])
        suggestion_box.place_forget()
    except:
        pass
def insert_suggestion(event):
    try:
        selected = suggestion_box.get(suggestion_box.curselection())
        prefix = current_prefix()

        # Check if it’s a snippet
        snippet = autocomplete.expand_snippet(selected)
        if snippet:
            text_area.insert(tk.INSERT, snippet[len(prefix):])
        else:
            text_area.insert(tk.INSERT, selected[len(prefix):])
        suggestion_box.place_forget()
    except:
        pass
def insert_snippet(snippet_type):
    snippets = {
        "For Loop": "for i in range(5):\n    print(i)",
        "If-Else": "x = 5\nif x > 0:\n    print('Positive')\nelse:\n    print('Negative')",
        "Function": "def greet(name):\n    print('Hello', name)",
        "While Loop": "count = 0\nwhile count < 5:\n    print(count)\n    count += 1",
        "Input-Print": "name = input('Enter your name: ')\nprint('Welcome', name)"
    }
    
    text_area.insert(tk.INSERT, snippets.get(snippet_type, "# Snippet not found"))
def check_syntax():
    code = text_area.get("1.0", tk.END)
    text_area.tag_remove("error_line", "1.0", tk.END)  # Clear previous highlights

    try:
        compile(code, "<string>", "exec")
        status_label.config(text="✅ No syntax errors", fg="#6A9955")
    except SyntaxError as e:
        lineno = e.lineno
        status_label.config(text=f"❌ Syntax Error: {e.msg} (line {lineno})", fg="#F44747")
        
        # Highlight the error line
        line_start = f"{lineno}.0"
        line_end = f"{lineno}.end"
        text_area.tag_add("error_line", line_start, line_end)
    except Exception as e:
        status_label.config(text=f"⚠️ Error: {str(e)}", fg="#F44747")

def update_cursor_position(event=None):
    index = text_area.index(tk.INSERT)
    line, col = index.split(".")
    char_count = len(text_area.get("1.0", "end-1c"))
    cursor_status.config(text=f"📌 Line {line}, Col {int(col)+1} | 📏 {char_count} chars")




    #tk.Button(popup, text="Replace All", command=replace_text, bg="#007acc", fg="white").pack(pady=10)


# Step 7: Key Bindings
#text_area.bind("<KeyRelease>", show_suggestions)
#text_area.bind("<KeyRelease>", lambda e: [show_suggestions(e), highlight_syntax()])
text_area.bind("<KeyRelease>", lambda e: [show_suggestions(e), highlight_syntax(), update_line_numbers()])
text_area.bind("<MouseWheel>", update_line_numbers)
text_area.bind("<Button-1>", update_line_numbers)
text_area.bind("<Key>", auto_close)
root.bind("<Control-f>", lambda e: open_search_replace())
root.bind("<Control-r>", lambda e: run_current_code())
text_area.bind("<KeyRelease>", lambda e: [show_suggestions(e), highlight_syntax(), update_line_numbers(), check_syntax(), update_cursor_position()])
text_area.bind("<Button-1>", lambda e: [update_line_numbers(), update_cursor_position()])
text_area.bind("<MouseWheel>", lambda e: update_cursor_position())




suggestion_box.bind("<Return>", insert_suggestion)
suggestion_box.bind("<Double-Button-1>", insert_suggestion)
suggestion_box.bind("<Down>", lambda e: suggestion_box.focus_set())
suggestion_box.bind("<Up>", lambda e: suggestion_box.focus_set())
text_area.bind("<KeyRelease>", lambda e: [show_suggestions(e), highlight_syntax(), update_line_numbers(), check_syntax()])



# Step 8: Run the app
def main():
    auto_save()
    root.mainloop()
if __name__ == "__main__":
    main()
