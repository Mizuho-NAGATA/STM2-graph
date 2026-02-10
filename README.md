# INFICON STM-2 Log Graphing (UNOFFICIAL)
This Python program is designed to graph the log files of the INFICON STM-2 USB Thin Film Rate/Thickness Monitor. One of the key features of this program is its ability to display the average rate in the graph title, providing a quick and easy way to understand the data.

このPythonプログラムはINFICON STM-2 USB薄膜レート/膜厚モニターのログファイルをグラフ化するためのものです。グラフタイトルに平均蒸着レート（0.1Å/s以上のときだけを抽出）と蒸着時間を表示することができます。

**注意：このプログラムはINFICON社の公式なものではありません。**

**Note: This program is not official INFICON.**

<img src="https://github.com/user-attachments/assets/a641cd46-c0b4-459e-8640-a15197d4259a" width="400">
<img src="https://github.com/user-attachments/assets/b0240cef-47a5-4da9-ba1c-040d399f5605" width="400">

## Features

- INFICON STM-2 USB 薄膜レート/厚さモニターのログファイルを読み取ります。
- レート、厚さ、周波数を時間経過とともにプロットします。
- 各グラフを別々のウィンドウに表示します。
- 3つのグラフを1つのウィンドウにまとめて比較しやすくします。
- 平均レートを計算し、グラフのタイトルに表示します。
- **クロスプラットフォーム対応**: Windows、macOS、Linux で動作します。

## Platform Support / プラットフォーム対応

This program now supports multiple platforms with automatic Japanese font detection:
- **Windows**: Uses BIZ UD Gothic, MS Gothic, or Yu Gothic fonts
- **macOS**: Uses Hiragino or Osaka fonts  
- **Linux**: Uses Takao Gothic or Noto Sans CJK fonts

このプログラムは複数のプラットフォームに対応し、日本語フォントを自動検出します：
- **Windows**: BIZ UD ゴシック、MSゴシック、游ゴシックフォントを使用
- **macOS**: ヒラギノまたはOsakaフォントを使用
- **Linux**: TakaoPゴシックまたはNoto Sans CJKフォントを使用

## Usage

1. Run the program: `python INFICON_STM-2_graph.py`
2. A dialog box will appear. Select the log file you want to graph.
3. Enter a title for the graph when prompted.
4. The program will display the graphs.

## Requirements

- Python 3
- tkinter
- matplotlib
- numpy

---

## 著者  
- Copyright (c) 2026 NAGATA Mizuho, 永田 みず穂 - Institute of Laser Engineering, The University of Osaka
---

## ライセンス License

- このプロジェクトはMITライセンスの下で公開されています。ライセンスの全文については、[LICENSE](https://github.com/Mizuho-NAGATA/STM2-graph/blob/main/LICENSE) をご覧ください。  
- This project is released under the MIT License. For the full text of the license, please see the LICENSE file.
---
