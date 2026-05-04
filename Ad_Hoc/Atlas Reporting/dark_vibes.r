dark_vibes <- function() {
  theme(
    # 1. Background Colors
    panel.background = element_rect(fill = NA, color = NA),
    panel.grid.major = element_line(color = "#444444ff", linewidth = 0.25, linetype = "solid"),
    panel.grid.minor = element_line(color = "#444444ff", linewidth = 0.25, linetype = "dotted"),
    plot.background  = element_rect(fill = "#262626", color = NA),
    legend.background = element_rect(fill = "#262626", color = NA),
    legend.key = element_rect(fill = "grey50", color = NA),

    # 2. Text Colors (Modified sizes for "Shrink" effect)
    text = element_text(color = "white"),
    axis.text = element_text(color = "white"),
    axis.title = element_text(color = "white"),
    plot.title = element_text(color = "white", face="bold"),
    plot.subtitle = element_text(color = "#cccccc"),
    
    # Shrinking legend text specifically
    legend.text = element_text(color = "white", size = 8), 
    legend.title = element_text(color = "white", size = 9, face = "bold", hjust = 0),

    # 3. Positioning & Margins
    axis.text.x = element_text(hjust = 1),
    
    # Plot Margin: Top, Right (Added Padding), Bottom, Left
    plot.margin = margin(t = 10, r = 25, b = 10, l = 10, unit = "pt"), 
    
    # Legend Adjustments
    legend.position = "top",
    legend.box = "horizontal",
    legend.title.position = "left",   # Moves title to the left of keys
    legend.margin = margin(t = 5, b = 5), 
    legend.key.size = unit(0.35, "cm"), # Shrinks the colored squares/lines
    legend.key.spacing.x = unit(10, "pt"), # Tightens spacing between keys
    legend.title.spacing = unit(10, "pt"), # Gap between title and first key
    
    # 4. Remove outer border
    panel.border = element_blank()
  )
}
