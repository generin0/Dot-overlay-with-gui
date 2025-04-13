import tkinter as tk
from tkinter import ttk
import ctypes
import itertools

# Основное окно
overlay = tk.Tk()# --> определение ткинтера
style = ttk.Style() # --> стиль
style.theme_use('clam') # --> тема
 settings_window = tk.Toplevel()
label_title = ttk.Label(settings_window, text="Overlay", background='Grey', foreground='white', font=("Segoe UI", 12, "bold")) # --> заголовок в окне
label_title.pack(pady=10) # --> положение заголовка
settings_window.title("Overlay") # --> название окна
settings_window.geometry("240x320") # --> геометрия окна
settings_window.configure(bg='Grey') # --> бг окна
settings_window.resizable(False, False) # --> можно.нельзя менять размер
# Переменные
is_visible = True# --> переменная для отображения точки (включение\выключение)
crosshair_visible = False# --> выключение\включение прицела
dot_visible = True# --> выключение\включение точки
colors = itertools.cycle(['#ff0000', '#34a8ff', '#050505', '#ffffff'])# --> цвета для change_color()
current_color = next(colors)
x1, y1, x2, y2 = 5, 5, 8, 8 # --> первичные координаты точки

def make_window_clickthrough(hwnd): # --> позволяет мыши не появляться во время взаимодействия с игрой\окном
    extended_style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
    extended_style |= 0x00000020
    extended_style |= 0x00080000
    ctypes.windll.user32.SetWindowLongW(hwnd, -20, extended_style)

def change_color(): # --> меняет цвет прицела
    global current_color
    current_color = next(colors)
    canvas.itemconfig(dot, fill=current_color, outline=current_color)
    canvas.itemconfig(crosshair_h, fill=current_color)
    canvas.itemconfig(crosshair_v, fill=current_color)

def toggle_crosshair(): # --> добавляет действия по нажатию определённой кнопки
    global crosshair_visible, dot_visible
    if dot_visible: # --> отрисовка прицела\точки
        canvas.itemconfig(dot, state='hidden')
        dot_visible = False
        crosshair_visible = True
        canvas.itemconfig(crosshair_h, state='normal')
        canvas.itemconfig(crosshair_v, state='normal')
    else: # --> если точка не видна, прицел показываем
        canvas.itemconfig(dot, state='normal')
        dot_visible = True
        crosshair_visible = False
        canvas.itemconfig(crosshair_h, state='hidden')
        canvas.itemconfig(crosshair_v, state='hidden')

def resize_dot(increase=True): 
    global x1, y1, x2, y2
    delta = -0.5 if increase else 0.5
    if increase and x2 - x1 < 20: # --> меняет размер(больше)
        x1 += delta
        y1 += delta
        x2 -= delta
        y2 -= delta
    elif not increase and x2 - x1 > 3: # --> меняет размер(меньше)
        x1 += delta
        y1 += delta
        x2 -= delta
        y2 -= delta
    canvas.coords(dot, x1, y1, x2, y2)

def toggle_overlay(): # --> показывает\скрывает прицел
    global is_visible
    if is_visible:
        overlay.withdraw()
    else:
        overlay.deiconify()
    is_visible = not is_visible

def close_overlay(): 
    overlay.destroy()
    settings_window.destroy()

def main(): # --> мейн функция, создание прозрачного окна, определение переменных dot, crosshair_v, crosshair_h, canvas 
    global canvas, dot, crosshair_h, crosshair_v

    screen_width = overlay.winfo_screenwidth() # --> сбор информации по ширине
    screen_height = overlay.winfo_screenheight() # --> сбор информации по высоте

    overlay.overrideredirect(True)
    overlay.attributes("-topmost", True) # --> поверх окон
    overlay.geometry(f'200x200+{screen_width//2-7}+{screen_height//2-7}') # --> размер окна процесса
    overlay.resizable(False, False) # --> можно\нельзя менять размер окна
    overlay.wm_attributes("-transparentcolor", "black") # --> прозрачность

    canvas = tk.Canvas(overlay, width=200, height=200, bg='black', highlightthickness=0) # --> объявление канваса
    canvas.pack()

    dot = canvas.create_oval(x1, y1, x2, y2, fill=current_color, outline=current_color) # --> непосредственно создание точки
    overlay.deiconify() # --> показывать точку при открытии программы
    crosshair_h = canvas.create_line(0, 7, 15, 7, fill=current_color, state='hidden', width=1) # --> непосредственно создание прицела
    crosshair_v = canvas.create_line(7, 0, 7, 15, fill=current_color, state='hidden', width=1)

    overlay.update_idletasks()
    overlay.update()
  
    hwnd = ctypes.windll.user32.GetParent(overlay.winfo_id())
    make_window_clickthrough(hwnd)

    overlay.mainloop()
############################################################################################################# ИНТЕРФЕЙС
btn_color = ttk.Button(settings_window, text="Change color", command=change_color)
btn_color.pack(pady=5)

btn_switch = ttk.Button(settings_window, text="Switch dot/crosshair", command=toggle_crosshair)
btn_switch.pack(pady=5)

btn_increase = ttk.Button(settings_window, text="Increase crosshair size", command=lambda: resize_dot(True))
btn_increase.pack(pady=5)

btn_decrease = ttk.Button(settings_window, text="Decrease crosshair size", command=lambda: resize_dot(False))
btn_decrease.pack(pady=5)

btn_show_hide = ttk.Button(settings_window, text="Show/Hide overlay", command=toggle_overlay)
btn_show_hide.pack(pady=5)

btn_exit = ttk.Button(settings_window, text="Exit", command=close_overlay)
btn_exit.pack(pady=5)

############################################################################################################# ИНТЕРФЕЙС

main()
