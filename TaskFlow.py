
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb

# === Главное окно ===
root = tb.Window(themename="darkly")
root.title("Планировщик задач")
root.geometry("900x550")
root.configure(bg="#121212")

# ========== Глобальные настройки ==========
FONT_TITLE = ("Poppins", 14, "bold")  # Крупный шрифт для заголовка
FONT_DESC = ("Poppins", 10, "italic")  # Меньший шрифт для пояснения
BG_COLOR = "#121212"
FG_COLOR = "#E0E0E0"
BTN_COLOR = "#1E1E1E"
LIST_COLOR = "#1A1A1A"
MENU_COLOR = "#191919"

# ========== Фреймы ==========
frame_welcome = tk.Frame(root, bg=BG_COLOR)  # Экран приветствия
frame_main = tk.Frame(root, bg=BG_COLOR)  # Основной экран

# === Экран приветствия ===
label_welcome = tk.Label(frame_welcome, text="Добро пожаловать в\nПланировщик задач!",
                         font=("Poppins", 24), bg=BG_COLOR, fg=FG_COLOR)
label_welcome.pack(expand=True)

frame_welcome.pack(fill=tk.BOTH, expand=True)  # Показываем приветственный экран

# === Вертикальное боковое меню ===
menu_frame = tk.Frame(root, bg=MENU_COLOR, width=60)

def create_menu_button(icon, command):
    btn = tk.Button(menu_frame, text=icon, font=("Poppins", 14), bg=BTN_COLOR, fg=FG_COLOR,
                    relief="flat", bd=0, padx=10, pady=10, cursor="hand2",
                    activebackground="#292929", activeforeground=FG_COLOR,
                    command=command)
    btn.pack(fill=tk.X, pady=5)
    return btn

btn_tasks = create_menu_button("📌", lambda: show_frame(frame_main))
btn_settings = create_menu_button("⚙", lambda: messagebox.showinfo("Настройки", "Здесь будут настройки"))
btn_exit = create_menu_button("🚪", root.quit)

# === Функция переключения экранов ===
def show_frame(frame):
    frame_welcome.pack_forget()
    frame_main.pack_forget()
    menu_frame.pack(side=tk.LEFT, fill=tk.Y)  # Показываем меню
    frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

# === Основной экран ===
frame_tasks = tk.Frame(frame_main, bg=BG_COLOR)
frame_tasks.pack(fill=tk.BOTH, expand=True)

# Разделение на 2 части
frame_left = tk.Frame(frame_tasks, bg=BG_COLOR, width=400)
frame_right = tk.Frame(frame_tasks, bg=BG_COLOR)

frame_left.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10, expand=True)
frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10, expand=True)

# Поля для ввода задачи
label_task = tk.Label(frame_left, text="Заголовок задачи:", font=FONT_TITLE, bg=BG_COLOR, fg=FG_COLOR)
label_task.pack(anchor="w")

entry_task = tk.Entry(frame_left, font=FONT_TITLE, bg=LIST_COLOR, fg=FG_COLOR, bd=0, relief="flat")
entry_task.pack(fill=tk.X, pady=5, ipady=5)

label_desc = tk.Label(frame_left, text="Пояснение:", font=FONT_DESC, bg=BG_COLOR, fg=FG_COLOR)
label_desc.pack(anchor="w")

entry_desc = tk.Text(frame_left, font=FONT_DESC, bg=LIST_COLOR, fg=FG_COLOR, height=4, bd=0, relief="flat")
entry_desc.pack(fill=tk.X, pady=5)

# Функции задач
def add_task():
    task_text = entry_task.get().strip()
    desc_text = entry_desc.get("1.0", tk.END).strip()
    if task_text:
        full_text = (task_text, desc_text)  # Сохраняем отдельно заголовок и пояснение
        task_list.insert(tk.END, full_text)
        entry_task.delete(0, tk.END)
        entry_desc.delete(1.0, tk.END)

def delete_task():
    selected = task_list.curselection()
    if selected:
        task_list.delete(selected[0])
    else:
        messagebox.showwarning("Ошибка", "Выберите задачу для удаления")

def edit_task():
    selected = task_list.curselection()
    if selected:
        task_text, desc_text = task_list.get(selected[0])
        entry_task.delete(0, tk.END)
        entry_desc.delete(1.0, tk.END)
        entry_task.insert(tk.END, task_text)
        entry_desc.insert(tk.END, desc_text)
        task_list.delete(selected[0])

# Анимация кнопок
def on_enter(e):
    e.widget["bg"] = "#292929"

def on_leave(e):
    e.widget["bg"] = BTN_COLOR

btn_frame = tk.Frame(frame_left, bg=BG_COLOR)
btn_frame.pack(fill=tk.X, pady=10)
def create_button(text, command):
    btn = tk.Button(btn_frame, text=text, font=FONT_TITLE, bg=BTN_COLOR, fg=FG_COLOR,
                    relief="flat", bd=0, padx=15, pady=8, cursor="hand2",
                    activebackground="#292929", activeforeground=FG_COLOR,
                    command=command)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    return btn

btn_add = create_button("Добавить", add_task)
btn_edit = create_button("Редактировать", edit_task)
btn_delete = create_button("Удалить", delete_task)

# === Список задач ===
label_list = tk.Label(frame_right, text="Список задач", font=FONT_TITLE, bg=BG_COLOR, fg=FG_COLOR)
label_list.pack(anchor="w", pady=5)

task_list = tk.Listbox(frame_right, font=FONT_TITLE, bg=LIST_COLOR, fg=FG_COLOR,
                       selectbackground="#3A3A3A", bd=0, height=15, relief="flat")
task_list.pack(fill=tk.BOTH, expand=True, pady=5)

# === Настройка отображения задач в списке ===
def format_task_display(event):
    task_list.delete(0, tk.END)  # Очищаем список
    for task_text, desc_text in task_data:
        task_list.insert(tk.END, task_text)  # Заголовок
        if desc_text:
            task_list.insert(tk.END, f"   {desc_text}")  # Пояснение отступом и меньшим шрифтом

task_data = []
task_list.bind("<<ListboxSelect>>", format_task_display)

# Переключение с экрана приветствия на задачи через 2 секунды
root.after(2000, lambda: show_frame(frame_main))

root.mainloop()