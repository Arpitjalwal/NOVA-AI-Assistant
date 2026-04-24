import tkinter as tk
import math
import threading
import datetime

# Global variables
angle = 0 
root = None

def run_gui():
    global root, angle
    root = tk.Tk()
    root.title("NOVA JARVIS INTERFACE")
    
    # Screen Logic
    width, height = 800, 700
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.overrideredirect(True) 
    root.config(bg='black') 
    root.attributes("-transparentcolor", "black") 
    root.attributes("-topmost", True) 

    canvas = tk.Canvas(root, width=width, height=height, bg="black", highlightthickness=0)
    canvas.pack()

    cx, cy = 400, 350 # Center Point

    def update_data():
        global angle
        canvas.delete("all")
        
        # 1. TOP LEFT STATUS BOX
        canvas.create_rectangle(30, 30, 200, 80, outline="#00FFFF", width=1)
        canvas.create_text(40, 45, text=":::: JARVIS OS: v4.0 ::::", fill="#00FFFF", font=("Orbitron", 8), anchor="w")
        canvas.create_text(40, 65, text="STATUS: ONLINE", fill="#00FFFF", font=("Orbitron", 10, "bold"), anchor="w")

        # 2. TOP RIGHT DATE/TIME
        now = datetime.datetime.now()
        canvas.create_text(width-30, 45, text=now.strftime("%H:%M:%S"), fill="#00FFFF", font=("Orbitron", 10), anchor="e")
        canvas.create_text(width-30, 65, text=now.strftime("%Y-%m-%d"), fill="#00FFFF", font=("Orbitron", 10), anchor="e")

        # 3. CENTRAL STAR CORE (The Orange Sun)
        s_radius = 60 + 5 * math.sin(angle * 2)
        star_points = []
        for i in range(24): # More points for star spikes
            r = s_radius if i % 2 == 0 else s_radius * 0.6
            a = (i * math.pi / 12) + angle
            star_points.extend([cx + r * math.cos(a), cy + r * math.sin(a)])
        canvas.create_polygon(star_points, fill="#FF4500", outline="#FFCC00", width=2)

        # 4. RADIAL CONNECTING LINES & NODES (As per Image)
        nodes = ["VOICE", "NETWORK", "SECURITY", "ALGORITH", "SYSTEM", "MEMORY"]
        r_dist = 220 # Distance of nodes from center
        
        for i, label in enumerate(nodes):
            # Calculate position
            a = (i * (2 * math.pi / len(nodes))) - (math.pi / 2)
            nx = cx + r_dist * math.cos(a)
            ny = cy + r_dist * math.sin(a)
            
            # Connecting Dotted Lines
            canvas.create_line(cx, cy, nx, ny, fill="#00FFFF", dash=(5, 5), width=1)
            
            # Node Circle
            canvas.create_oval(nx-15, ny-15, nx+15, ny+15, outline="#00FFFF", width=2)
            canvas.create_text(nx, ny+25, text=label, fill="#00FFFF", font=("Orbitron", 7, "bold"))

        # 5. ROTATING ORANGE RINGS
        for r in [130, 180]:
            offset = angle if r == 130 else -angle
            canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start=math.degrees(offset), extent=120, style=tk.ARC, outline="#FF4500", width=2)
            canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start=math.degrees(offset)+180, extent=120, style=tk.ARC, outline="#FF4500", width=2)

        angle += 0.03 
        root.after(40, update_data)

    update_data()
    root.mainloop()

def start_gui_thread():
    t = threading.Thread(target=run_gui)
    t.daemon = True 
    t.start()