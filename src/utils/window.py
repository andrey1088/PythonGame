from PyQt6.QtWidgets import QPushButton

def create_menu_button(title):
    map_button = QPushButton(title)
    map_button.setStyleSheet("""  
        QPushButton {
            background: rgba(0, 172, 252, 50);
            font-size: 14px;
            border: none;
            border-radius: 10px;
            padding: 20px;
            color: #fff;
        }
        QPushButton:hover {
            background: rgba(0, 172, 252, 20);
        }
      """)

    return map_button

def create_button(title, image_path, font_size=1):
    button = QPushButton(title)
    button.setStyleSheet(f"""  
        QPushButton {{
            background-image: url({image_path});
            background-repeat: no-repeat;
            background-position: center;
            font-size: {font_size}px;
            font-weight: bold;
            border: none;
            border-radius: 20px;
            padding: 140px 10px 20px;
            color: #fff;
        }}
        QPushButton:hover {{
            opacity: 0.5;
        }}
      """)

    return button