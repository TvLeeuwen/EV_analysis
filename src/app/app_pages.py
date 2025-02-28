# Imports ---------------------------------------------------------------------
import os
import streamlit as st
from src.app.app_io import (
    kine_uploader,
    dir_downloader,
)
from src.app.app_functions import (
    calculate_total_muscle_force,
    clear_output,
)
from src.app.app_visuals import (
    visual_kinematics,
    visual_dynamics,
)

sts = st.session_state


# Defs ------------------------------------------------------------------------
def page_home():
    st.title("Input")
    st.write(f"Home directory: {sts.app_path}")

    with st.expander("Debug: Show states", expanded=False):
        st.write(sts)

    st.subheader("Kinematics file")
    kine_uploader()


def page_kinematics():
    st.title("Kinematics")

    if (
        sts.kine_path is not None
    ):

        if sts.kine_path:
            group_kine = st.toggle("Group kinematics legend", value=True)
            c_scale = st.radio(
                "Iteration:",
                ["Rainbow", "Viridis", "Turbo", "Thermal", "Plasma"],
                horizontal=True,
            )

            visual_kinematics(
                sts.kine_path,
                c_scale,
                group_kine,
            )
        else:
            st.write("Please upload your kinematics files under :rainbow[Input]")


def page_dynamics():
    st.header("Dynamics")

    st.write("Nothing to see here, yet...")
    # if sts.moco_solution_dynamics_path is not None and os.path.exists(
    #     sts.moco_solution_dynamics_path
    # ):
    #     group_legend = st.toggle("Group dynamics legend", value=True)
    #     color_map = visual_dynamics(
    #         sts.moco_solution_dynamics_path,
    #         group_legend,
    #     )
    #     st.subheader("Total muscle force")
    #     if st.button("Calculate total muscle force"):
    #         sts.muscle_forces_path = calculate_total_muscle_force(
    #             sts.moco_solution_dynamics_path,
    #         )

    # if sts.muscle_forces_path is not None and os.path.exists(sts.muscle_forces_path):
    #     visual_dynamics(
    #         sts.muscle_forces_path,
    #         color_map=color_map,
    #     )

    # else:
    #     st.write(
    #         "No dynamics detected. Run track kinematics under :rainbow[Kinematics]"
    #     )


def page_output():
    st.title("Output")
    st.write(f"Output directory: {sts.output_path}")

    output_files = [
        f
        for f in sorted(os.listdir(sts.output_path), key=lambda x: (x.lower(), len(x)))
        if os.path.isfile(os.path.join(sts.output_path, f))
    ]

    if output_files:
        dir_downloader(
            sts.output_path,
            "Output",
            download_name="dir",
        )

        if st.button(":red[Clear all output]"):
            clear_output("all")
            st.rerun()

        st.subheader("Files")
        if st.button(":red[Clear files]"):
            clear_output("files")

        st.subheader("Download files")

        for file_name in output_files:
            st.write(file_name)
            # with open(os.path.join(sts.output_path, file_name), "rb") as file:
            #     file_data = file.read()
            #     st.download_button(
            #         label=f"{file_name}",
            #         data=file_data,
            #         file_name=file_name,
            #     )

        st.subheader("Remove files", divider="red")
        for file_name in output_files:
            if st.button(f":red[{file_name}]"):
                clear_output("file", file_name)

        st.subheader("Folders")
        if st.button(":red[Clear folders]"):
            clear_output("dirs")

        [
            dir_downloader(os.path.join(sts.output_path, dir), dir, show_files=True)
            for dir in os.listdir(sts.output_path)
            if os.path.isdir(os.path.join(sts.output_path, dir))
        ]

    else:
        st.write("Output folder is empty")
