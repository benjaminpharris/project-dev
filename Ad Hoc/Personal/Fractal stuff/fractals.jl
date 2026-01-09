# Defining Complex numbers

c = Complex(1, 2)

println(c)

typeof(c)

using Base: pi

c * pi



# 1. THE MATH (Optimized for Mac/GPU)
function mandelbrot(c::Complex, max_iter=100)
    z = c
    for i in 1:max_iter
        if abs2(z) > 4.0
            return Float32(i) # Return Float32 for the GPU
        end
        z = z*z + c
    end
    return Float32(0) # Points inside the set are 0
end

using GLMakie

# 2. THE UI SETUP
fig = Figure(size = (800, 800))
# We manually set the limits so you don't start in "The Black Void"
ax = Axis(fig[1, 1], 
    aspect = DataAspect(), 
    title = "Mandelbrot: Scroll to Zoom",
    limits = (-2.1, 0.7, -1.2, 1.2) 
)

# 3. THE REACTIVE ENGINE
# This 'lift' triggers whenever you zoom or pan
fractal_data = lift(ax.finallimits) do lims
    # Resolution: Start small (400) to ensure speed, then bump to 800
    res = 400 
    
    x_range = LinRange(lims.origin[1], lims.origin[1] + lims.widths[1], res)
    y_range = LinRange(lims.origin[2], lims.origin[2] + lims.widths[2], res)
    
    # Calculate! Note the 'y' is the outer loop for correct orientation
    return [mandelbrot(x + y*im) for y in y_range, x in x_range]
end

# 4. THE PLOT
# 'colorrange' is key: it prevents the pink glitch by defining the scale
hm = heatmap!(ax, fractal_data, 
    colormap = :inferno, 
    colorrange = (0, 100) 
)

display(fig)