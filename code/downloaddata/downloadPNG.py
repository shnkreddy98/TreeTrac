import requests

# Base URL with a placeholder for the image index
base_url = "https://svs.gsfc.nasa.gov/vis/a030000/a030800/a030878/frames/3840x2160_16x9_30p/BlackMarble2016_{}.png"

# Starting and ending indices
start = 127
end = 4319

for i in range(start, end + 1):
    # Format the index with leading zeros to match the URL pattern (e.g., 00000, 00001, ..., 04319)
    image_index = f"{i:05}"
    url = base_url.format(image_index)
    
    # Send a request to download the image
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Save the image with the formatted index
        filename = f"pngs/BlackMarble2016_{image_index}.png"
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download image at index {image_index}")

