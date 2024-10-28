import streamlit as st
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import time
from io import BytesIO


def encrypt_file(input_file, key):
    start_encrypt = time.perf_counter()  # Start timing in seconds
    chunk_size = 64 * 1024  # 64 KB
    init_vector = get_random_bytes(16)  # 128 bits IV for AES

    # Create AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv=init_vector)

    # Create a BytesIO buffer to hold the encrypted data
    encrypted_file = BytesIO()
    encrypted_file.write(init_vector)

    # Read the file in chunks and encrypt
    while True:
        chunk = input_file.read(chunk_size)
        if len(chunk) == 0:
            break
        elif len(chunk) % 16 != 0:  # Padding to make chunk size multiple of 16
            chunk += b" " * (16 - len(chunk) % 16)
        encrypted_file.write(cipher.encrypt(chunk))

    encrypted_file.seek(0)  # Reset pointer to the start
    end_encrypt = time.perf_counter()  # End timing in seconds
    return encrypted_file, end_encrypt - start_encrypt  # Return elapsed time


def decrypt_file(input_file, key):
    chunk_size = 64 * 1024  # 64 KB
    start_decrypt = time.perf_counter()  # Start timing in seconds

    # Read IV from the beginning of the input file
    init_vector = input_file.read(16)
    cipher = AES.new(key, AES.MODE_CBC, iv=init_vector)

    # Create a BytesIO buffer to hold the decrypted data
    decrypted_file = BytesIO()

    # Read the file in chunks and decrypt
    while True:
        chunk = input_file.read(chunk_size)
        if len(chunk) == 0:
            break
        decrypted_file.write(cipher.decrypt(chunk))

    decrypted_file.seek(0)  # Reset pointer to the start
    end_decrypt = time.perf_counter()  # End timing in seconds
    return decrypted_file, end_decrypt - start_decrypt  # Return elapsed time


def show_aes_page():
    st.title("AES Encryption")

    # File uploader for images
    uploaded_file = st.file_uploader(
        label="Upload an image for AES encryption", type=["png", "jpeg", "jpg"]
    )

    if uploaded_file:
        prv = "super_secret_keysuper_secret_key"
        key = prv.encode("utf-8")[:32]  # Limit key to 32 bytes

        # Encrypt the uploaded file when the "Encrypt AES" button is clicked
        if st.button("Encrypt AES"):
            encrypted_file, encryption_time = encrypt_file(uploaded_file, key)
            st.write(
                f"Encryption time: {encryption_time:.4f} seconds"
            )  # Display time in seconds

            # Provide an option to download the encrypted file
            st.download_button(
                label="Download Encrypted File",
                data=encrypted_file.getvalue(),  # Convert BytesIO to bytes
                file_name=f"encrypted_{uploaded_file.name}.txt",
                mime="text/plain",
            )

        # If encrypted file exists, offer decryption
        encrypted_file_uploader = st.file_uploader(
            label="Upload an encrypted file to decrypt", type=["txt"]
        )

        if encrypted_file_uploader:
            # Decrypt the file when "Decrypt AES" button is clicked
            if st.button("Decrypt AES"):
                decrypted_file, decryption_time = decrypt_file(
                    encrypted_file_uploader, key
                )
                st.write(
                    f"Decryption time: {decryption_time:.4f} seconds"
                )  # Display time in seconds

                # Provide an option to download the decrypted file
                st.download_button(
                    label="Download Decrypted Image",
                    data=decrypted_file.getvalue(),  # Convert BytesIO to bytes
                    file_name=f"decrypted_{uploaded_file.name}",
                    mime="image/png",
                )

    # Go Back button
    if st.button("Go Back"):
        # Set the page to main without rerunning
        st.session_state.page = "main"  # Update the session state page variable

        # Redirect using query params (this will automatically trigger a rerun)
        st.query_params.update(
            page="main"
        )  # Update query parameters to navigate to main


if __name__ == "__main__":
    show_aes_page()
