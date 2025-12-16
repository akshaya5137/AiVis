import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
from backend import (capture_faces, train_model, start_attendance, view_registered_users, 
                     manage_user, get_users, get_attendance_data)

class ScrollableFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="#161A23", height=400, highlightthickness=0)
        sb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.frame = ttk.Frame(self.canvas)
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.win_id = self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=sb.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.win_id, width=e.width))

class AiVisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AiVis - Smart Face Recognition")
        self.root.geometry("1100x700")
        self.root.configure(bg="#0F1117")
        if os.path.exists("attendance/attendance_session.csv"): os.remove("attendance/attendance_session.csv")

        self.style = ttk.Style()
        self.style.theme_use('clam')
        colors = {"bg": "#0F1117", "panel": "#161A23", "fg": "#E6E8EE", "accent": "#7C7CFF", "danger": "#FF5C5C"}
        
        styles = {
            "TFrame": {"background": colors["bg"]},
            "TLabelframe": {"background": colors["panel"], "foreground": colors["fg"], "bordercolor": "#23283A"},
            "TLabelframe.Label": {"background": colors["panel"], "foreground": colors["accent"], "font": ("Segoe UI", 11, "bold")},
            "TLabel": {"background": colors["bg"], "foreground": colors["fg"], "font": ("Segoe UI", 11)},
            "Header.TLabel": {"font": ("Calibri", 36, "bold"), "foreground": colors["accent"], "background": colors["bg"]},
            "Slogan.TLabel": {"font": ("Segoe UI", 12, "italic"), "foreground": "#8A93A6", "background": colors["bg"]},
            "TButton": {"font": ("Segoe UI", 10, "bold"), "padding": 10, "background": colors["panel"], "foreground": colors["fg"], "borderwidth": 1},
            "Danger.TButton": {"foreground": colors["danger"], "background": colors["panel"]}
        }
        for name, cfg in styles.items(): self.style.configure(name, **cfg)
        self.style.map("TButton", background=[("active", "#23283A")], foreground=[("active", colors["accent"])])

        main = ttk.Frame(root, padding=20, style="TFrame")
        main.pack(fill=tk.BOTH, expand=True)
        
        h_frame = ttk.Frame(main, style="TFrame")
        h_frame.pack(pady=(0, 20))
        ttk.Label(h_frame, text="AiVis", style="Header.TLabel").pack()
        ttk.Label(h_frame, text="Your Face, Your Key", style="Slogan.TLabel").pack()
        
        content = ttk.Frame(main)
        content.pack(fill=tk.BOTH, expand=True)
        self.create_sidebar(content)
        
        self.panel = ttk.LabelFrame(content, text="Live Session Report", padding=15)
        self.panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.build_report()
        self.update_report()
        self.edits = {"del": set(), "ren": {}, "hist": []}

    def create_sidebar(self, parent):
        f = ttk.LabelFrame(parent, text="Actions", padding=15)
        f.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        actions = [("Register User", self.reg), ("Train Model", self.train), ("Start Camera", self.cam),
                   ("SEP",), ("View Users", view_registered_users), ("Manage Users", self.manage),
                   ("Reset Session", self.reset), ("SEP",), ("Exit", self.root.quit, "Danger.TButton")]
        
        for a in actions:
            if a[0] == "SEP": ttk.Separator(f, orient='horizontal').pack(fill='x', pady=10)
            else: ttk.Button(f, text=a[0], command=a[1], width=20, style=a[2] if len(a)>2 else "TButton").pack(pady=5)

    def build_report(self):
        for w in self.panel.winfo_children(): w.destroy()
        self.panel.config(text="Live Session Report")
        
        self.stats = ttk.Label(self.panel, text="Present: 0 | Absent: 0", font=("Segoe UI", 14, "bold"))
        self.stats.pack(pady=(0, 10))
        
        sum_f = ttk.LabelFrame(self.panel, text="Session Summary", padding=10)
        sum_f.pack(side=tk.BOTTOM, fill=tk.X, pady=(15, 0))
        self.sum_txt = tk.Text(sum_f, height=4, font=("Segoe UI", 10), bg="#0F1117", fg="#E6E8EE", relief="flat")
        self.sum_txt.pack(fill=tk.BOTH)

        head = ttk.Frame(self.panel)
        head.pack(fill=tk.X, pady=2)
        
        for i, (txt, w) in enumerate([("ID", 1), ("Name", 3), ("Status", 2)]):
            head.columnconfigure(i, weight=w)
            tk.Label(head, text=txt, font=("Segoe UI", 10, "bold"), bg="#161A23", fg="#7C7CFF", anchor="center").grid(row=0, column=i, sticky="ew")
        
        self.list = ScrollableFrame(self.panel)
        self.list.pack(fill=tk.BOTH, expand=True)

    def update_report(self):
        if not hasattr(self, 'list'): return
        for w in self.list.frame.winfo_children(): w.destroy()
        p, a, date = get_attendance_data()
        
        # Sort logic
        recs = sorted([(x[0], x[1], "Present ✓", "#3DDC97") for x in p] + [(x[0], x[1], "Absent ✗", "#FF5C5C") for x in a], key=lambda x: int(x[0]) if x[0].isdigit() else 999)

        for uid, name, stat, col in recs:
            row = tk.Frame(self.list.frame, bg="#161A23")
            row.pack(fill=tk.X, pady=2)
            for i, w in enumerate([1, 3, 2]): row.columnconfigure(i, weight=w)
            
            # ID and Name (Centered)
            tk.Label(row, text=uid, bg="#161A23", fg="#E6E8EE", anchor="center").grid(row=0, column=0, sticky="ew")
            tk.Label(row, text=name, bg="#161A23", fg="#E6E8EE", anchor="center").grid(row=0, column=1, sticky="ew")
            
            # Pill Badge
            p_wrap = tk.Frame(row, bg="#161A23")
            p_wrap.grid(row=0, column=2)
            
            # Border frame needs to be packed into wrapper
            pill_border = tk.Frame(p_wrap, bg=col, padx=1, pady=1)
            pill_border.pack()
            
            # Label needs to be packed into border
            tk.Label(pill_border, text=stat, width=15, bg="#161A23", fg=col, font=("Segoe UI", 9, "bold")).pack()
            
        self.stats.config(text=f"Present: {len(p)} | Absent: {len(a)}")
        self.sum_txt.delete(1.0, tk.END)
        self.sum_txt.insert(tk.END, f"Date: {date}\n\nPresent:\n{chr(10).join([x[1] for x in p]) or 'None'}\n\nAbsent:\n{chr(10).join([x[1] for x in a]) or 'None'}")

    def manage(self):
        for w in self.panel.winfo_children(): w.destroy()
        self.panel.config(text="Manage Users")
        self.edits = {"del": set(), "ren": {}, "hist": []}
        
        ctl = ttk.Frame(self.panel); ctl.pack(fill=tk.X, pady=(0, 10))
        for txt, cmd, side in [("Done", self.save, tk.RIGHT), ("Undo", self.undo, tk.RIGHT), ("Back", self.cancel, tk.LEFT)]:
            ttk.Button(ctl, text=txt, command=cmd).pack(side=side, padx=5)
        
        self.m_list = ScrollableFrame(self.panel); self.m_list.pack(fill=tk.BOTH, expand=True); self.refresh_m()

    def refresh_m(self):
        for w in self.m_list.frame.winfo_children(): w.destroy()
        head = ttk.Frame(self.m_list.frame); head.pack(fill=tk.X, pady=5)
        for t, w in zip(["DEL", "ID", "Name", "Edit"], [5, 10, 20, 5]):
            tk.Label(head, text=t, width=w, bg="#161A23", fg="#7C7CFF", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=5)
            
        for uid, folder in get_users(folders_only=True).items():
            name = folder.split('.', 1)[1] if '.' in folder else "Unknown"
            disp = self.edits["ren"].get(uid, name); b_del = uid in self.edits["del"]
            
            r = tk.Frame(self.m_list.frame, bg="#161A23"); r.pack(fill=tk.X, pady=2)
            tk.Button(r, text="🗑️", width=3, bg="#FF5C5C" if b_del else "#0F1117", fg="white", relief="flat", command=lambda i=uid: self.toggle_del(i)).pack(side=tk.LEFT, padx=5)
            tk.Label(r, text=uid, width=10, bg="#161A23", fg="#E6E8EE").pack(side=tk.LEFT, padx=5)
            tk.Label(r, text=disp, width=20, bg="#161A23", fg="#FF5C5C" if b_del else ("#7C7CFF" if uid in self.edits["ren"] else "#E6E8EE"), font=("Segoe UI", 10, "overstrike" if b_del else "normal")).pack(side=tk.LEFT, padx=5)
            tk.Button(r, text="✎", width=3, bg="#0F1117", fg="white", relief="flat", command=lambda i=uid, n=disp: self.ren(i, n)).pack(side=tk.LEFT, padx=5)

    def toggle_del(self, uid):
        act = "unmark" if uid in self.edits["del"] else "mark"
        if act == "mark": self.edits["del"].add(uid)
        else: self.edits["del"].remove(uid)
        self.edits["hist"].append((act, uid, None)); self.refresh_m()

    def ren(self, uid, old):
        new = simpledialog.askstring("Rename", f"New name for {uid}:", initialvalue=old)
        if new and new != old:
            prev = self.edits["ren"].get(uid, old)
            self.edits["ren"][uid] = new; self.edits["hist"].append(("ren", uid, prev)); self.refresh_m()

    def undo(self):
        if not self.edits["hist"]: return
        act, uid, val = self.edits["hist"].pop()
        if act == "mark": self.edits["del"].remove(uid)
        elif act == "unmark": self.edits["del"].add(uid)
        elif act == "ren": self.edits["ren"][uid] = val
        self.refresh_m()

    def save(self):
        if not messagebox.askyesno("Save", "Apply changes?"): return
        for uid in self.edits["del"]: manage_user(uid, "delete")
        for uid, name in self.edits["ren"].items(): 
            if uid not in self.edits["del"]: manage_user(uid, "rename", name)
        messagebox.showinfo("Saved", "Done. Please retrain!"); self.refresh_m()

    def cancel(self): self.build_report(); self.update_report()
    def reg(self): 
        uid = simpledialog.askstring("ID", "ID:"); name = simpledialog.askstring("Name", "Name:")
        if uid and name: capture_faces(uid, name); messagebox.showinfo("Done", "Captured")
    def train(self): train_model(); messagebox.showinfo("Done", "Trained")
    def cam(self): messagebox.showinfo("Info", "Starting..."); start_attendance(); self.update_report()
    def reset(self): 
        if messagebox.askyesno("Reset", "Clear session?"): 
            if os.path.exists("attendance/attendance_session.csv"): os.remove("attendance/attendance_session.csv")
            self.update_report()

if __name__ == "__main__": root = tk.Tk(); AiVisApp(root); root.mainloop()
