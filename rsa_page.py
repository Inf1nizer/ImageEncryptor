import streamlit as st
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from io import BytesIO
import time


def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key


def encrypt_file(input_file, public_key):
    cipher = PKCS1_OAEP.new(RSA.import_key(public_key))
    encrypted_file = BytesIO()

    # Start timing the encryption process
    start_time = time.perf_counter()

    while True:
        chunk = input_file.read(214)  # 214 bytes max for 2048-bit RSA
        if not chunk:
            break
        encrypted_chunk = cipher.encrypt(chunk)
        encrypted_file.write(encrypted_chunk)

    encrypted_file.seek(0)  # Reset pointer to the start
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    return encrypted_file, elapsed_time


def decrypt_file(input_file, private_key):
    cipher = PKCS1_OAEP.new(RSA.import_key(private_key))
    decrypted_file = BytesIO()

    # Start timing the decryption process
    start_time = time.perf_counter()

    while True:
        chunk = input_file.read(256)  # 256 bytes for 2048-bit RSA
        if not chunk:
            break
        decrypted_chunk = cipher.decrypt(chunk)
        decrypted_file.write(decrypted_chunk)

    decrypted_file.seek(0)  # Reset pointer to the start
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    return decrypted_file, elapsed_time


def show_rsa_page():
    st.title("RSA Encryption")

    # Check if keys are already generated in session state
    if "private_key" not in st.session_state or "public_key" not in st.session_state:
        st.session_state.private_key, st.session_state.public_key = generate_rsa_keys()

    private_key = st.session_state.private_key
    public_key = st.session_state.public_key

    # Display the public key for encryption
    st.subheader("Public Key:")
    st.text(public_key.decode())

    # File uploader for images
    uploaded_file = st.file_uploader(
        label="Upload an image for RSA encryption", type=["png", "jpeg", "jpg"]
    )

    if uploaded_file:
        # Encrypt the uploaded file when the "Encrypt RSA" button is clicked
        if st.button("Encrypt RSA"):
            encrypted_file, encryption_time = encrypt_file(uploaded_file, public_key)
            st.write(f"File encrypted successfully in {encryption_time:.4f} seconds.")

            # Provide an option to download the encrypted file
            st.download_button(
                label="Download Encrypted File",
                data=encrypted_file.getvalue(),  # Convert BytesIO to bytes
                file_name=f"encrypted_{uploaded_file.name}.bin",
                mime="application/octet-stream",
            )

    # File uploader for encrypted files
    encrypted_file_uploader = st.file_uploader(
        label="Upload an encrypted file to decrypt", type=["bin"]
    )

    if encrypted_file_uploader:
        # Decrypt the file when "Decrypt RSA" button is clicked
        if st.button("Decrypt RSA"):
            decrypted_file, decryption_time = decrypt_file(
                encrypted_file_uploader, private_key
            )
            st.write(f"File decrypted successfully in {decryption_time:.4f} seconds.")

            # Provide an option to download the decrypted file
            st.download_button(
                label="Download Decrypted Image",
                data=decrypted_file.getvalue(),  # Convert BytesIO to bytes
                file_name=f"decrypted_{uploaded_file.name}",
                mime="image/png",
            )

    if st.button("Go Back"):
        st.session_state.page = "main"  # Update the session state page variable
        st.query_params.update(page="main")  # Redirect using query params


if __name__ == "__main__":
    show_rsa_page()
