import customtkinter as ctk
from typing import Callable


class GUI(ctk.CTk):
    class StyledButton(ctk.CTkButton):
        # Creates a button with preset styling options
        def __init__(self, master: ctk.CTkFrame, text: str = "CTkLabel", command: Callable = None) -> None:
            super().__init__(
                master,
                text=text,
                text_color="#F5C6EC",
                font=("Calibri", 26),
                corner_radius=0,
                border_width=2,
                border_color="#000000",
                fg_color="#CF2191",
                hover_color="#9A208C",
                command=command
            )

    def __init__(self) -> None:
        super().__init__()

        # Window settings
        self.title("Tic Tac Toe")
        self.geometry(f"600x600+{self.winfo_screenwidth()//2 - 150}+{self.winfo_height()//2}")
        self.resizable(False, False)
        ctk.set_appearance_mode("light")

        # Frame covering entire window
        self.bg_frame = ctk.CTkFrame(self, fg_color="#F5C6EC", corner_radius=0)
        self.bg_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Fonts
        self.TITLE_FONT = ("Calibri", 48, "bold")
        self.SUBTITLE_FONT = ("Calibri", 34)
        self.TURN_FONT = ("Calibri", 34, "bold")
        self.SCORE_FONT = ("Calibri", 26, "bold")

        # Create widgets

        self.title_label = ctk.CTkLabel(
            self.bg_frame,
            text="Tic Tac Toe",
            font=self.TITLE_FONT,
            text_color="#9A208C"
        )

        self.subtitle_label = ctk.CTkLabel(
            self.bg_frame,
            text="Select a Mode",
            font=self.SUBTITLE_FONT,
            text_color="#9A208C"
        )

        self.normal_btn = self.StyledButton(self.bg_frame, text="Normal")
        self.impossible_btn = self.StyledButton(self.bg_frame, text="Impossible")
        self.friend_btn = self.StyledButton(self.bg_frame, text="Play a Friend!", command=self.menu_to_grid)

        self.grid_frame = ctk.CTkFrame(self, fg_color="#9A208C", corner_radius=0)
        self.grid_blocks = [ctk.CTkCanvas(self.grid_frame, bg="#F5C6EC", bd=0, highlightthickness=0) for _ in range(9)]

        self.turn_var = ctk.StringVar(value="X to play!")
        self.turn_label = ctk.CTkLabel(
            self.bg_frame,
            textvariable=self.turn_var,
            font=self.TURN_FONT,
            text_color="#9A208C"
        )

        self.x_score_var = ctk.StringVar(value="X Score:\n0")
        self.x_score_label = ctk.CTkLabel(
            self.bg_frame,
            textvariable=self.x_score_var,
            font=self.SCORE_FONT,
            text_color="#9A208C",
        )

        self.o_score_var = ctk.StringVar(value="O Score:\n0")
        self.o_score_label = ctk.CTkLabel(
            self.bg_frame,
            textvariable=self.o_score_var,
            font=self.SCORE_FONT,
            text_color="#9A208C"
        )

        self.return_btn = ctk.CTkButton(
            self.bg_frame,
            text="← Menu",
            text_color="#9A208C",
            font=self.SCORE_FONT,
            fg_color="transparent",
            hover_color="#FFD1F7",
            command=self.grid_to_menu
        )

        # Bind the hover effects
        self.bind_btn_hover()

    def start(self):
        # Starts the GUI
        self.display_menu()
        self.mainloop()

    def bind_btn_hover(self) -> None:
        # Buttons change size on hover
        self.normal_btn.bind(
            "<Enter>",
            lambda e: self.normal_btn.place(relx=0.5, rely=0.45, relwidth=0.35, relheight=0.07, anchor="center")
        )

        self.normal_btn.bind(
            "<Leave>",
            lambda e: self.normal_btn.place(relx=0.5, rely=0.45, relwidth=0.33, relheight=0.06, anchor="center")
        )

        self.impossible_btn.bind(
            "<Enter>",
            lambda e: self.impossible_btn.place(relx=0.5, rely=0.517, relwidth=0.35, relheight=0.07, anchor="center")
        )

        self.impossible_btn.bind(
            "<Leave>",
            lambda e: self.impossible_btn.place(relx=0.5, rely=0.517, relwidth=0.33, relheight=0.06, anchor="center")
        )

        self.friend_btn.bind(
            "<Enter>",
            lambda e: self.friend_btn.place(relx=0.5, rely=0.584, relwidth=0.35, relheight=0.07, anchor="center")
        )

        self.friend_btn.bind(
            "<Leave>",
            lambda e: self.friend_btn.place(relx=0.5, rely=0.584, relwidth=0.33, relheight=0.06, anchor="center")
        )

    def display_menu(self) -> None:
        # Places the labels
        self.title_label.place(relx=0.5, rely=0.3, anchor="center")
        self.subtitle_label.place(relx=0.5, rely=0.38, anchor="center")

        # Places the buttons
        self.normal_btn.place(relx=0.5, rely=0.45, relwidth=0.33, relheight=0.06, anchor="center")
        self.impossible_btn.place(relx=0.5, rely=0.517, relwidth=0.33, relheight=0.06, anchor="center")
        self.friend_btn.place(relx=0.5, rely=0.584, relwidth=0.33, relheight=0.06, anchor="center")

    def hide_menu(self) -> None:
        # Hides the labels
        self.title_label.place_forget()
        self.subtitle_label.place_forget()

        # Hides the button
        self.normal_btn.place_forget()
        self.impossible_btn.place_forget()
        self.friend_btn.place_forget()

    def display_grid(self) -> None:
        # Place labels
        self.turn_label.place(relx=0.5, rely=0.1, anchor="center")
        self.x_score_label.place(relx=0.3, rely=0.9, anchor="center")
        self.o_score_label.place(relx=0.7, rely=0.9, anchor="center")

        # Place the grid area
        self.grid_frame.place(relx=0.5, rely=0.5, relwidth=0.6, relheight=0.6, anchor="center")

        # Grid Layout
        self.grid_frame.columnconfigure((0, 2, 4), weight=32, uniform="a")  # Columns
        self.grid_frame.columnconfigure((1, 3), weight=1, uniform="a")  # Vertical grid lines

        self.grid_frame.rowconfigure((0, 2, 4), weight=32, uniform="a")  # Rows
        self.grid_frame.rowconfigure((1, 3), weight=1, uniform="a")  # Horizontal grid lines

        # Grid block positions
        coordinate_list = [
            (0, 0), (0, 2), (0, 4),
            (2, 0), (2, 2), (2, 4),
            (4, 0), (4, 2), (4, 4)
        ]

        # Placing the grid blocks
        for index, grid_block in enumerate(self.grid_blocks):
            coordinates = coordinate_list[index]
            grid_block.grid(row=coordinates[0], column=coordinates[1])

        # Place button
        self.return_btn.place(relx=0, rely=0, relwidth=0.18)

    def hide_grid(self) -> None:
        # Hide labels
        self.turn_label.place_forget()
        self.x_score_label.place_forget()
        self.o_score_label.place_forget()

        # Hide grid
        self.grid_frame.place_forget()

        # Hide button
        self.return_btn.place_forget()

    def menu_to_grid(self) -> None:
        # Transitions from the menu to the grid
        self.hide_menu()
        self.display_grid()

    def grid_to_menu(self) -> None:
        # Transitions from the grid to the menu
        self.hide_grid()
        self.display_menu()
