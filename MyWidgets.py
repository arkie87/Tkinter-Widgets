from tkinter import Entry, Checkbutton, StringVar,  IntVar


class ValidatedEntry(Entry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(validate="all", validatecommand=(self.register(self.validate), "%P"))
        self.bind("<KeyRelease>", self.guess)
        self.bind("<Return>", self.accept)
        self.bind("<FocusIn>", self.highlight)
        self.bind("<FocusOut>", self.unhighlight)
        self.bind("<BackSpace>", self.backspace)

    def backspace(self, event):
        self.selection_range(self.index("insert") - 1, "end")
        
    def validate(self, text):
        return True

    def guess(self, text):
        return True

    def unhighlight(self, event):
        self.icursor(0)
        self.selection_range(0, 0)

    def accept(self, event):
        event.widget.tk_focusNext().focus()

    def highlight(self, event):
        self.selection_range(0, "end")


class FloatEntry(ValidatedEntry):
    def validate(self, text):
        return (
            all(char in "0123456789.-" for char in text) and  # all characters are valid
            "-" not in text[1:] and  # "-" is the first character or not present
            text.count(".") <= 1  # only 0 or 1 periods
        )

    def get(self):
        return float(super().get() or 0)


class PositiveFloatEntry(FloatEntry):
    def validate(self, text):
        return super().validate(text) and "-" not in text


class DollarEntry(FloatEntry):
    def validate(self, text):
        return super().validate(text) and ("." not in text or len(text[text.index(".")+1:]) <= 2)


class PositiveDollarEntry(PositiveFloatEntry, DollarEntry):
    def validate(self, text):
        return super().validate(text)


class IntEntry(FloatEntry):
    def validate(self, text):
        return super().validate(text) and "." not in text
            
    def get(self):
        return int(super().get())


class PositiveIntEntry(IntEntry):
    def validate(self, text):
        return super().validate(text) and "-" not in text


class AutoCompleteEntry(ValidatedEntry):
    def __init__(self, frame, items, *args, **kwargs):
        super().__init__(frame, *args, **kwargs)
        self.items = items
        self.text = StringVar(frame)
        self.configure(textvariable=self.text)

    def guess(self, event):
        input_text = self.get().lower()[:self.index("insert")]
        if not input_text or input_text in [item.lower() for item in self.items]:
            self.selection_range(0, "end")
            return

        for item in self.items:
            if item.lower().startswith(input_text):
                self.text.set(item)
                self.selection_range(len(input_text), "end")
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
    row = 0

    Label(frame, text="Validated Entry").grid(row=row, column=0)
    ve = ValidatedEntry(frame)
    ve.grid(row=row, column=1)
    row += 1

    Label(frame, text="Float Entry").grid(row=row, column=0)
    fe = FloatEntry(frame)
    fe.grid(row=row, column=1)
    row += 1

    Label(frame, text="Positive Float Entry").grid(row=row, column=0)
    pfe = PositiveFloatEntry(frame)
    pfe.grid(row=row, column=1)
    row += 1

    Label(frame, text="Dollar Entry").grid(row=row, column=0)
    ce = DollarEntry(frame)
    ce.grid(row=row, column=1)
    row += 1

    Label(frame, text="Positive Dollar Entry").grid(row=row, column=0)
    ce = PositiveDollarEntry(frame)
    ce.grid(row=row, column=1)
    row += 1

    Label(frame, text="Int Entry").grid(row=row, column=0)
    ie = IntEntry(frame)
    ie.grid(row=row, column=1)
    row += 1

    Label(frame, text="Positive Int Entry").grid(row=row, column=0)
    pie = PositiveIntEntry(frame)
    pie.grid(row=row, column=1)
    row += 1

    Label(frame, text="Auto Completing Entry").grid(row=row, column=0)
    ace = AutoCompleteEntry(frame, stores)
    ace.grid(row=row, column=1)
    row += 1

    Label(frame, text="Strict Auto Completing Entry").grid(row=row, column=0)
    sace = StrictAutoCompleteEntry(frame, stores)
    sace.grid(row=row, column=1)
    row += 1

    cb = IntVar()
    Checkbutton(frame, variable=cb).grid(row=row, column=0)
    Button(frame, text="quit", command=destroy).grid(row=row, column=1)
    row += 1

    frame.mainloop()


if __name__ == "__main__":
    from tkinter import Tk, Button, Toplevel, Label
    root = Tk()
    root.title("Entry Widgets")
    root.geometry("400x400")

    Button(root, text="new", command=frame).pack()
    Button(root, text="quit", command=root.destroy).pack()
    root.mainloop()
