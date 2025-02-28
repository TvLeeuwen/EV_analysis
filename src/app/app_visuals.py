"""Definitions for data visualization in streamlit"""

# Imports ---------------------------------------------------------------------
import os
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from src.MSM.sto_generator import read_input, read_mat_to_df


# Defs ------------------------------------------------------------------------
def update_fig_layout(fig):
    fig.update_layout(
        # plot_bgcolor="white",
        height=700,
        # width=1000,
        xaxis_title="Time (s)",
        yaxis_title="Value",
        legend_title="Variables",
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1,
            xanchor="left",
            x=0,
            itemsizing="constant",
            traceorder="grouped",
        ),
    )


def visual_kinematics(dfs, c_scale, group_legend):
    """
    Plot kinematics to compare Moco track performance between input and output

    :param dfs list: list of dfs
    :param group_legend bool: [TODO:description]
    """
    df_minmax = pd.DataFrame(
        columns=[
            "Joint",
            "Min",
            "Max",
            "ROM",
        ]
    )
    fig = go.Figure()
    for i, df_path in enumerate(dfs):
        dataset = os.path.splitext(os.path.basename(df_path))[0]
        if os.path.splitext(df_path)[1] == ".mat":
            df = read_mat_to_df(df_path)
        elif os.path.splitext(df_path)[1] == ".mot":
            df, _ = read_input(df_path)

        colors = px.colors.sample_colorscale(
            c_scale,
            [n / (len(dfs) - 1) if len(dfs) > 1 else 0 for n in range(len(dfs))],
        )

        df_minmax.loc[len(df_minmax)] = [
            dataset,
            "-",
            "-",
            "-",
        ]

        for column in df.columns:
            # print(column)
            if (
                # column.strip() != "time"
                "hip_flexion" in column
                or "knee_angle" in column
                or "ankle_angle" in column
            ):
                legend = column if group_legend else f"{dataset}: {column.strip()}"
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df[column],
                        mode="lines",
                        line=dict(color=colors[i]),
                        name=f"{dataset}: {column.strip()}",
                        legendgroup=legend,
                        hovertext=column,
                    )
                )
                df_minmax.loc[len(df_minmax)] = [
                    column,
                    np.amin(df[column]),
                    np.amax(df[column]),
                    np.amax(df[column]) - np.amin(df[column]),
                ]

    update_fig_layout(fig)

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.write("ROM")
    st.table(df_minmax)


def visual_dynamics(dynamics_path, group_legend=False, color_map=None):
    if os.path.splitext(dynamics_path)[1] == ".sto":
        df, _ = read_input(dynamics_path)
    elif os.path.splitext(dynamics_path)[1] == ".json":
        df = pd.read_json(dynamics_path, orient="records", lines=True)
    else:
        print("Input file for dynamics visualisation not recognized, use .sto or .json")
        return

    r = False
    if not color_map:
        # Required for a consistent color index
        columns = set()
        for column in df.columns:
            if column != "time":
                columns.add(column.split("|")[0])
        colors = px.colors.sample_colorscale(
            "viridis", [n / (len(columns) - 1) for n in range(len(columns))]
        )
        color_map = {col: colors[i] for i, col in enumerate(columns)}
        r = True
    else:
        new_color_map = {}
        for col in df.columns:
            muscle = col.split("|")[0]
            for key, value in color_map.items():
                if muscle in key:
                    new_color_map[muscle] = value
        color_map = new_color_map

    fig = go.Figure()
    for column in df.columns:
        if column != "time":
            state_name = column.split("|")[1] if group_legend else column
            name = column.split("/")[-1]
            muscle = column.split("|")[0]
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df[column],
                    mode="lines",
                    line=dict(color=color_map[muscle]),
                    name=f"{column.split('/')[-1]}",
                    legendgroup=state_name,
                )
            )
    update_fig_layout(fig)

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    if r:
        return color_map
