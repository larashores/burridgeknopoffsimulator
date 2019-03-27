import tkinter as tk
from tkinter import ttk

import bisect


from signal import Signal


class ListChoiceGUI(ttk.Frame):
    def __init__(self, parent=None, **kwargs):
        ttk.Frame.__init__(self, parent)
        self.signal_delete = Signal()
        self.signal_up = Signal()
        self.signal_down = Signal()
        self.signal_select = Signal()

        frm = ttk.Frame(self)
        self.lbox = tk.Listbox(frm, selectmode=tk.SINGLE, **kwargs)
        self.sbar = ttk.Scrollbar(frm)
        self.hsbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL)

        self.hsbar.config(command=self.lbox.xview)
        self.sbar.config(command=self.lbox.yview)
        self.lbox.config(xscrollcommand=self.hsbar.set)
        self.lbox.config(yscrollcommand=self.sbar.set)
        self.lbox.config(selectmode=tk.SINGLE)

        self.sbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.hsbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.lbox.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        frm.pack(expand=tk.YES, fill=tk.BOTH)

        self.lbox.bind('<Delete>', lambda event: self.signal_delete() if self.lbox.size() >= 1 else None)
        self.lbox.bind('<Button-1>', lambda event: self.after(20, self._click))
        self.lbox.bind('<Up>', lambda event: self.signal_up())
        self.lbox.bind('<Down>', lambda event: self.signal_down())

    def _click(self):
        val = self.lbox.curselection()
        if len(val) == 1:
            self.signal_select(val[0])
        else:
            self.signal_select(None)

    def update_selection(self, ind):
        self.lbox.selection_clear(0, tk.END)
        self.lbox.selection_set(ind)
        self.after(20, lambda: self.lbox.activate(ind))

    def update_selection_after(self, ind):
        self.update_idletasks()
        self.update()
        self.after(20, lambda: self.update_selection(ind))


class KeyWrapper:
    def __init__(self, iterable, key_func = None):
        self._it = iterable
        self.key_func = key_func

    def __getitem__(self, i):
        return self.key_func(self._it[i])

    def __len__(self):
        return len(self._it)


