import tkinter as tk
from tkinter import filedialog
import os
import shutil
import markdown

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path.set(folder_selected)
    else:
        folder_path.set("没有选择文件夹")
    return folder_selected


def change_extension_to_txt(src_path, dest_path):
    entries = os.listdir(src_path)

    for entry in entries:
        full_path = os.path.join(src_path, entry)

        if os.path.isdir(full_path):
            new_dest_path = os.path.join(dest_path, entry)
            if not os.path.exists(new_dest_path):
                os.makedirs(new_dest_path)
            change_extension_to_txt(full_path, new_dest_path)
        else:
            base_name, ext = os.path.splitext(entry)
            if ext == '.md':
                try:
                    with open(full_path, 'r', encoding='utf-8') as file:
                        text = file.read()
                    html = markdown.markdown(text)

                    new_filename = f"{base_name}.html"
                    with open(os.path.join(dest_path, new_filename), 'w', encoding='utf-8') as file:
                        file.write('<meta charset="UTF-8">')
                        file.write(html)
                    new_full_path = os.path.join(dest_path, new_filename)
                except FileNotFoundError:
                    print(f"文件未找到: {full_path}")
                except Exception as e:
                    print(f"处理 {full_path} 文件时发生错误: {e}")

            elif (ext == '.jpg' or ext=='.doc' or ext=='.xlsx' or ext=='.pdf' or ext=='.png'
                  or ext=='.html' or ext=='.ppt' or ext=='.pptx' or ext=='.csv' or ext=='.exe'
                  or ext=='.mp4'or ext=='.mp3'or ext=='.et' or ext=='.ett' or ext=='.bmp'
                  or ext=='.dot' or ext=='.wpt' or ext=='.wps' or ext=='.docx' or ext=='.xlt'):
                new_filename = entry
                new_full_path = os.path.join(dest_path, new_filename)
                shutil.copy(full_path, new_full_path)


            else:
                new_filename = f"{base_name}.txt"
                new_full_path = os.path.join(dest_path, new_filename)
                shutil.copy(full_path, new_full_path)

            print(f"Copied {full_path} to {new_full_path}")

def list_files_in_directory(path):
    new_path = r'D:\copy_file'

    if not os.path.exists(new_path):
        os.makedirs(new_path)

    change_extension_to_txt(path, new_path)


root = tk.Tk()


folder_path = tk.StringVar()
label = tk.Label(root, textvariable=folder_path)
label.pack()

path=r'C:\Users\thinkpad\Desktop\6666'
path = select_folder()
print(path)


list_files_in_directory(path)

root.destroy()