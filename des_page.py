# des_page.py

import streamlit as st
from Cryptodome.Cipher import DES
from Cryptodome.Random import get_random_bytes
import time
from io import BytesIO


def des_encrypt_file(input_file, key):
    start_encrypt = time.perf_counter()  # Start timing in seconds
    chunk_size = 64 * 1024  # 64 KB
    init_vector = get_random_bytes(8)  # 64 bits IV for DES

    # Create DES cipher object
    cipher = DES.new(key, DES.MODE_CBC, iv=init_vector)

    # Create a BytesIO buffer to hold the encrypted data
    encrypted_file = BytesIO()
    encrypted_file.write(init_vector)

    # Read the file in chunks and encrypt
    while True:
        chunk = input_file.read(chunk_size)
        if len(chunk) == 0:
            break
        elif len(chunk) % 8 != 0:  # Padding to make chunk size multiple of 8
            chunk += b" " * (8 - len(chunk) % 8)
        encrypted_file.write(cipher.encrypt(chunk))

    encrypted_file.seek(0)  # Reset pointer to the start
    end_encrypt = time.perf_counter()  # End timing in seconds
    return encrypted_file, end_encrypt - start_encrypt  # Return elapsed time


def des_decrypt_file(input_file, key):
    chunk_size = 64 * 1024  # 64 KB
    start_decrypt = time.perf_counter()  # Start timing in seconds

    # Read IV from the beginning of the input file
    init_vector = input_file.read(8)
    cipher = DES.new(key, DES.MODE_CBC, iv=init_vector)

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


def show_des_page():
    st.title("DES Encryption")

    # File uploader for images
    uploaded_file = st.file_uploader(
        label="Upload an image for DES encryption", type=["png", "jpeg", "jpg"]
    )

    if uploaded_file:
        prv = "super_secret"  # DES key should be 8 bytes
        key = prv.encode("utf-8")[:8]  # Limit key to 8 bytes

        # Encrypt the uploaded file when the "Encrypt DES" button is clicked
        if st.button("Encrypt DES"):
            encrypted_file, encryption_time = des_encrypt_file(uploaded_file, key)
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

        # File uploader for encrypted files
        encrypted_file_uploader = st.file_uploader(
            label="Upload an encrypted file to decrypt", type=["txt"]
        )

        if encrypted_file_uploader:
            # Decrypt the file when "Decrypt DES" button is clicked
            if st.button("Decrypt DES"):
                decrypted_file, decryption_time = des_decrypt_file(
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
    show_des_page()
