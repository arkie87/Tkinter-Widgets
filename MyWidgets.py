from tkinter import Entry, Checkbutton, StringVar,  IntVar, INSERT, END


class ValidatedEntry(Entry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(validate="all", validatecommand=(self.register(self.validate), "%P"))
        
    def validate(self, text):
        return True


class FloatEntry(ValidatedEntry):
    def validate(self, text):
        if (
            all(char in "0123456789.-" for char in text) and  # all characters are valid
            "-" not in text[1:] and  # "-" is the first character or not present
            text.count(".") <= 1  # only 0 or 1 periods
        ):
            return True
        else:
            return False

    def get(self):
        f = super().get()
        if f == "":
            return 0
        else:
            return float(f)


class PositiveFloatEntry(FloatEntry):
    def validate(self, text):
        if super().validate(text) and "-" not in text:
            return True
        else:
            return False


class IntEntry(FloatEntry):
    def validate(self, text):
        if super().validate(text) and "." not in text:
            return True
        else:
            return False
            
    def get(self):
        return int(super().get())


class PositiveIntEntry(IntEntry):
    def validate(self, text):
        if super().validate(text) and "-" not in text:
            return True
        else:
            return False


class AutoCompleteEntry(ValidatedEntry):
    def __init__(self, frame, items, *args, **kwargs):
        super().__init__(frame, *args, **kwargs)
        self.items = items
        self.text = StringVar(frame)
        self.configure(textvariable=self.text)
        self.bind("<FocusIn>", self.deselect)
        self.bind("<FocusOut>", self.deselect)
        self.bind("<Return>", self.accept)
        self.bind("<BackSpace>", self.backspace)
        self.bind("<KeyRelease>", self.guess)

    def deselect(self, event):
        self.selection_range(0, 0)

    def accept(self, event):
        self.icursor(0)
        self.selection_range(0, END)
        event.widget.tk_focusNext().focus()

    def backspace(self, event):
        self.selection_range(self.index(INSERT) - 1, END)

    def guess(self, event):
        input_text = self.get().lower()[:self.index(INSERT)]
        if input_text:
            for item in self.items:
                if item.lower().startswith(input_text):
                    self.text.set(item)
                    self.selection_range(len(input_text), len(item))
                    return


class StrictAutoCompleteEntry(AutoCompleteEntry):
    def validate(self, text):
        if text == "":
            return True
        else:
            for item in self.items:
                if item.lower().startswith(text.lower()):
                    return True
            return False


def frame():
    def destroy():
        print(ve.get(), fe.get(), pfe.get(), ie.get(), pie.get(), ace.get(), sace.get(), cb.get())
        frame.destroy()
        frame.quit()

    stores = ["Trader Joes", "Target", "Trade Goods", "Tarps R Us"]
    frame = Toplevel()
    frame.geometry("400x400")
    Label(frame, text="Validated Entry").grid(row=0, column=0)
    ve = ValidatedEntry(frame)
    ve.grid(row=0, column=1)
    Label(frame, text="Float Entry").grid(row=1, column=0)
    fe = FloatEntry(frame)
    fe.grid(row=1, column=1)
    Label(frame, text="Positive Float Entry").grid(row=2, column=0)
    pfe = PositiveFloatEntry(frame)
    pfe.grid(row=2, column=1)
    Label(frame, text="Int Entry").grid(row=3, column=0)
    ie = IntEntry(frame)
    ie.grid(row=3, column=1)
    Label(frame, text="Positive Int Entry").grid(row=4, column=0)
    pie = PositiveIntEntry(frame)
    pie.grid(row=4, column=1)
    Label(frame, text="Auto Completing Entry").grid(row=5, column=0)
    ace = AutoCompleteEntry(frame, stores)
    ace.grid(row=5, column=1)
    Label(frame, text="Strict Auto Completing Entry").grid(row=6, column=0)
    sace = StrictAutoCompleteEntry(frame, stores)
    sace.grid(row=6, column=1)
    cb = IntVar()
    Checkbutton(frame, variable=cb).grid(row=7, column=0)
    Button(frame, text="quit", command=destroy).grid(row=7, column=1)
    frame.mainloop()


if __name__ == "__main__":
    from tkinter import Tk, Button, Toplevel, Label
    root = Tk()
    root.title("Entry Widgets")
    root.geometry("400x400")

    Button(root, text="new", command=frame).pack()
    Button(root, text="quit", command=root.destroy).pack()
    root.mainloop()