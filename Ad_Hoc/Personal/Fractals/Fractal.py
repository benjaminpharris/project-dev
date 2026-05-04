import numpy as np
import fastplotlib as fpl
import glfw

# 1. CONFIG: Force Desktop Backend
fpl.config.loop_type = "GLFW"

print("Initializing GPU Fractal Engine...")

# --- GLOBAL STATE ---
# We keep track of the exponent and resolution globally
state = {
    "exponent": 2.0,      # The 'd' in z^d + c
    "res": 800,           # Resolution (width/height)
    "max_iter": 100       # Detail level
}

# --- THE MATH ENGINE ---
def calculate_fractal(xmin, xmax, ymin, ymax, width, height, exponent=2.0, max_iter=100):
    # 1. Create the complex grid
    x = np.linspace(xmin, xmax, width, dtype=np.float32)
    y = np.linspace(ymin, ymax, height, dtype=np.float32)
    X, Y = np.meshgrid(x, y)
    c = X + 1j * Y
    
    z = np.zeros_like(c)
    output = np.zeros(c.shape, dtype=np.float32)
    
    # 2. Iterate
    # We use a simplified loop for raw speed during zoom
    for i in range(max_iter):
        mask = np.abs(z) <= 10
        # The Generalized Formula: z = z^exponent + c
        # We use 'power' instead of ** for better complex handling in numpy
        z[mask] = np.power(z[mask], exponent) + c[mask]
        
        # Smooth coloring recording
        escaped_now = (np.abs(z) > 10) & (output == 0)
        if i > 0:
            abs_z = np.abs(z[escaped_now])
            abs_z[abs_z == 0] = 1.0 # Prevent log(0)
            output[escaped_now] = i + 1 - np.log2(np.log2(abs_z))
            
    return output

# --- SETUP THE SCENE ---
# Create the figure
fig = fpl.Figure(size=(800, 600))

# Initial Generation
print("Generating initial frame...")
initial_data = calculate_fractal(-2.0, 0.5, -1.2, 1.2, state["res"], state["res"], state["exponent"])

# Add the Image to Subplot [0,0]
graphic = fig[0, 0].add_image(initial_data, cmap="magma", name="fractal_layer")

# Add Text Overlay (OSD)
text_overlay = fig[0, 0].add_text(
    text=f"Exponent: {state['exponent']:.2f} | Zoom: 1.0x",
    font_size=20,
    color="white",
    offset=(10, 10),
    anchor="top-left"
)

# --- INTERACTIVITY HOOKS ---

# 1. INFINITE ZOOM (Camera Change Event)
def on_zoom_pan(ev):
    # Get the new coordinates from the camera
    # get_world_rect returns (xmin, xmax, ymin, ymax)
    bounds = fig[0, 0].camera.get_world_rect()
    
    # Safety check: Prevent zooming in past float32 precision (creates artifacts)
    width = bounds[1] - bounds[0]
    if width < 1e-10: 
        return

    # Recalculate fractal for the new window
    new_data = calculate_fractal(
        bounds[0], bounds[1], 
        bounds[3], bounds[2], # Note: Y is often flipped in graphics, check this if upside down
        state["res"], state["res"],
        state["exponent"],
        state["max_iter"]
    )
    
    # Update the GPU texture
    graphic.data = new_data
    
    # Update Text
    zoom_level = 2.5 / width
    text_overlay.text = f"Exponent: {state['exponent']:.2f} | Zoom: {zoom_level:.1f}x"

# Attach the zoom hook
fig[0, 0].camera.add_event_handler(on_zoom_pan, "change")


# 2. PARAMETER CONTROL (Keyboard Events)
def on_key_press(ev):
    update_needed = False
    
    # Check which key was pressed
    if ev.key == "up":
        state["exponent"] += 0.1
        update_needed = True
    elif ev.key == "down":
        state["exponent"] -= 0.1
        update_needed = True
    elif ev.key == "r":
        # Reset View
        fig[0, 0].camera.set_world_rect((-2.0, 0.5, -1.2, 1.2))
        return # Camera change will trigger the update automatically

    if update_needed:
        # Force a re-render with the new exponent
        # We manually call our zoom handler to use current coordinates
        on_zoom_pan(None)

# Attach the key hook to the renderer (listens to the whole window)
fig.renderer.add_event_handler(on_key_press, "key_down")


# --- LAUNCH ---
print("Controls:")
print("  [Scroll]   Zoom In/Out")
print("  [Right-Click + Drag] Pan")
print("  [Up/Down]  Change Exponent (Morph Fractal)")
print("  [R]        Reset View")

fig.show()
fpl.loop.run()