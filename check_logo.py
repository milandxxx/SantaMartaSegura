from PIL import Image
img = Image.open(r'C:\Users\CBN\Desktop\SantaMartaSegura\src\assets\logo-santa-marta.png')
print(f'Size: {img.size}, Mode: {img.mode}')