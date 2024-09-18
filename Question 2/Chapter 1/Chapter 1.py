from PIL import Image
import time


def generated_num():
    # Generate the number based on the current time
    current_time = int(time.time())

    generated_number = (current_time % 100) + 50

    if generated_number % 2 == 0:
        generated_number += 10

    return generated_number


def generate_image(img, n):
    width, height = img.size  # Get the size of the image
    pixels = img.load()  # Load pixel data

    total_RedPixel = 0  # Initialize a variable to store the sum of red pixel values

    for i in range(width):
        for j in range(height):
            r, g, b = pixels[i, j]

            # Ensure pixel values stay within valid range (0-255)
            r_new = min(r + n, 255)
            g_new = min(g + n, 255)
            b_new = min(b + n, 255)

            # Update the pixel with the new values
            pixels[i, j] = (r_new, g_new, b_new)

            # Add the new red value to the total sum of red pixels
            total_RedPixel += r_new

    # Save the modified image as 'chapter1out.png'
    img.save('chapter1out.png')

    return total_RedPixel


# Open the input image (ensure it exists with the correct name)
img = Image.open('chapter1.jpg')
num = generated_num()

# Generate the new image and print the sum of red pixels
print(generate_image(img, num))




