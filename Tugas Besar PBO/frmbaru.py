import tkinter as tk
from tkinter import Frame, Label, Entry, Button, messagebox, END
from tkinter import ttk  # Import ttk separately

from Mk import Matakuliah

class FormMatakuliah:

    def __init__(self, parent, title):
        self.parent = parent
        self.parent.geometry("880x650")
        self.parent.title(title)
        self.parent.protocol("WM_DELETE_WINDOW", self.onKeluar)
        self.ditemukan = None
        self.aturKomponen()
        self.onReload()

    def aturKomponen(self):
        mainFrame = Frame(self.parent, bd=10, bg='Dark Orange')
        mainFrame.pack(fill=tk.BOTH, expand=tk.YES)

        label_bg_color = "#87CEEB"
        Label(mainFrame, text='NAMA MAHASISWA:', bg=label_bg_color).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        Label(mainFrame, text='NAMA MK:', bg=label_bg_color).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        Label(mainFrame, text='SKS:', bg=label_bg_color).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        Label(mainFrame, text='SEMESTER:', bg=label_bg_color).grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)

        self.txtNAMAMHS = Entry(mainFrame)
        self.txtNAMAMHS.grid(row=0, column=1, padx=5, pady=5)

        # Use a Combobox for NAMA MK
        self.txtNAMAMK = ttk.Combobox(mainFrame, width=27)
        self.txtNAMAMK.grid(row=1, column=1, padx=5, pady=5)
        self.txtNAMAMK['values'] = ('Pemrograman 2', 'Sistem Informasi', 'Kalkulus 2', 'Struktur Data', 'AIK 2', 'Statistik')

        self.txtSKS = Entry(mainFrame)
        self.txtSKS.grid(row=2, column=1, padx=5, pady=5)

        self.txtSEMESTER = ttk.Combobox(mainFrame, width=27)
        self.txtSEMESTER.grid(row=3, column=1, padx=5, pady=5)
        self.txtSEMESTER['values'] = ('1', '2', '3')
        self.txtSEMESTER.current(0)

        btn_color = "#4CAF50"
        self.btnSimpan = Button(mainFrame, text='Simpan', command=self.onSimpan, width=10, bg=btn_color)
        self.btnSimpan.grid(row=0, column=3, padx=5, pady=5)

        self.btnClear = Button(mainFrame, text='Clear', command=self.onClear, width=10, bg=btn_color)
        self.btnClear.grid(row=1, column=3, padx=5, pady=5)

        self.btnHapus = Button(mainFrame, text='Hapus', command=self.onDelete, width=10, bg=btn_color)
        self.btnHapus.grid(row=2, column=3, padx=5, pady=5)

        self.btnSaveEdit = Button(mainFrame, text='Simpan Edit', command=self.onSimpanEdit, width=10, bg=btn_color)
        self.btnSaveEdit.grid(row=3, column=3, padx=5, pady=5)

        columns = ('idmhs', 'namamhs', 'namamk', 'sks', 'semester', 'edit')
        self.tree = ttk.Treeview(mainFrame, columns=columns, show='headings', height=5)
        self.tree.grid(row=4, column=0, columnspan=4, pady=10)

        headings = ['ID', 'NAMAMHS', 'NAMAMK', 'SKS', 'SEMESTER', 'Edit']
        col_widths = [30, 200, 200, 30, 100, 50]

        for i, col in enumerate(columns):
            self.tree.heading(col, text=headings[i], anchor='center')
            self.tree.column(col, width=col_widths[i], anchor='center', stretch=tk.NO)

        self.tree.tag_configure('Treeview', background='')
        self.tree.tag_configure('colored_heading', background='')

        self.tree.bind('<ButtonRelease-1>', self.onEdit)

    def onClear(self, event=None):
        self.txtNAMAMHS.delete(0, END)
        self.txtNAMAMHS.insert(END, "")
        self.txtNAMAMK.delete(0, END)
        self.txtNAMAMK.insert(END, "")
        self.txtSKS.delete(0, END)
        self.txtSKS.insert(END, "")
        self.btnSimpan.config(text="Simpan")
        self.onReload()
        self.ditemukan = False

    def onReload(self, event=None):
        mhs = Matakuliah()
        result = mhs.getAllData()

        for item in self.tree.get_children():
            self.tree.delete(item)

        matakuliahs = []
        for row_data in result:
            matakuliahs.append(row_data)

        for matakuliah in matakuliahs:
            id, namamhs, namamk, tk, status = matakuliah
            self.tree.insert('', END, values=(id, namamhs, namamk, tk, status.upper()))

            if status.upper() == "Tersimpan":
                self.tree.tag_configure("parkir", background="#a4f9a0")
                self.tree.item(self.tree.get_children()[-1], tags=("parkir",))
            elif status.upper() == "KELUAR PARKIR":
                self.tree.tag_configure("keluar_parkir", background="#ff7979")
                self.tree.item(self.tree.get_children()[-1], tags=("keluar_parkir",))

    def onSimpan(self, event=None):
        namamhs = self.txtNAMAMHS.get()
        namamk = self.txtNAMAMK.get()
        sks = self.txtSKS.get()

        if not namamhs or not namamk or not sks:
            messagebox.showwarning("Data Belum Lengkap", "Harap isi semua kolom data terlebih dahulu.")
            return

        mhs = Matakuliah()
        mhs.namamhs = namamhs
        mhs.namamk = namamk
        mhs.sks = sks

        if self.ditemukan:
            res = mhs.updateByNIP(namamhs)
            ket = 'Diperbarui'
        else:
            res = mhs.simpan()
            ket = 'Disimpan'

        rec = mhs.affected
        if rec > 0:
            messagebox.showinfo("showinfo", f"Data Berhasil {ket}")
        else:
            messagebox.showwarning("showwarning", f"Data Gagal {ket}")

        self.onClear()
        return rec

    def onDelete(self, event=None):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("showinfo", "Pilih data yang akan dihapus.")
            return

        namamhs = self.tree.item(selected_item, "values")[1]
        mhs = Matakuliah()
        mhs.namamhs = namamhs
        res = mhs.deleteByNIM(namamhs)
        rec = mhs.affected

        if rec > 0:
            messagebox.showinfo("showinfo", "Data Berhasil dihapus")
            self.onReload()  # Refresh the Treeview
        else:
            messagebox.showwarning("showwarning", "Data Gagal dihapus")

        self.onClear()

    def onKeluar(self, event=None):
        self.parent.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    aplikasi = FormMatakuliah(root, "Aplikasi Data matakuliah")
    root.mainloop()
