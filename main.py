from PIL import Image
import os

Image.MAX_IMAGE_PIXELS = None


def main():
    write_to_console("Preparing for work...")

    # Попытка открыть файлы изображений, иначе - ошибка
    try:
        original = Image.open("source.jpg")
    except FileNotFoundError:
        write_to_console(
            "The file 'source.jpg' was not found. Check for its presence in the folder with the program and run it again.")
        return

    try:
        image_for_pixel = Image.open("pixel.jpg")
    except FileNotFoundError:
        write_to_console(
            "The file 'pixel.jpg' was not found. Check for its presence in the folder with the program and run it again.")
        return

    # Загрузка списков пикселей изображений
    original_pixels = original.load()
    original_width, original_height = original.size
    pixel_image_pixels = image_for_pixel.load()
    pixel_image_width, pixel_image_height = image_for_pixel.size

    # Проверка размера итогового изображения и подтверждение старта его создания.
    number_of_pixels = original_width * pixel_image_width * original_height * pixel_image_height
    if number_of_pixels >= 10 ** 13:
        if not confirm_working(original_width * pixel_image_width, original_height * pixel_image_height,
                               "This will most likely burn your computer."):
            write_to_console("Operation aborted.")
            return
    elif number_of_pixels >= 10 ** 10:
        if not confirm_working(original_width * pixel_image_width, original_height * pixel_image_height,
                               "This will most likely burn your computer."):
            write_to_console("Operation aborted.")
            return
    elif number_of_pixels >= 10 ** 7:
        if not confirm_working(original_width * pixel_image_width, original_height * pixel_image_height,
                               "This will take a large amount of time."):
            write_to_console("Operation aborted.")
            return

    write_to_console("Enter the desired title for the final image: ")
    name_result = input()

    # Получение степени видимости главного изображения
    write_to_console(
        "Enter the degree of 'visibility' of the main image. At 0, the image will not be visible, and at 1 "
        "the image will simply be enlarged by several times. The standard and most optimal value is 0.5.", True)

    while True:
        try:
            visible = float(input())
            break
        except ValueError:
            pass
    negative_visible = 1 - visible

    # Создание холста
    write_to_console("Creating an Image of the Right Size...")
    result = Image.new('RGB', (1, 1), color='red')
    try:
        result = Image.new('RGB', (original_width * pixel_image_width, original_height * pixel_image_height),
                           color='red')
    except MemoryError:
        write_to_console("The generated image is TOO large. Lower the resolution"
                         "images 'pixel.jpg' and 'source.jpg' and try again.")
    pixels = result.load()
    loading_final = (original_width - 1) / 100

    # Заполнение холста
    for x in range(original_width):
        loading = round(x / loading_final, 3)
        write_to_console(f"Processing - {loading}%")
        for y in range(original_height):
            r_original = visible * original_pixels[x, y][0]
            g_original = visible * original_pixels[x, y][1]
            b_original = visible * original_pixels[x, y][2]
            for pixelX in range(pixel_image_width):
                for pixelY in range(pixel_image_height):
                    pixel = pixel_image_pixels[pixelX, pixelY]
                    pixels[pixelX + pixel_image_width * x, pixelY + pixel_image_height * y] = (
                        int(pixel[0] * negative_visible + r_original), int(pixel[1] * negative_visible + g_original),
                        int(pixel[2] * negative_visible + b_original))
    write_to_console("Saving an image...")
    result.save(f"{name_result}.jpg")
    write_to_console("Image saved.")


# Написать что-то в консоль
def write_to_console(text, end=False):
    os.system('cls')
    if end:
        print(text)
    else:
        print(text, end='')


# Подтверждение какого-либо действия
def confirm_working(sizeX, sizeY, text):
    os.system('cls')
    print(
        f"An image of size {sizeX}x{sizeY} will be created. {text} Continue? (n/y)")
    while True:
        answer = input()
        if answer == "n":
            return False
        elif answer == "y":
            return True
        else:
            print("Enter the correct answer (n - no, y - yes)")


# Начало
if __name__ == '__main__':
    main()
