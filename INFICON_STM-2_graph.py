# -------------------------------------------------------------
# Graphing INFICON STM-2 USB Thin Film Rate/Thickness Monitor Log Files: Displaying Average Rate in Graph Title
# This program was developed with the assistance of ChatGPT and Copilot.
# Copyright (c) 2024 NAGATA Mizuho. Institute of Laser Engineering, Osaka University.
# Created on: 2024-05-15
# Last updated on: 2025-05-16
# -------------------------------------------------------------

import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import os
import sys

# Constants for deposition rate calculations
# 蒸着レート計算用の定数
SHUTTER_OPEN_THRESHOLD = 0.1  # Å/s - Threshold to determine if shutter is open
ANGSTROM_TO_NM_CONVERSION = 0.1  # Conversion factor from Å/s to nm/s

# Configure Japanese font for matplotlib (cross-platform support)
# 日本語フォント設定（クロスプラットフォーム対応）
def setup_japanese_font():
    """Setup Japanese font for matplotlib with cross-platform support."""
    font_paths = []
    
    if sys.platform == 'win32':
        # Windows fonts
        font_paths = [
            "C:/Windows/Fonts/BIZ-UDGothicR.ttc",
            "C:/Windows/Fonts/msgothic.ttc",
            "C:/Windows/Fonts/YuGothR.ttc"
        ]
    elif sys.platform == 'darwin':
        # macOS fonts
        font_paths = [
            "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
            "/Library/Fonts/Osaka.ttf"
        ]
    else:
        # Linux fonts
        font_paths = [
            "/usr/share/fonts/truetype/takao-gothic/TakaoPGothic.ttf",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
        ]
    
    # Try each font path
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                fp = FontProperties(fname=font_path)
                plt.rcParams['font.family'] = fp.get_name()
                return
            except Exception:
                continue
    
    # Fallback: Use system default font
    # If no Japanese font found, matplotlib will use default font
    pass

# Setup font at module load time
setup_japanese_font()

def read_log_file(filename):
    """
    Read INFICON STM-2 log file and parse deposition data.
    
    Args:
        filename: Path to the log file
        
    Returns:
        tuple: (time, rate, thick, frequency, avg_rate_nm, open_duration)
               Returns (None, None, None, None, None, None) on error
    """
    try:
        time, rate, thick, frequency = [], [], [], []
        shutter_open_times = []
        shutter_open_rates = []

        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if line.startswith('Time'):
                    continue  # Skip header line
                if line.startswith('Stop Log'):
                    break  # Stop reading at end of data

                data = line.split(',')
                if len(data) < 4:
                    continue  # Skip invalid lines

                try:
                    t = float(data[0].strip())
                    r = float(data[1].strip())
                    th = float(data[2].strip())
                    f = float(data[3].strip())
                except (ValueError, IndexError) as e:
                    # Skip lines with invalid numeric data
                    continue

                time.append(t)
                rate.append(r)
                thick.append(th)
                frequency.append(f)

                # Determine if shutter is open based on deposition rate threshold
                # 蒸着レートが閾値以上の場合、シャッターが開いていると判断
                if r > SHUTTER_OPEN_THRESHOLD:
                    shutter_open_times.append(t)
                    shutter_open_rates.append(r)

        # Calculate average deposition rate (convert Å/s to nm/s)
        avg_rate_nm = np.mean(shutter_open_rates) * ANGSTROM_TO_NM_CONVERSION if shutter_open_rates else 0
        
        # Calculate shutter open duration
        shutter_open_duration = max(shutter_open_times) - min(shutter_open_times) if shutter_open_times else 0

        return time, rate, thick, frequency, avg_rate_nm, shutter_open_duration
        
    except FileNotFoundError:
        messagebox.showerror("Error", f"File not found: {filename}")
        return None, None, None, None, None, None
    except PermissionError:
        messagebox.showerror("Error", f"Permission denied: {filename}")
        return None, None, None, None, None, None
    except Exception as e:
        messagebox.showerror("Error", f"Error reading log file: {e}")
        return None, None, None, None, None, None

def plot_graph(x, y, title, x_label, y_label, color, avg_rate_nm, open_duration):
    """
    Plot a single graph with average rate and duration in the title.
    
    Args:
        x: Time data
        y: Y-axis data (rate, thickness, or frequency)
        title: Base title for the graph
        x_label: Label for x-axis
        y_label: Label for y-axis
        color: Line color
        avg_rate_nm: Pre-calculated average deposition rate in nm/s
        open_duration: Pre-calculated shutter open duration in seconds
    """
    try:
        # Add average rate and duration to title
        # グラフタイトルに平均蒸着レート(nm/s)とシャッター開時間(秒)を追加
        full_title = f'{title} (Avg Rate: {avg_rate_nm:.2f} nm/s, Open Duration: {open_duration:.1f} sec)'

        plt.figure(figsize=(8, 6))
        plt.plot(x, y, color=color)
        plt.title(full_title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Error plotting graph: {e}")

def plot_all_graphs_in_one_window(time, rate, thick, frequency, title, avg_rate_nm, open_duration):
    """
    Plot all three graphs (rate, thickness, frequency) in a single window.
    
    Args:
        time: Time data
        rate: Rate data
        thick: Thickness data
        frequency: Frequency data
        title: Base title for the graphs
        avg_rate_nm: Average deposition rate in nm/s
        open_duration: Shutter open duration in seconds
    """
    try:
        fig, axs = plt.subplots(3, 1, figsize=(10, 12))
        graph_title = f"{title} (Avg Rate: {avg_rate_nm:.2f} nm/s, Shutter Open: {open_duration:.1f} sec)"
        fig.suptitle(graph_title, fontsize=16)

        axs[0].plot(time, rate, color='blue')
        axs[0].set_title('Rate vs Time')
        axs[0].set_xlabel('Time [sec]')
        axs[0].set_ylabel('Rate [Å/S]')

        axs[1].plot(time, thick, color='green')
        axs[1].set_title('Thickness vs Time')
        axs[1].set_xlabel('Time [sec]')
        axs[1].set_ylabel('Thickness [Å]')

        axs[2].plot(time, frequency, color='red')
        axs[2].set_title('Frequency vs Time')
        axs[2].set_xlabel('Time [sec]')
        axs[2].set_ylabel('Frequency [Hz]')

        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Error plotting all graphs: {e}")

def select_file_and_plot():
    """Main function to select log file and display graphs."""
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(title="Select log file", filetypes=[('Log Files', '*.log')])
    if file_path:
        time, rate, thick, frequency, avg_rate_nm, open_duration = read_log_file(file_path)

        if not time:  # Check if read_log_file encountered an error
            return

        graph_title = simpledialog.askstring("Graph Title", "Enter graph title:")

        if graph_title:
            # Display each graph in a separate window
            plot_graph(time, rate, graph_title + ' (Rate vs Time)', 'Time [sec]', 'Rate [Å/S]', 
                      color='blue', avg_rate_nm=avg_rate_nm, open_duration=open_duration)
            plot_graph(time, thick, graph_title + ' (Thickness vs Time)', 'Time [sec]', 'Thickness [Å]', 
                      color='green', avg_rate_nm=avg_rate_nm, open_duration=open_duration)
            plot_graph(time, frequency, graph_title + ' (Frequency vs Time)', 'Time [sec]', 'Frequency [Hz]', 
                      color='red', avg_rate_nm=avg_rate_nm, open_duration=open_duration)

            # Three graphs in one window
            plot_all_graphs_in_one_window(time, rate, thick, frequency, graph_title, avg_rate_nm, open_duration)

if __name__ == '__main__':
    select_file_and_plot()
