from PIL import Image
import numpy as np
import random
import os

def xor_pixel(value, key):
    return value ^ key

def shuffle_pixels(image_array, key):
    h, w, c = image_array.shape
    flat_pixels = image_array.reshape(-1, c)
    indices = list(range(len(flat_pixels)))

    random.seed(key)
    random.shuffle(indices)
    shuffled = flat_pixels[indices]
    return shuffled.reshape((h, w, c)), indices

def unshuffle_pixels(shuffled_array, key):
    h, w, c = shuffled_array.shape
    flat_shuffled = shuffled_array.reshape(-1, c)
    indices = list(range(len(flat_shuffled)))

    random.seed(key)
    random.shuffle(indices)

    # Reverse index mapping
    unshuffled = np.zeros_like(flat_shuffled)
    for i, shuffled_i in enumerate(indices):
        unshuffled[shuffled_i] = flat_shuffled[i]
    return unshuffled.reshape((h, w, c))

def encrypt_image(input_path, output_path, key):
    if not os.path.exists(input_path):
        print("⚠️ Input file not found.")
        return

    image = Image.open(input_path).convert("RGB")
    image_array = np.array(image)

    # XOR operation
    xor_array = image_array ^ key

    # Pixel shuffling
    shuffled_array, _ = shuffle_pixels(xor_array, key)

    encrypted_image = Image.fromarray(shuffled_array)
    encrypted_image.save(output_path)
    print(f"🔒 Encrypted image saved to: {output_path}")

def decrypt_image(input_path, output_path, key):
    if not os.path.exists(input_path):
        print("⚠️ Input file not found.")
        return

    image = Image.open(input_path).convert("RGB")
    image_array = np.array(image)

    # Reverse shuffling
    unshuffled_array = unshuffle_pixels(image_array, key)

    # XOR to decrypt
    decrypted_array = unshuffled_array ^ key

    decrypted_image = Image.fromarray(decrypted_array)
    decrypted_image.save(output_path)
    print(f"🔓 Decrypted image saved to: {output_path}")

def main():
    print("\n=== 🧊 Unique Image Encryption Tool ===")
    while True:
        print("\n1. Encrypt Image\n2. Decrypt Image\n3. Exit")
        choice = input("Enter choice (1/2/3): ")

        if choice == '1':
            input_path = input("Enter input image path: ").strip()
            output_path = input("Enter output (encrypted) image path: ").strip()
            key = int(input("Enter encryption key (number): "))
            encrypt_image(input_path, output_path, key)

        elif choice == '2':
            input_path = input("Enter encrypted image path: ").strip()
            output_path = input("Enter output (decrypted) image path: ").strip()
            key = int(input("Enter encryption key (number): "))
            decrypt_image(input_path, output_path, key)

        elif choice == '3':
            print("Goodbye 👋")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
