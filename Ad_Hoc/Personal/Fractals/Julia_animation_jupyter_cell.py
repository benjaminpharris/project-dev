import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.animation import FuncAnimation, FFMpegWriter
from numba import njit, prange
import cmasher as cmr

# --- 1. CONFIGURATION ---
# Display Settings (Samsung Odyssey G9 / 49" Ultrawide standards)
PIXEL_W = 5120
PIXEL_H = 1440
DPI = 300

# Calculate Figure Size in Inches for Matplotlib
WIDTH_INCHES = PIXEL_W / DPI
HEIGHT_INCHES = PIXEL_H / DPI

# Animation Settings
FPS = 60
DURATION_SEC = 30
TOTAL_FRAMES = FPS * DURATION_SEC
print(f"Total Frames to Render: {TOTAL_FRAMES} (Approx. 10-15 mins on i9)")

# Fractal Settings
NUM_ITER = 1000      # 1000 is plenty for video; 1500 if you want to be safe
GAMMA = 0.4          # Adjusted slightly for 'arctic' (usually needs more gamma than 'magma')
ZOOM_LEVEL = 0.8     # Controls how 'close' the camera is to the fractal

# --- 2. THE NUMBA ENGINE ---
@njit(parallel=True, fastmath=True)
def julia_numba(width, height, c_real, c_imag, max_iter, x_range, y_range):
    result = np.zeros((height, width), dtype=np.float64)
    
    # Pre-calculate coordinate scaling
    # We map pixels 0..width to -x_range..+x_range
    x_scale = (2.0 * x_range) / width
    y_scale = (2.0 * y_range) / height
    x_offset = -x_range
    y_offset = -y_range
    
    for y in prange(height):
        for x in range(width):
            zx = x * x_scale + x_offset
            zy = y * y_scale + y_offset
            
            i = 0
            while i < max_iter and (zx*zx + zy*zy) < 4.0:
                temp = zx*zx - zy*zy + c_real
                zy = 2.0 * zx * zy + c_imag
                zx = temp
                i += 1
            
            # Smooth Coloring
            if i < max_iter:
                log_zn = np.log(zx*zx + zy*zy) / 2.0
                nu = np.log(log_zn / np.log(2.0)) / np.log(2.0)
                result[y, x] = i + 1.0 - nu
            else:
                result[y, x] = 0
                
    return result

# --- 3. PATH GENERATION (The Loop) ---
# Create a perfect circle in the complex plane
# We use 'endpoint=False' to ensure the last frame doesn't duplicate the first
# so the loop is seamless.
t = np.linspace(0, 2*np.pi, TOTAL_FRAMES, endpoint=False)
radius = 0.7885 
path_real = radius * np.cos(t)
path_imag = radius * np.sin(t)

# --- 4. MESH SETUP (Aspect Ratio Logic) ---
aspect_ratio = PIXEL_W / PIXEL_H 
# Standard vertical view is [-2, 2]. 
# We expand horizontal view to match aspect ratio.
y_view = 2.0 / ZOOM_LEVEL
x_view = y_view * aspect_ratio

# --- 5. INITIALIZATION ---
print("Initializing Figure...")
fig = plt.figure(figsize=(WIDTH_INCHES, HEIGHT_INCHES), dpi=DPI)
ax = plt.axes([0, 0, 1, 1], frameon=False)
ax.set_axis_off()

# Generate first frame to setup the plot artist
initial_data = julia_numba(PIXEL_W, PIXEL_H, path_real[0], path_imag[0], NUM_ITER, x_view, y_view)

# Setup Norm and Colormap
norm = colors.PowerNorm(gamma=GAMMA, vmin=0, vmax=NUM_ITER)
im = ax.imshow(initial_data, 
               cmap='cmr.arctic', 
               norm=norm, 
               interpolation='nearest', 
               origin='lower')

# --- 6. ANIMATION LOOP ---
def update(frame_idx):
    if frame_idx % 60 == 0:
        print(f"Rendering Frame {frame_idx}/{TOTAL_FRAMES}")
        
    c_r = path_real[frame_idx]
    c_i = path_imag[frame_idx]
    
    # Calculate new data
    data = julia_numba(PIXEL_W, PIXEL_H, c_r, c_i, NUM_ITER, x_view, y_view)
    im.set_array(data)
    return [im]

print("Starting Render...")
ani = FuncAnimation(fig, update, frames=TOTAL_FRAMES, blit=True)

# Save High Bitrate MP4
# bitrate=30000 ensures the grain/detail isn't compressed out
writer = FFMpegWriter(fps=FPS, bitrate=30000, extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p'])
ani.save('ultrawide_julia_loop.mp4', writer=writer, dpi=DPI)
print("Render Complete!")