import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO

# Helper function to load image from a URL
def load_image_from_url(url):
    # Define a custom User-Agent header
    # It's good practice to make this descriptive and include contact info
    # For example: "MyPythonImageDownloader/1.0 (YourName/ProjectName; contact@example.com)"
    headers = {
        "User-Agent": "MyPythonImageProcessor/1.0 (LearningProject; sindhusura46@gmail.com)"
    }
    
    response = requests.get(url, headers=headers)
    # Ensure the request was successful
    response.raise_for_status()
    return Image.open(BytesIO(response.content))

# Elephant image URL
elephant_url = "https://upload.wikimedia.org/wikipedia/commons/3/37/African_Bush_Elephant.jpg"

# Load elephant image
try:
    elephant = load_image_from_url(elephant_url)
except requests.exceptions.RequestException as e:
    print(f"Error loading image: {e}")
    exit() # Exit if image can't be loaded

# Display original image
plt.figure(figsize=(6, 4))
plt.imshow(elephant)
plt.title("Elephant")
plt.axis("off")
plt.savefig("elephant_grayscale.png") # Corrected: Added filename for saving
plt.show() # Display the plot

# Convert to NumPy array and print shape
elephant_np = np.array(elephant)
print("Elephant image shape:", elephant_np.shape)

# Convert to grayscale
elephant_gray = elephant.convert("L")

# Display grayscale image
plt.figure(figsize=(6, 4))
plt.imshow(elephant_gray, cmap="gray")
plt.title("Elephant (Grayscale)")
plt.axis("off")
plt.savefig("elephant_grayscale.png") # Corrected: Added filename for saving
plt.show() # Display the plot