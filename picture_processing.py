import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox


def rotate_images(input_directory, output_directory, angles, background_color=(255, 255, 255)):
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(input_directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            input_path = os.path.join(input_directory, filename)
            img = Image.open(input_path)

            for angle in angles:
                rotated_img = img.rotate(angle, expand=True, fillcolor=background_color)
                new_background = Image.new('RGB', img.size, background_color)
                offset_x = (new_background.width - rotated_img.width) // 2
                offset_y = (new_background.height - rotated_img.height) // 2
                new_background.paste(rotated_img, (offset_x, offset_y))

                base_name, ext = os.path.splitext(filename)
                new_filename = f"{base_name}_rotated_{angle}{ext}"
                output_path = os.path.join(output_directory, new_filename)
                new_background.save(output_path)


def browse_input_directory():
    dir_path = filedialog.askdirectory()
    input_dir_entry.delete(0, tk.END)
    input_dir_entry.insert(0, dir_path)


def browse_output_directory():
    dir_path = filedialog.askdirectory()
    output_dir_entry.delete(0, tk.END)
    output_dir_entry.insert(0, dir_path)


def choose_background_color():
    color = colorchooser.askcolor(title="选择背景颜色")[1]
    if color:
        bg_color_entry.delete(0, tk.END)
        bg_color_entry.insert(0, color)


def extract_color_from_image():
    img_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if img_path:
        img = Image.open(img_path)
        avg_color = tuple(map(int, img.resize((1, 1)).getpixel((0, 0))))
        color_hex = "#{:02x}{:02x}{:02x}".format(*avg_color)
        bg_color_entry.delete(0, tk.END)
        bg_color_entry.insert(0, color_hex)


def start_rotation():
    input_directory = input_dir_entry.get()
    output_directory = output_dir_entry.get()
    angles_str = angles_entry.get()

    try:
        angles = list(map(int, angles_str.split(',')))
    except ValueError:
        messagebox.showerror("输入错误", "请确保旋转角度是用英文逗号分隔的整数！")
        return

    background_color = bg_color_entry.get()
    if not background_color.startswith('#'):
        messagebox.showerror("输入错误", "请确保背景颜色是有效的十六进制颜色！")
        return

    rotate_images(input_directory, output_directory, angles, background_color)
    messagebox.showinfo("完成", "图像处理完成！")


# 创建主窗口
root = tk.Tk()
root.title("AI奇异果")

# 设置窗口图标
root.iconphoto(False, tk.PhotoImage(file='img/AI奇异果LOGO.png'))  # 使用 .png 格式的图标
# 或者使用以下代码设置 .ico 格式的图标
# root.iconbitmap('path/to/your/icon.ico')

# 输入目录
tk.Label(root, text="图像输入目录:").grid(row=0, column=0)
input_dir_entry = tk.Entry(root, width=50)
input_dir_entry.grid(row=0, column=1)
tk.Button(root, text="浏览", command=browse_input_directory).grid(row=0, column=2)

# 输出目录
tk.Label(root, text="图像输出目录:").grid(row=1, column=0)
output_dir_entry = tk.Entry(root, width=50)
output_dir_entry.grid(row=1, column=1)
tk.Button(root, text="浏览", command=browse_output_directory).grid(row=1, column=2)

# 自定义旋转角度
tk.Label(root, text="旋转角度 (用英文逗号分隔):").grid(row=2, column=0)
angles_entry = tk.Entry(root, width=50)
angles_entry.grid(row=2, column=1)

# 背景颜色
tk.Label(root, text="背景颜色:").grid(row=3, column=0)
bg_color_entry = tk.Entry(root, width=50)
bg_color_entry.grid(row=3, column=1)
tk.Button(root, text="选择颜色", command=choose_background_color).grid(row=3, column=2)
tk.Button(root, text="提取颜色", command=extract_color_from_image).grid(row=4, column=2)

# 开始按钮
tk.Button(root, text="开始处理", command=start_rotation).grid(row=5, columnspan=3)

# 启动主循环
root.mainloop()
