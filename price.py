import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import math

def round_value(value, rounding_type, digit):
    """指定された丸め方法と桁で値を丸める"""
    scale = digit
    if rounding_type == 'round':
        return round(value / scale) * scale
    elif rounding_type == 'floor':
        return math.floor(value / scale) * scale
    elif rounding_type == 'ceil':
        return math.ceil(value / scale) * scale
    else:
        return value

def calculate_selling_price():
    """売価・利益率・利益額を計算して表示"""
    try:
        cost = float(entry_cost.get())
        if cost < 0:
            raise ValueError("仕入れ値は0以上の値を入力してください。")
        
        margin = float(entry_margin.get())
        if not (0 <= margin < 100):
            raise ValueError("利益率は0%以上、100%未満で入力してください。")
        
        # 利益率が100%の場合のゼロ除算を防ぐ
        if margin == 100:
            raise ZeroDivisionError 
        
        base_selling_price = cost / (1 - margin / 100)
        
        selected_rounding_type = rounding_var.get()
        selected_digit_text = digit_var.get()
        
        digit_map = {
            "1の位": 1,
            "10の位": 10,
            "100の位": 100,
            "1000の位": 1000
        }
        # 辞書に存在しない場合のデフォルト値を1に設定
        digit_value = digit_map.get(selected_digit_text, 1) 
        
        rounded_selling_price = round_value(base_selling_price, selected_rounding_type, digit_value)
        
        # 利益計算の妥当性を確保
        if rounded_selling_price > 0:
            final_profit_margin = ((rounded_selling_price - cost) / rounded_selling_price) * 100
            profit_amount = rounded_selling_price - cost
        else:
            final_profit_margin = 0.0
            # 売価が0の場合、利益はマイナスの仕入れ値になる
            profit_amount = -cost 
            # 仕入れ値も0なら利益も0
            if cost == 0:
                profit_amount = 0.0 
            
        label_result.config(
            text=(
                f"売価（計算値）: ¥{base_selling_price:,.2f}\n"
                f"売価（調整後）: ¥{rounded_selling_price:,.0f}\n"
                f"最終利益率: {final_profit_margin:,.2f} %\n"
                f"利益額: ¥{profit_amount:,.0f}"
            ),
            foreground="blue"
        )

    except ValueError as e:
        messagebox.showerror("入力エラー", f"入力値が無効です。\n{e}")
        label_result.config(text="売価: エラー", foreground="red")
    except ZeroDivisionError:
        messagebox.showerror("計算エラー", "利益率が100%に近すぎます。計算できません。")
        label_result.config(text="売価: エラー", foreground="red")
    except Exception as e:
        # 予期せぬエラーをキャッチ
        messagebox.showerror("予期せぬエラー", f"予期せぬエラーが発生しました: {e}")
        label_result.config(text="売価: エラー", foreground="red")

def clear_fields():
    entry_cost.delete(0, tk.END)
    entry_margin.delete(0, tk.END)
    label_result.config(text="売価: ", foreground="black")
    rounding_var.set('round')
    digit_var.set('1の位')
    entry_cost.focus_set() # クリア後に仕入れ値フィールドにフォーカスを設定

# --- GUI構築 ---
root = tk.Tk()
root.title("売価計算ツール")
root.geometry("450x430")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")

try:
    bg_color = style.lookup('TFrame', 'background')
    root.configure(bg=bg_color)
except tk.TclError:
    # テーマが背景色を提供しない場合のフォールバック
    root.configure(bg="#f0f0f0")

# --- 入力 ---
input_frame = ttk.LabelFrame(root, text="入力")
input_frame.pack(padx=10, pady=5, fill="x")

ttk.Label(input_frame, text="仕入れ値（円）:").grid(row=0, column=0, pady=5, padx=5, sticky="w")
entry_cost = ttk.Entry(input_frame)
entry_cost.grid(row=0, column=1, pady=5, padx=5, sticky="ew")

ttk.Label(input_frame, text="利益率（%）:").grid(row=1, column=0, pady=5, padx=5, sticky="w")
entry_margin = ttk.Entry(input_frame)
entry_margin.grid(row=1, column=1, pady=5, padx=5, sticky="ew")

input_frame.grid_columnconfigure(1, weight=1)

# --- 丸め設定 ---
round_settings_frame = ttk.LabelFrame(root, text="丸め設定")
round_settings_frame.pack(padx=10, pady=5, fill="x")

ttk.Label(round_settings_frame, text="丸め処理:").grid(row=0, column=0, pady=5, padx=5, sticky="w")
rounding_var = tk.StringVar(value='round')
ttk.Radiobutton(round_settings_frame, text="四捨五入", variable=rounding_var, value="round").grid(row=0, column=1, sticky="w")
ttk.Radiobutton(round_settings_frame, text="切り捨て", variable=rounding_var, value="floor").grid(row=0, column=2, sticky="w")
ttk.Radiobutton(round_settings_frame, text="切り上げ", variable=rounding_var, value="ceil").grid(row=0, column=3, sticky="w")

ttk.Label(round_settings_frame, text="丸める桁:").grid(row=1, column=0, pady=5, padx=5, sticky="w")
digit_options = ["1の位", "10の位", "100の位", "1000の位"]
digit_var = tk.StringVar(value=digit_options[0])
digit_menu = ttk.Combobox(round_settings_frame, textvariable=digit_var, values=digit_options, state="readonly")
digit_menu.grid(row=1, column=1, columnspan=3, pady=5, padx=5, sticky="ew")
digit_menu.set(digit_options[0]) # 初期表示を正しく設定

round_settings_frame.grid_columnconfigure(1, weight=1)

# --- ボタン ---
button_frame = ttk.Frame(root)
button_frame.pack(pady=5)

ttk.Button(button_frame, text="売価を計算", command=calculate_selling_price).pack(side=tk.LEFT, padx=5)
ttk.Button(button_frame, text="クリア", command=clear_fields).pack(side=tk.LEFT, padx=5)

# --- 結果表示 ---
label_result = ttk.Label(root, text="売価: ", font=("Helvetica", 12, "bold"))
label_result.pack(pady=10)

# アプリケーション起動時に最初の入力フィールドにフォーカスを設定
entry_cost.focus_set()

root.mainloop()