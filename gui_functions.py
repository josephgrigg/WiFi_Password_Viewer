from column_select_window import ColumnSelect
import tkinter.filedialog as filedialog


def toggle_row_color(menu, row_color):
    """
    :type menu: tkinter.Menu object
    :type row_color: tkinter.StringVar() object
    """
    menu.screen.results_display.tag_configure('grey background',
                                              background=row_color.get())
    menu.grey_rows = not menu.grey_rows


def copy_selection(master, results_display):
    master.clipboard_clear()

    # Determine the order that the columns appear on the screen.
    order_map = []
    # '#all' means that the columns are in their original order and all
    # are being shown.
    if '#all' in results_display['displaycolumns']:
        order_map = list(range(len(ColumnSelect.column_names)))
    else:
        for title in results_display['displaycolumns']:
            order_map.append(ColumnSelect.column_names.index(title))

    for item in results_display.selection():
        values = results_display.item(item=item, option='values')
        for i in range(len(order_map)):
            if order_map[i] < len(values):
                master.clipboard_append(values[order_map[i]])
                if i != len(order_map) - 1:
                    master.clipboard_append('\t')
        if item != results_display.selection()[-1]:
            master.clipboard_append('\n')


def clear_clipboard(master):
    master.clipboard_clear()
    master.clipboard_append('')


def save_as(results_display):
    file = filedialog.asksaveasfile(
        mode='w',
        defaultextension='.txt',
        filetypes=(('Tab delimited text file', '*.txt'), ('all files', '*.*')))
    # Exit function if user presses cancel button.
    if file is None:
        return
    # Determine the order that the columns appear on the screen.
    order_map = []
    # '#all' means that the columns are in their original order and all
    # are being shown.
    if '#all' in results_display['displaycolumns']:
        order_map = list(range(len(ColumnSelect.column_names)))
    else:
        for title in results_display['displaycolumns']:
            order_map.append(ColumnSelect.column_names.index(title))

    for item in results_display.selection():
        values = results_display.item(item=item, option='values')
        for i in range(len(order_map)):
            if order_map[i] < len(values):
                file.write(values[order_map[i]])
                if i != len(order_map) - 1:
                    file.write('\t')
        if item != results_display.selection()[-1]:
            file.write('\n')
    file.close()
