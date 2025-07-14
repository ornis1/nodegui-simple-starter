import gi
import cairo

gi.require_version("Gtk", "3.0")
gi.require_version("PangoCairo", "1.0")

from gi.repository import Gtk, Pango, Gdk, GLib

class MirrorLabel(Gtk.DrawingArea):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.letter_spacing = 20 * Pango.SCALE  # Расстояние между буквами (10 пикселей)
        self.set_size_request(-1, -1)
        
    def set_text(self, text):
        self.text = text
        self.queue_draw()
        
    def do_draw(self, cr):
        # Черный фон
        cr.set_source_rgb(0, 0, 0)
        cr.paint()

        # Настройки текста
        layout = self.create_pango_layout(self.text)
        font_desc = Pango.FontDescription()
        font_desc.set_size(80 * Pango.SCALE)  # Уменьшил размер для наглядности
        font_desc.set_weight(Pango.Weight.BOLD)
        layout.set_font_description(font_desc)

        # Установка расстояния между буквами
        attr_list = Pango.AttrList()
        attr_list.insert(Pango.attr_letter_spacing_new(10 * Pango.SCALE))
        layout.set_attributes(attr_list)

        # Размеры
        width = self.get_allocated_width()
        height = self.get_allocated_height()
        text_width, text_height = layout.get_pixel_size()

        # Обычное отображение текста (без зеркалирования)
        cr.set_source_rgb(0.1, 0.1, 0.1)  # Белый текст
        cr.move_to((width - text_width)/2, (height - text_height)/2)
        PangoCairo.show_layout(cr, layout)

class FullscreenWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Marat")
        
        # Устанавливаем полноэкранный режим
        self.fullscreen()
        
        # Текущий язык (0=английский, 1=русский, 2=корейский)
        self.current_lang = 0
        self.texts = ["KTChH", "КТЧХ", "김치 떡볶이 잡채 호떡"]
        
        # Основной вертикальный контейнер
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(main_box)
        
        # Контейнер для текста (с расширением)
        text_box = Gtk.Box()
        main_box.pack_start(text_box, True, True, 0)
        
        # Создаем кастомный виджет с зеркальным текстом
        self.label = MirrorLabel(self.texts[self.current_lang])
        text_box.pack_start(self.label, True, True, 0)
        
        # Черный фон окна
        self.override_background_color(Gtk.StateFlags.NORMAL, 
                                      Gdk.RGBA(0, 0, 0, 1))
        
        # Подключение обработчика закрытия окна
        self.connect("destroy", Gtk.main_quit)
        
        # Запускаем таймер для автоматического переключения языков
        self.timeout_id = GLib.timeout_add_seconds(5, self.rotate_language)
    
    def rotate_language(self):
        # Переключение языка
        self.current_lang = (self.current_lang + 1) % len(self.texts)
        
        # Обновление текста
        self.label.set_text(self.texts[self.current_lang])
        
        # Возвращаем True, чтобы таймер продолжал работать
        return True

# Добавляем необходимые импорты
from gi.repository import PangoCairo

# Создаем и показываем окно
win = FullscreenWindow()
win.show_all()

# Запускаем главный цикл GTK
Gtk.main()