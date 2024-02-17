import tkinter as tk
from tkinter import Frame, Label, Entry, Button, ttk, StringVar, messagebox
from Mk import matakuliah

class Formmatakuliah:
    
    def __init__(self, parent, title, update_main_window):
        self.parent = parent
        self.update_main_window = update_main_window       
        self.parent.geometry("450x450")
        self.parent.title(title)
        self.parent.protocol("WM_DELETE_WINDOW", self.onKeluar)
        self.ditemukan = None
        self.aturKomponen()
        self.onReload()
        
    def aturKomponen(self):
        mainFrame = Frame(self.parent, bd=10, bg='Dark Orange')
        mainFrame.pack(fill=tk.BOTH, expand=tk.YES)

        label_bg_color = "blue"
        Label(mainFrame, text='NAMA MAHASISWA:', bg=label_bg_color).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        Label(mainFrame, text='NAMA MK:', bg=label_bg_color).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        Label(mainFrame, text='SKS:', bg=label_bg_color).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        Label(mainFrame, text='SEMESTER:', bg=label_bg_color).grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)

        # Label
        Label(mainFrame, text='NAMA MAHASISWA:').grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.txtNAMAMHS = Entry(mainFrame) 
        self.txtNAMAMHS.grid(row=0, column=1, padx=5, pady=5) 
        self.txtNAMAMHS.bind("<Return>", self.onCari)  # menambahkan event Enter key

        Label(mainFrame, text='NAMA MK:').grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.txtNAMAMK = ttk.Combobox(mainFrame, width=27)
        self.txtNAMAMK.grid(row=1, column=1, padx=5, pady=5)
        self.txtNAMAMK['values'] = ('Pemrograman 2', 'Sistem Informasi', 'Kalkulus 2', 'Struktur Data', 'AIK 2', 'Statistik')

        Label(mainFrame, text='SKS:').grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.txtSKS = Entry(mainFrame) 
        self.txtSKS.grid(row=2, column=1, padx=5, pady=5) 

        Label(mainFrame, text='SEMESTER:').grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.txtSEMESTER = StringVar()
        Cbo = ttk.Combobox(mainFrame, width=27, textvariable=self.txtSEMESTER) 
        Cbo.grid(row=3, column=1, padx=5, pady=5)
        Cbo['values'] = ('1', '2', '3')
        Cbo.current()      
    
        # Button
        self.btnSimpan = Button(mainFrame, text='Simpan', command=self.onSimpan, width=10, bg='orange')
        self.btnSimpan.grid(row=0, column=3, padx=5, pady=5)

        self.btnClear = Button(mainFrame, text='Clear', command=self.onClear, width=10, bg='orange')
        self.btnClear.grid(row=1, column=3, padx=5, pady=5)

        self.btnHapus = Button(mainFrame, text='Hapus', command=self.onDelete, width=10, bg='orange')
        self.btnHapus.grid(row=2, column=3, padx=5, pady=5)

        # New button for Save Edit
        self.btnSaveEdit = Button(mainFrame, text='Simpan Edit', command=self.onSimpanEdit, width=10, bg='orange')
        self.btnSaveEdit.grid(row=3, column=3, padx=5, pady=5)


        # define columns
        columns = ('idmhs', 'namamhs', 'namamk', 'sks', 'semester', 'edit')

        self.tree = ttk.Treeview(mainFrame, columns=columns, show='headings')
        # define headings
        self.tree.heading('idmhs', text='ID', anchor='center')
        self.tree.column('idmhs', width="30", anchor='center', stretch=tk.NO)
        self.tree.heading('namamhs', text='NAMAMHS', anchor='center')
        self.tree.column('namamhs', width="200", anchor='center', stretch=tk.NO)
        self.tree.heading('namamk', text='NAMAMK', anchor='center')
        self.tree.column('namamk', width="200", anchor='center', stretch=tk.NO)
        self.tree.heading('sks', text='SKS', anchor='center')
        self.tree.column('sks', width="30", anchor='center', stretch=tk.NO)
        self.tree.heading('semester', text='SEMESTER', anchor='center')
        self.tree.column('semester', width="100", anchor='center', stretch=tk.NO)
        self.tree.heading('edit', text='Edit', anchor='center')
        self.tree.column('edit', width="50", anchor='center', stretch=tk.NO)

        # set tree position
        self.tree.place(x=0, y=200)
        self.onReload()
        
        # bind edit button
        self.tree.bind('<ButtonRelease-1>', self.onEdit)
        
    def onClear(self, event=None):
        self.txtNAMAMHS.delete(0, tk.END)
        self.txtNAMAMHS.insert(tk.END, "")
        self.txtNAMAMK.delete(0, tk.END)
        self.txtNAMAMK.insert(tk.END, "")       
        self.txtSKS.delete(0, tk.END)
        self.txtSKS.insert(tk.END, "")
        self.txtSEMESTER.set("")
        self.btnSimpan.config(text="Simpan")
        self.onReload()
        self.ditemukan = False
        
    def onReload(self, event=None):
        # get data mahasiswa
        dosen = matakuliah()
        result = dosen.getAllData()
        for item in self.tree.get_children():
            self.tree.delete(item)
        students = []
        for row_data in result:
            students.append(row_data)

        for student in students:
            student_data = student + ("Edit",)
            self.tree.insert('', tk.END, values=student_data)
    
    def onCari(self, event=None):
        namamhs = self.txtNAMAMHS.get()
        dosen = matakuliah()
        res = dosen.getByNAMAMHS(namamhs)
        rec = dosen.affected
        if rec > 0:
            messagebox.showinfo("showinfo", "Data Ditemukan")
            self.TampilkanData()
            self.ditemukan = True
        else:
            messagebox.showwarning("showwarning", "Data Tidak Ditemukan") 
            self.ditemukan = False
            self.txtNAMAMK.focus()
        return res
        
    def TampilkanData(self, event=None):
        namamhs = self.txtNAMAMHS.get()
        dosen = matakuliah()
        res = dosen.getByNAMAMHS(namamhs)
        self.txtNAMAMK.delete(0, tk.END)
        self.txtNAMAMK.insert(tk.END, dosen.namamk)
        self.txtSKS.delete(0, tk.END)
        self.txtSKS.insert(tk.END, dosen.sks)
        self.txtSEMESTER.set(dosen.semester)   
        self.btnSimpan.config(text="Update")
                 
    def onSimpan(self, event=None):
        namamhs = self.txtNAMAMHS.get()
        namamk = self.txtNAMAMK.get()
        sks = self.txtSKS.get()
        semester = self.txtSEMESTER.get()
        
        dosen = matakuliah()
        dosen.namamhs = namamhs
        dosen.namamk = namamk
        dosen.sks = sks
        dosen.semester = semester
        
        if self.ditemukan:
            res = dosen.updateByNAMAMHS(namamhs)
            ket = 'Diperbarui'
        else:
            res = dosen.simpan()
            ket = 'Disimpan'
            
        rec = dosen.affected
        if rec > 0:
            messagebox.showinfo("showinfo", "Data Berhasil " + ket)
            self.onReload()  # Reload the Treeview after inserting/updating
        else:
            messagebox.showwarning("showwarning", "Data Gagal " + ket)

        self.onClear()
        return rec
    
   # ... (previous code)

    def onEdit(self, event):
        item = self.tree.selection()[0]
        self.txtNAMAMHS.delete(0, tk.END)
        self.txtNAMAMHS.insert(tk.END, self.tree.item(item, 'values')[1])
        self.TampilkanData()
        self.ditemukan = True  # Set the flag to indicate that the record is found
        # Change the text of the Save button to "Simpan Edit"
        self.btnSimpan.config(text="Simpan Edit")

    def onSimpanEdit(self, event=None):
        namamhs = self.txtNAMAMHS.get()
        namamk = self.txtNAMAMK.get()
        sks = self.txtSKS.get()
        semester = self.txtSEMESTER.get()

        dosen = matakuliah()
        dosen.namamhs = namamhs
        dosen.namamk = namamk
        dosen.sks = sks
        dosen.semester = semester

        if self.ditemukan:
            res = dosen.updateByNAMAMHS(namamhs, {'namamk': namamk, 'sks': sks, 'semester': semester})
            ket = 'Diperbarui'
        else:
            res = dosen.simpan()
            ket = 'Disimpan'

        rec = dosen.affected
        if rec > 0:
            messagebox.showinfo("showinfo", "Data Berhasil " + ket)
            self.onReload()  # Reload the Treeview after inserting/updating
            self.btnSimpan.config(text="Simpan")  # Change the text back to "Simpan"
        else:
            messagebox.showwarning("showwarning", "Data Gagal " + ket)

        self.onClear()
        return rec


    def onDelete(self, event=None):
        namamhs = self.txtNAMAMHS.get()
        dosen = matakuliah()
        dosen.namamhs = namamhs
        if self.ditemukan:
            res = dosen.deleteByNAMAMHS(namamhs)
            rec = dosen.affected
        else:
            messagebox.showinfo("showinfo", "Data harus ditemukan dulu sebelum dihapus")
            rec = 0
        
        if rec > 0:
            messagebox.showinfo("showinfo", "Data Berhasil dihapus")
        
        self.onClear()
    
    def onEdit(self, event):
        item = self.tree.selection()[0]
        self.txtNAMAMHS.delete(0, tk.END)
        self.txtNAMAMHS.insert(tk.END, self.tree.item(item, 'values')[1])
        self.TampilkanData()
        self.ditemukan = True  # Set the flag to indicate that the record is found

    def onKeluar(self, event=None):
        # memberikan perintah menutup aplikasi
        self.parent.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    aplikasi = Formmatakuliah(root, "Aplikasi Data Mahasiswa")
    root.mainloop()
