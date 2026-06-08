# -------------------------------------------------------------
# Graphing INFICON STM-2 USB Thin Film Rate/Thickness Monitor Log Files: Displaying Average Rate in Graph Title
# This program was developed with the assistance of ChatGPT and Copilot.
# Copyright (c) 2024 NAGATA Mizuho. Institute of Laser Engineering, Osaka University.
# Created on: 2024-05-15
# Last updated on: 2025-06-09
# -------------------------------------------------------------

import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np

# 日本語フォントを指定
font_path = "C:/Windows/Fonts/BIZ-UDGothicR.ttc"
fp = FontProperties(fname=font_path)
plt.rcParams["font.family"] = fp.get_name()


def read_log_file(filename):
    try:
        time, rate, thick, frequency = [], [], [], []
        shutter_open_times = []  # シャッター開閉のタイミングを記録（r > 0.2 で判定）
        shutter_open_rates = []  # 平均レート計算用のデータを蓄積（r >= 0.1 で判定）

        current_time_offset = 0.0
        last_time_in_run = 0.0

        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if line.startswith("Start Log"):
                    if time:
                        current_time_offset += last_time_in_run
                    continue

                if (
                    line.startswith("Time")
                    or line.startswith("Stop Log")
                    or not line.strip()
                ):
                    continue

                data = line.split(",")
                if len(data) >= 4:
                    try:
                        raw_time = float(data[0].strip())
                        last_time_in_run = raw_time

                        actual_time = raw_time + current_time_offset
                        r = float(data[1].strip())
                        t = float(data[2].strip())
                        f = float(data[3].strip())

                        time.append(actual_time)
                        rate.append(r)
                        thick.append(t)
                        frequency.append(f)

                        # ─── 二つの条件の両立処理 ───

                        # 条件1: 0.2 Å/s 超でおおよそのシャッター開放「時刻」を切り出す
                        if r > 0.2:
                            shutter_open_times.append(actual_time)

                        # 条件2: 平均レートの計算には、膜厚に寄与する 0.1 Å/s 以上のデータをすべて抽出する
                        if r >= 0.1:
                            shutter_open_rates.append(r)

                    except ValueError:
                        continue

        if not time:
            messagebox.showerror("Error", "No valid data found in the log file.")
            return [], [], [], [], 0, 0

        # 平均レートとシャッター開放時間の計算
        # 0.1 Å/s 以上のデータが存在すれば平均を算出
        if shutter_open_rates:
            avg_rate_nm = np.mean(shutter_open_rates) / 10
        else:
            avg_rate_nm = 0

        # 0.2 Å/s 超で検知したシャッターの最初と最後の差から開放時間を算出
        if shutter_open_times:
            open_duration = shutter_open_times[-1] - shutter_open_times[0]
        else:
            open_duration = 0

        return time, rate, thick, frequency, avg_rate_nm, open_duration

    except Exception as e:
        messagebox.showerror("Error", f"Error reading log file: {e}")
        return [], [], [], [], 0, 0


def plot_graph(x, y, title, x_label, y_label, color):
    try:
        # 蒸着レートが有意の値（例: 0.2 Å/s 以上）の場合、シャッターが開いていると判断
        shutter_open_times = [x[i] for i in range(len(y)) if y[i] > 0.2]
        shutter_open_rates = [y[i] for i in range(len(y)) if y[i] > 0.2]

        avg_rate_nm = (
            np.mean(shutter_open_rates) * 0.1 if shutter_open_rates else 0
        )  # nm/s に変換
        open_duration = (
            (max(shutter_open_times) - min(shutter_open_times))
            if shutter_open_times
            else 0
        )

        # グラフタイトルに平均蒸着レート(nm/s)とシャッター開時間(秒)を追加
        title = f"{title} (Avg Rate: {avg_rate_nm:.2f} nm/s, Open Duration: {open_duration:.1f} sec)"

        plt.figure(figsize=(8, 6))
        plt.plot(x, y, color=color)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Error plotting graph: {e}")


def plot_all_graphs_in_one_window(
    time, rate, thick, frequency, title, avg_rate_nm, open_duration
):
    try:
        fig, axs = plt.subplots(3, 1, figsize=(10, 12))
        graph_title = f"{title} (Avg Rate: {avg_rate_nm:.2f} nm/s, Shutter Open: {open_duration:.1f} sec)"
        fig.suptitle(graph_title, fontsize=16)

        axs[0].plot(time, rate, color="blue")
        axs[0].set_title("Rate vs Time")
        axs[0].set_xlabel("Time [sec]")
        axs[0].set_ylabel("Rate [Å/S]")

        axs[1].plot(time, thick, color="green")
        axs[1].set_title("Thickness vs Time")
        axs[1].set_xlabel("Time [sec]")
        axs[1].set_ylabel("Thickness [Å]")

        axs[2].plot(time, frequency, color="red")
        axs[2].set_title("Frequency vs Time")
        axs[2].set_xlabel("Time [sec]")
        axs[2].set_ylabel("Frequency [Hz]")

        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Error plotting all graphs: {e}")


def select_file_and_plot():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select log file", filetypes=[("Log Files", "*.log")]
    )
    if file_path:
        time, rate, thick, frequency, avg_rate_nm, open_duration = read_log_file(
            file_path
        )

        if not time:  # Check if read_log_file encountered an error
            return

        graph_title = simpledialog.askstring("Graph Title", "Enter graph title:")

        if graph_title:
            # Display each graph in a separate window
            plot_graph(
                time,
                rate,
                graph_title + " (Rate vs Time)",
                "Time [sec]",
                "Rate [Å/S]",
                color="blue",
            )
            plot_graph(
                time,
                thick,
                graph_title + " (Thickness vs Time)",
                "Time [sec]",
                "Thickness [Å]",
                color="green",
            )
            plot_graph(
                time,
                frequency,
                graph_title + " (Frequency vs Time)",
                "Time [sec]",
                "Frequency [Hz]",
                color="red",
            )

            # Three graphs in one window
            plot_all_graphs_in_one_window(
                time, rate, thick, frequency, graph_title, avg_rate_nm, open_duration
            )


if __name__ == "__main__":
    select_file_and_plot()
