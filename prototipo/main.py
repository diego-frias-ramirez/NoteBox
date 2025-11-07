import tkinter as tk
from login_view import LoginView

def main():
    root = tk.Tk()
    app = LoginView(root)
    root.mainloop()

if __name__ == "__main__":
    main()