class ListChoice:
    HEIGHT_PER_CELL = 21.4

    def __init__(self, parent=None, **kwargs):
        self.signal_select = Signal()
        self.signal_delete = Signal()

        self._cur_selection = None
        self._unsorted_to_sorted_index = []
        self._sorted_to_unsorted_index = []
        self._data = []
        self._sorted_data = []
        self._wrapper = KeyWrapper(self._sorted_data)
        self._gui = ListChoiceGUI(parent, **kwargs)

        self._gui.signal_select.connect(self._on_select)
        self._gui.signal_delete.connect(self.signal_delete)
        self._gui.signal_up.connect(self._up)
        self._gui.signal_down.connect(self._down)

    def __len__(self):
        return self._gui.lbox.size()

    def __getitem__(self, item):
        return self._data[item]

    def set_key(self, key_func):
        if self._cur_selection is not None:
            selection_viewable = self.get_top() <= self._unsorted_to_sorted_index[self._cur_selection] <= self.get_bottom()
            dif = self._unsorted_to_sorted_index[self._cur_selection] - self.get_top()

        self._wrapper.key_func = key_func
        old = self._data.copy()
        self._clear()
        for data in old:
            self._append(data)

        if self._cur_selection is not None:
            self._gui.update_selection_after(self._unsorted_to_sorted_index[self._cur_selection])

        if self._cur_selection is not None and selection_viewable:
            self.set_top(self._unsorted_to_sorted_index[self._cur_selection] - dif)

    def insert(self, ind, data):
        self._insert(ind, data)
        if self._cur_selection is not None:
            self._gui.update_selection(self._unsorted_to_sorted_index[self._cur_selection])

    def _insert(self, ind, data):
        if self._wrapper.key_func:
            sorted_index = bisect.bisect(self._wrapper, self._wrapper.key_func(data))
        else:
            sorted_index = ind
        for i, val in enumerate(self._sorted_to_unsorted_index):
            if val >= ind:
                self._sorted_to_unsorted_index[i] += 1
        for i, val in enumerate(self._unsorted_to_sorted_index):
            if val >= sorted_index:
                self._unsorted_to_sorted_index[i] += 1
        self._unsorted_to_sorted_index.insert(ind, sorted_index)
        self._sorted_to_unsorted_index.insert(sorted_index, ind)
        self._data.insert(ind, data)
        self._sorted_data.insert(sorted_index, data)
        self._gui.lbox.insert(sorted_index, data)

    def append(self, data):
        self.insert(len(self._data), data)

    def _append(self, data):
        self._insert(len(self._data), data)

    def pop(self, ind):
        data = self._pop(ind)
        if self._cur_selection == ind:
            self._cur_selection = None
            self.signal_select(None)
        return data

    def _pop(self, ind):
        sorted_ind = self._unsorted_to_sorted_index[ind]
        for i, val in enumerate(self._unsorted_to_sorted_index):
            if val > sorted_ind:
                self._unsorted_to_sorted_index[i] -= 1
        for i, val in enumerate(self._sorted_to_unsorted_index):
            if val > ind:
                self._sorted_to_unsorted_index[i] -= 1
        self._unsorted_to_sorted_index.pop(ind)
        self._sorted_to_unsorted_index.pop(sorted_ind)
        self._sorted_data.pop(sorted_ind)
        self._gui.lbox.delete(sorted_ind)
        return  self._data.pop(ind)

    def clear(self):
        self._clear()
        self._cur_selection = None
        self.signal_select(None)

    def _clear(self):
        self._data.clear()
        self._sorted_data.clear()
        self._sorted_to_unsorted_index.clear()
        self._unsorted_to_sorted_index.clear()
        self._gui.lbox.delete(0, tk.END)

    def state(self, *args, **kwargs):
        self._gui.state(*args, **kwargs)

    def itemconfig(self, *args, **kwargs):
        self._gui.lbox.itemconfig(*args, **kwargs)

    def get_selection(self):
        return self._cur_selection

    def set_selection(self, ind):
        ind %= len(self._data)
        self._cur_selection = ind
        self._gui.update_selection(self._unsorted_to_sorted_index[ind])
        self.signal_select(ind)
        self.set_top(ind)

    def get_bottom(self):
        return self.get_top() + self._gui.lbox.winfo_height() / self.HEIGHT_PER_CELL

    def get_top(self):
        return self._gui.lbox.yview()[0] * len(self._data)

    def set_top(self, top):
        if not self._data:
            return
        value = top / len(self._data)
        self._gui.lbox.yview_moveto(value)

    def update_line(self, ind, data):
        if self._cur_selection is not None:
            selection_viewable = self.get_top() <= self._unsorted_to_sorted_index[self._cur_selection] <= self.get_bottom()
            dif = self._unsorted_to_sorted_index[self._cur_selection] - self.get_top()

        self._pop(ind)
        self._insert(ind, data)
        if self._cur_selection == ind:
            self._gui.update_selection(self._unsorted_to_sorted_index[ind])

        if self._cur_selection is not None and selection_viewable:
            self.set_top(self._unsorted_to_sorted_index[self._cur_selection] - dif)

    def bind(self, *args, **kwargs):
        self._gui.lbox.bind(*args, **kwargs)

    def pack(self, **kwargs):
        self._gui.pack(**kwargs)

    def _on_select(self, ind):
        if ind is None:
            return None
        self._cur_selection = self._sorted_to_unsorted_index[ind]
        self.signal_select(self._cur_selection)

    def _up(self):
        if self._cur_selection is None:
            return
        sorted_ind = self._unsorted_to_sorted_index[self._cur_selection]
        if sorted_ind > 0:
            sorted_ind -= 1
            self._cur_selection = self._sorted_to_unsorted_index[sorted_ind]
            self._gui.update_selection(sorted_ind)
            self.signal_select(self._cur_selection)

    def _down(self):
        if self._cur_selection is None:
            return
        sorted_ind = self._unsorted_to_sorted_index[self._cur_selection]
        if sorted_ind < len(self._data) - 1:
            sorted_ind += 1
            self._cur_selection = self._sorted_to_unsorted_index[sorted_ind]
            self._gui.update_selection(sorted_ind)
            self.signal_select(self._cur_selection)


if __name__ == '__main__':
    root = tk.Tk()
    #              0      1      2       3        4       5       6      7     8     9      10
    test_data = ['bab', 'zfs', 'haf', 'abbas', 'abfba', 'asg', 'brrafv', 'a', 'ah', 'adf', 'afd']
    list1 = ListChoice(root)
    list1.signal_select.connect(lambda ind: print(ind))
    edit = ttk.Entry(root)
    button = ttk.Button(root, text='Apply')
    button.config(command=lambda: list1.update_line(list1.get_selection(), edit.get()))

    chk_frm = ttk.Frame(root)
    funcs = [('Real Position', None),
             ('Alphabetical', lambda val: str(val)),
             ('Length', lambda val: len(val))]
    v = tk.IntVar()
    for ind in range(len(funcs)):
        string, func = funcs[ind]
        chk = ttk.Radiobutton(chk_frm, variable=v, value=ind, text=string, command=lambda func=func: list1.set_key(func))
        chk.pack(side=tk.LEFT)
    chk_frm.pack()
    list1.pack(expand=tk.YES, fill=tk.BOTH)
    edit.pack()
    button.pack()

    def test(event):
        selection = list1.get_selection()
        if selection is not None:
            list1.pop(selection)
    for choice in test_data:
        list1.append(choice)
    list1.bind('<Delete>', test)
    print(list1._unsorted_to_sorted_index)
    print(list1._sorted_to_unsorted_index)
    tk.mainloop()
