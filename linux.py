import tkinter as tk
from tkinter import filedialog, messagebox
from pycdlib import PyCdlib
try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO
class FSProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FS to ISO Creator")
        self.root.geometry("400x200")
        self.root.configure(bg="black")
        
        # Dados carregados do arquivo .fs
        self.system_config=""
        self.system_name=""
        self.files_to_process = None        
        # Botão para carregar arquivo .fs
        self.load_button = tk.Button(
            root, text="Load .fs File", command=self.load_fs_file, bg="white", fg="black"
        )
        self.load_button.pack(pady=10)
        
        # Botão para criar arquivo .iso
        self.save_button = tk.Button(
            root, text="Save as .iso", command=self.save_iso_file, bg="white", fg="black"
        )
        self.save_button.pack(pady=10)
        
        # Rótulo de status
        self.status_label = tk.Label(
            root, text="", bg="black", fg="white", wraplength=350
        )
        self.status_label.pack(pady=10)

    def load_fs_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("bin Files", "*.bin"), ("All Files", "*.*")]
        )
        if not file_path:
            return

        try:
            system_name=file_path
            splitdir=file_path.split("/")
            system_name=splitdir[len(splitdir)-1]
            systempoint=system_name.find(".")
            
            if systempoint>-1:
                system_name=system_name[:systempoint].upper()
            self.system_name=system_name
            
            system_name=file_path.replace(".bin",".cfg")
            with open(file_path, "rb") as f:
                content = f.read()
                self.system_config=content
            with open(file_path, "rb") as f:
                content = f.read()
                self.files_to_process = content
            
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load .fs file: {e}")
            self.status_label.config(text="Failed to load .fs file.")

    def save_iso_file(self):
        if not self.files_to_process:
            messagebox.showerror("Error", "No data loaded. Please load a .fs file first.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".iso", filetypes=[("ISO Files", "*.iso"), ("All Files", "*.*")]
        )
        if not save_path:
            return

        try:
            iso = PyCdlib()
            iso.new()

            # Adicionar os arquivos ao ISO
            bootstr = self.files_to_process            
            iso.add_fp(BytesIO(bootstr), len(bootstr), '/BOOT.;1')

            iso.add_eltorito('/BOOT.;1')
           
            iso.add_directory('/BOOT')
            
            iso.add_directory('/BOOT/GRUB')
            print(self.system_name)
            iso.add_directory('/BOOT/'+self.system_name+"")
            
            bootstr =self.files_to_process
            iso.add_fp(BytesIO(bootstr), len(bootstr), '/BOOT/'+self.system_name+"/"+self.system_name+".BIN")
            bootstr =self.system_config
            iso.add_fp(BytesIO(bootstr), len(bootstr), '/BOOT/'+self.system_name+"/"+self.system_name+".CFG")
           
            iso.write(save_path)
            iso.close()

            messagebox.showinfo("Success", f"ISO file saved at {save_path}")
            self.status_label.config(text="ISO file created successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create ISO file: {e}")
            self.status_label.config(text="Failed to create ISO file.")


if __name__ == "__main__":
    root = tk.Tk()
    app = FSProcessorApp(root)
    root.mainloop()

