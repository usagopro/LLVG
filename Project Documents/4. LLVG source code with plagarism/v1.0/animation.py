def draw_line(canvas, obj):
    # Create a line object on the canvas
    obj.canvas_id = canvas.create_line(obj.p1.x, obj.p1.y, obj.p1.x, obj.p1.y, fill=obj.fill_color, width=obj.width)

    # Calculate the distance between the two points
    dx = obj.p2.x - obj.p1.x
    dy = obj.p2.y - obj.p1.y
    distance = max(abs(dx), abs(dy))

    # Calculate the step size for each frame
    if distance != 0:
        x_step = dx / distance
        y_step = dy / distance
    else:
        x_step = y_step = 0

    def animate(frame):
        # Calculate the next point
        x = obj.p1.x + x_step * frame
        y = obj.p1.y + y_step * frame

        # Update the line coordinates
        canvas.coords(obj.canvas_id, obj.p1.x, obj.p1.y, x, y)

        if frame < distance:
            # Schedule the next animation frame
            canvas.after(10, animate, frame + 1)

    # Start the animation
    animate(1)
