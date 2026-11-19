from PyQt6.QtWidgets import QPushButton,QWidget

def ok_button(parent: QWidget | None = None,on_click=None, text = "OK"):
    # submit
    btn_ok = QPushButton(text, parent)
    btn_ok.setStyleSheet("background-color: rgb(110, 53, 201); color: white; padding: 6px;")
    if on_click is not None:
        btn_ok.clicked.connect(on_click)
    return btn_ok