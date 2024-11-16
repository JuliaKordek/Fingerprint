import cv2
import numpy as np
from tkinter import Tk, Label, Button, filedialog, messagebox, Frame
from matplotlib import pyplot as plt


# Function for thinning using OpenCV's ximgproc
def thin_image_opencv(binary_image):
    """Cienkowanie obrazu za pomocą cv2.ximgproc.thinning"""
    if binary_image.dtype != np.uint8:
        binary_image = binary_image.astype(np.uint8)
    thinned = cv2.ximgproc.thinning(binary_image, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN)
    return thinned


# Function to process the fingerprint image
def process_fingerprint(file_path):
    try:
        # Load the image
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise ValueError("Nie można wczytać obrazu.")

        # Preprocess the image
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        _, binary_image = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        thinned_image = thin_image_opencv(binary_image)

        # Display results
        plt.figure(figsize=(15, 5))
        plt.subplot(1, 3, 1)
        plt.title("Original Image")
        plt.imshow(image, cmap="gray")
        plt.axis("off")

        plt.subplot(1, 3, 2)
        plt.title("Binary Image")
        plt.imshow(binary_image, cmap="gray")
        plt.axis("off")

        plt.subplot(1, 3, 3)
        plt.title("Thinned Image")
        plt.imshow(thinned_image, cmap="gray")
        plt.axis("off")

        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się przetworzyć obrazu: {e}")


# Function to handle file selection
def select_file():
    file_path = filedialog.askopenfilename(
        title="Wybierz obraz odcisku palca",
        filetypes=[("Obrazy", "*.jpg;*.png;*.jpeg"), ("Wszystkie pliki", "*.*")]
    )
    if file_path:
        file_label.config(text=f"Wybrano plik: {file_path}")
        start_button.config(state="normal")  # Aktywuj przycisk po wybraniu pliku
        return file_path
    else:
        file_label.config(text="Nie wybrano pliku.")
        start_button.config(state="disabled")  # Dezaktywuj przycisk


# Initialize the GUI
def main():
    global file_label, start_button
    root = Tk()
    root.title("System Analizy Odcisków Palców")
    root.geometry("600x400")
    root.configure(bg="#F7F7F7")
    root.resizable(False, False)

    # Header
    header_frame = Frame(root, bg="#007BFF", height=70)
    header_frame.pack(fill="x")
    header_label = Label(header_frame, text="System Analizy Odcisków Palców", bg="#007BFF", fg="white",
                         font=("Arial", 18, "bold"))
    header_label.pack(pady=20)

    # Main content
    content_frame = Frame(root, bg="#F7F7F7")
    content_frame.pack(pady=20)

    # File selection
    select_button = Button(content_frame, text="Wybierz obraz odcisku", command=lambda: select_file(),
                           bg="#007BFF", fg="white", font=("Arial", 12), relief="flat", padx=10, pady=5)
    select_button.pack(pady=10)

    file_label = Label(content_frame, text="Nie wybrano pliku.", bg="#F7F7F7", fg="#333333", font=("Arial", 10))
    file_label.pack(pady=5)

    # Start processing button
    start_button = Button(content_frame, text="Rozpocznij ekstrakcję",
                          command=lambda: process_fingerprint(file_label.cget("text").replace("Wybrano plik: ", "")),
                          bg="#28A745", fg="white", font=("Arial", 12), relief="flat", padx=10, pady=5)
    start_button.config(state="disabled")  # Nieaktywny dopóki plik nie zostanie wybrany
    start_button.pack(pady=20)

    # Footer
    footer_frame = Frame(root, bg="#F7F7F7", height=50)
    footer_frame.pack(side="bottom", fill="x")
    footer_label = Label(footer_frame, text="© 2024 System Analizy Biometrycznej", bg="#F7F7F7",
                         fg="#777777", font=("Arial", 8))
    footer_label.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
