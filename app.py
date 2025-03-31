from flask import Flask, request, render_template, jsonify
from PIL import Image
import io
import base64
import re

app = Flask(__name__)

# Load the template image (Jar Jar with speech bubble)
JAR_JAR_TEMPLATE = "static/jar_jar_template.jpg"

# Define the coordinates of the speech bubble (left, top, right, bottom)
SPEECH_BUBBLE_COORDS = (520, 540, 1330, 800)  # Approximate coordinates

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the image data
        if 'image_data' in request.form:
            # Get the image data
            image_data = request.form['image_data']
            
            # Extract the base64 part
            image_data = re.sub('^data:image/.+;base64,', '', image_data)
            
            # Decode the image
            image_bytes = base64.b64decode(image_data)
            input_image = Image.open(io.BytesIO(image_bytes))
            
            # Create the meme
            output_image = create_meme(input_image)
            
            # Convert to base64 string to send back to the browser
            img_io = io.BytesIO()
            output_image.save(img_io, 'PNG')
            img_io.seek(0)
            
            # Convert to base64 string
            encoded_img = base64.b64encode(img_io.getvalue()).decode('utf-8')
            
            # Return the image as base64 data URL
            return jsonify({'image': f'data:image/png;base64,{encoded_img}'})
    
    return render_template('index.html')

def create_meme(input_image):
    # Open the Jar Jar template
    jar_jar = Image.open(JAR_JAR_TEMPLATE)
    
    # Calculate dimensions of speech bubble
    left, top, right, bottom = SPEECH_BUBBLE_COORDS
    bubble_width = right - left
    bubble_height = bottom - top
    
    # Resize input image to fit speech bubble
    resized_input = input_image.resize((bubble_width, bubble_height))
    
    # Create a copy of the Jar Jar image and paste the input
    result = jar_jar.copy()
    result.paste(resized_input, (left, top))
    
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5100)
