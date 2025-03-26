from PyQt6.QtWidgets import QPushButton

def create_menu_button(title, is_disabled=False):
    map_button = QPushButton(title)
    background = 'rgba(0, 172, 252, 50)' if not is_disabled else 'rgba(0, 172, 252, 20)'
    map_button.setStyleSheet(f"""  
        QPushButton {{
            background: {background};
            font-size: 14px;
            border: none;
            border-radius: 10px;
            padding: 20px;
            color: #fff;
        }}
        QPushButton:hover {{
            background: rgba(0, 172, 252, 20);
        }}
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