function render({model, el}) {

    
    
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');

    let isDragging = null; // Which line is being dragged (1 = vertLine1, 2 = vertLine2, 3 = horLine1, 4 = horLine2)
    let lastMouseX = 0; // To store the previous mouse position
    let lastMouseY = 0;

    // Initial positions of lines
    let vertLine1X = model.get('vline_left');
    let vertLine2X = model.get('vline_right');
    let horLine1Y = model.get('hline_upper');
    let horLine2Y = model.get('hline_lower');

    // Intersections Marker Settings
    const markerColor = model.get('_marker_color');
    const markerSize = model.get('_marker_size');

    // Lines Style Settings
    const lineThickness = model.get('_line_width');
    const lineColor = model.get('_line_color');

    // Set the scale factor (default to 1, meaning no scaling)
    const scaleFactor = model.get('_scale_factor');

    // Configuration for intersection point markers
    const intersectionConfig = {
      color: markerColor,     // Intersection point color
      size: markerSize,           // Intersection point size (radius for circle)
      shape: 'circle'    // Intersection point shape ('circle' or 'cross')
    };

    // Ensure smooth line joins and caps
    ctx.lineJoin = 'round';
    ctx.lineCap = 'round';

    // Create image object
    const backgroundImage = new Image();
    backgroundImage.src = model.get('_image_data');


    // When the image is loaded, start drawing
    backgroundImage.onload = function() {
      // Set canvas size to match the image size, then scale it by the scale factor
      canvas.width = backgroundImage.width * scaleFactor;
      canvas.height = backgroundImage.height * scaleFactor;

      // Draw the canvas with the image and lines
      drawCanvas();
    };

    // Draw the image, lines, and intersection points
    function drawCanvas() {
      // Clear the canvas before redrawing
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Draw the image on the canvas, scaling it according to the scale factor
      ctx.drawImage(backgroundImage, 0, 0, backgroundImage.width * scaleFactor, backgroundImage.height * scaleFactor);

      // Now draw the lines and intersection points on top of the image
      drawLines();
    }

    // Draw lines based on their current positions (scaled by the scale factor)
    function drawLines() {
      // Set the dashed style and red color for the lines
      ctx.setLineDash([5, 5]); // Make the lines dashed (5px dash, 5px gap)
      ctx.strokeStyle = lineColor; // Set the line color to red
      ctx.lineWidth = lineThickness; // Set the thickness of the lines scaled

      // Draw vertical lines
      ctx.beginPath();
      ctx.moveTo(vertLine1X * scaleFactor, 0);
      ctx.lineTo(vertLine1X * scaleFactor, canvas.height);
      ctx.moveTo(vertLine2X * scaleFactor, 0);
      ctx.lineTo(vertLine2X * scaleFactor, canvas.height);

      // Draw horizontal lines
      ctx.moveTo(0, horLine1Y * scaleFactor);
      ctx.lineTo(canvas.width, horLine1Y * scaleFactor);
      ctx.moveTo(0, horLine2Y * scaleFactor);
      ctx.lineTo(canvas.width, horLine2Y * scaleFactor);

      // Apply the stroke
      ctx.stroke();
      
      // Draw intersection points
      drawIntersectionPoints();

      // Draw captions "x1", "x2", "y1", and "y2"
      drawCaption();
    }

    // Draw intersection points based on configuration and scale
    function drawIntersectionPoints() {
      const intersections = [
        { x: vertLine1X * scaleFactor, y: horLine1Y * scaleFactor }, // Intersection of vertLine1 and horLine1
        { x: vertLine1X * scaleFactor, y: horLine2Y * scaleFactor }, // Intersection of vertLine1 and horLine2
        // { x: vertLine2X * scaleFactor, y: horLine1Y * scaleFactor }, // Intersection of vertLine2 and horLine1
        { x: vertLine2X * scaleFactor, y: horLine2Y * scaleFactor }, // Intersection of vertLine2 and horLine2
      ];

      intersections.forEach(point => {
        ctx.fillStyle = intersectionConfig.color;

        if (intersectionConfig.shape === 'circle') {
          ctx.beginPath();
          ctx.arc(point.x, point.y, intersectionConfig.size * scaleFactor, 0, Math.PI * 2); // Smooth circle at the intersection
          ctx.fill();
        } else if (intersectionConfig.shape === 'cross') {
          // Draw a cross at the intersection
          const size = intersectionConfig.size * scaleFactor;
          ctx.beginPath();
          ctx.moveTo(point.x - size, point.y - size);
          ctx.lineTo(point.x + size, point.y + size);
          ctx.moveTo(point.x - size, point.y + size);
          ctx.lineTo(point.x + size, point.y - size);
          ctx.stroke();
        }
      });
    }

    // Function to draw captions "x1", "x2", "y1", and "y2" next to the lines
    function drawCaption() {
      // Draw caption "x1" next to the left vertical line
      ctx.font = "14px Arial"; // Set font style for the caption
      ctx.fillStyle = lineColor; // Set text color (it is always same as line color)
      ctx.fillText("X1", vertLine1X * scaleFactor - 20, canvas.height - 10); // Draw "x1" next to the left vertical line

      // Draw caption "x2" next to the right vertical line
      ctx.fillText("X2", vertLine2X * scaleFactor - 20, canvas.height - 10); // Draw "x2" next to the right vertical line

      // Draw caption "y1" above the bottom horizontal line
      ctx.fillText("Y1", 10, horLine2Y * scaleFactor - 10); // Draw "y1" above the bottom horizontal line

      // Draw caption "y2" above the upper horizontal line
      ctx.fillText("Y2", 10, horLine1Y * scaleFactor - 10); // Draw "y2" above the upper horizontal line
    }

    // Mouse down event to start dragging
    canvas.addEventListener('mousedown', (event) => {
      const mouseX = event.offsetX;
      const mouseY = event.offsetY;
      
      // Save the current mouse position to use for dragging
      lastMouseX = mouseX;
      lastMouseY = mouseY;

      // Check if the mouse is near any vertical line
      if (Math.abs(mouseX - vertLine1X * scaleFactor) < 5) {
        isDragging = 1; // Dragging vertical line 1
        canvas.style.cursor = 'ew-resize'; // Change cursor when dragging
      } else if (Math.abs(mouseX - vertLine2X * scaleFactor) < 5) {
        isDragging = 2; // Dragging vertical line 2
        canvas.style.cursor = 'ew-resize'; // Change cursor when dragging
      }

      // Check if the mouse is near any horizontal line
      if (Math.abs(mouseY - horLine1Y * scaleFactor) < 5) {
        isDragging = 3; // Dragging horizontal line 1
        canvas.style.cursor = 'ns-resize'; // Change cursor when dragging
      } else if (Math.abs(mouseY - horLine2Y * scaleFactor) < 5) {
        isDragging = 4; // Dragging horizontal line 2
        canvas.style.cursor = 'ns-resize'; // Change cursor when dragging
      }
    });

    // Mouse move event to update the position of the dragged line
    canvas.addEventListener('mousemove', (event) => {
      const mouseX = event.offsetX;
      const mouseY = event.offsetY;

      // Check if the mouse is near any vertical line and change cursor to scale arrow (ew-resize)
      if (Math.abs(mouseX - vertLine1X * scaleFactor) < 10 || Math.abs(mouseX - vertLine2X * scaleFactor) < 10) {
        canvas.style.cursor = 'ew-resize';
      }
      // Check if the mouse is near any horizontal line and change cursor to scale arrow (ns-resize)
      else if (Math.abs(mouseY - horLine1Y * scaleFactor) < 10 || Math.abs(mouseY - horLine2Y * scaleFactor) < 10) {
        canvas.style.cursor = 'ns-resize';
      } 
      // If not near any line, revert to default cursor
      else {
        canvas.style.cursor = 'default';
      }

      // Update the position of the dragged line
      if (isDragging !== null) {
        const dx = mouseX - lastMouseX; // Change in mouse X
        const dy = mouseY - lastMouseY; // Change in mouse Y

        // Prevent lines from swapping or overlapping
        if (isDragging === 1 && vertLine1X + dx / scaleFactor < vertLine2X) {
          vertLine1X += dx / scaleFactor; // Move vertical line 1
          model.set("vline_left", vertLine1X);
          model.save_changes();
        } else if (isDragging === 2 && vertLine2X + dx / scaleFactor > vertLine1X) {
          vertLine2X += dx / scaleFactor; // Move vertical line 2
          model.set("vline_right", vertLine2X);
          model.save_changes();
        } else if (isDragging === 3 && horLine1Y + dy / scaleFactor < horLine2Y) {
          horLine1Y += dy / scaleFactor; // Move horizontal line 1
          model.set("hline_upper", horLine1Y);
          model.save_changes();
        } else if (isDragging === 4 && horLine2Y + dy / scaleFactor > horLine1Y) {
          horLine2Y += dy / scaleFactor; // Move horizontal line 2
          model.set("hline_lower", horLine2Y);
          model.save_changes();
        }

        // Update the last mouse position for the next move
        lastMouseX = mouseX;
        lastMouseY = mouseY;

        // Redraw the lines and intersection points after moving
        drawCanvas();
      }
    });

    // Mouse up and mouse leave events to stop dragging
    canvas.addEventListener('mouseup', () => {
      isDragging = null;
      canvas.style.cursor = 'default'; // Reset cursor when dragging ends
    });

    canvas.addEventListener('mouseleave', () => {
      isDragging = null;
      canvas.style.cursor = 'default'; // Reset cursor when mouse leaves
    });


    const container = document.createElement('div');
    container.appendChild(canvas);
    el.appendChild(container);

}

export default {render};