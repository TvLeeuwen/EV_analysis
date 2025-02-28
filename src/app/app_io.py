"""Functions to facilitate file I/O"""

# Imports ---------------------------------------------------------------------
import os
import io
import zipfile
import streamlit as st

sts = st.session_state


# Defs ------------------------------------------------------------------------
def setup_paths():
    # Folders -----------------------------------------------------------------
    if "app_path" not in sts:
        sts.app_path = os.getcwd()

    if "output_path" not in sts:
        sts.output_path = os.path.join(sts.app_path, "app/output")

    if "example_path" not in sts:
        sts.example_path = os.path.join(sts.app_path, "app/example")

    # Files -------------------------------------------------------------------
    if "kine_path" not in sts or not sts.kine_path:
        sts.kine_path = find_file_in_dir(
            sts.output_path,
            ".mot",
        )

    # Keep dir on homedir on refresh - may get stuck in /output
    if os.getcwd() == sts.app_path:
        os.makedirs(sts.output_path, exist_ok=True)
    elif os.getcwd() == sts.output_path:
        os.chdir(sts.app_path)


def find_file_in_dir(directory, string):
    for root, _, files in os.walk(directory):
        multiple_kine_files = []
        for file in files:
            if string in file:
                multiple_kine_files.append(os.path.join(sts.output_path, file))

        return multiple_kine_files


def write_to_output(file, output_dir, tag):
    tag = None if file.name[0 : len(tag)] == tag else tag
    file_name = f"{tag}_{file.name}" if tag else file.name
    file_path = os.path.join(output_dir, file_name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())

    return file_path


def kine_uploader():
    kine_path = st.file_uploader(
        "Drag and drop OR select all kinematics files here",
        accept_multiple_files=True,
        type=[
            ".mot",
        ],
    )
    # if kine_path is not None:
        # sts.kine_path = []
    for kine_ref in kine_path:
            # sts.kine_path.append(os.path.join(sts.output_path, kine_ref.name))
        write_to_output(
            kine_ref,
            sts.output_path,
            "",
        )


def zip_directory(folder_path):
    """Compress an entire directory into a ZIP file in memory."""
    buffer = io.BytesIO()  # Create a buffer to hold the ZIP file
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Add file to the ZIP archive with a relative path
                arcname = os.path.relpath(file_path, start=folder_path)
                zip_file.write(file_path, arcname=arcname)
    buffer.seek(0)  # Move to the start of the buffer
    return buffer.getvalue()


def dir_downloader(dir, dir_name, show_files=False, download_name="dir"):
    if os.path.exists(dir):
        download = (
            dir_name
        )
        st.download_button(
            label=f"Download {dir_name}.zip",
            data=zip_directory(dir),
            file_name=f"{download}.zip",
            mime="application/zip",
        )
        if show_files:
            st.write([file for file in os.listdir(dir)])
    else:
        st.error("The specified folder does not exist. Please check the path.")
