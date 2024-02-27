import customtkinter as ctk
from PIL import Image


class SplashScreen(ctk.CTk):
    """Generate a splash screen in the middle of the screen.
    Creates splash_status_text which is a StringVar, to update the user on progress (see tkinter documentation).
    Parameters:
    - image_path (str): Define the path to an image file including fyle type (see PILLOW Image.open and CTk.Image documentation).
    - initial_status_value (str, optional): Define the initial value of splash_status_text, the status text variable.
    - status_font (tuple, optional): Define (font_as_str, size_as_int_<=64) for splash status text (see custom tkinter documentation).
    - app_info (str, optional): Define the app name and version that is loading.
    - app_info_font (tuple, optional): Define (font_as_str, size_as_int_<=64) for app info text (see custom tkinter documentation)."""

    def __init__(self, image_path, initial_status_value="", status_font=("helvetica", 18), status_text_colour="black",
                 app_info="", app_info_font=("helvetica", 36), app_info_text_color="black") -> None:
        super().__init__()

        # Set class variables
        self._close_splashscreen = False
        self._canvas = ctk.CTkFrame(self)
        self._image_path = image_path
        self._initial_status_value = initial_status_value
        self._status_font = status_font
        self._status_text_colour = status_text_colour
        self._app_info = app_info
        self._app_info_font = app_info_font
        self._app_info_text_color = app_info_text_color
        self._check_user_input_types()
        
        # Setup window
        self._position_window()
        self._set_standalone_attributes()
        self._create_widgets()
        self._pack_widgets()

        self.after(500, self._check_close)


    @property
    def close_splashscreen(self):
        return self._close_splashscreen
    

    @close_splashscreen.setter
    def close_splashscreen(self, boolean):
        if type(boolean) != bool: raise TypeError(f"close_splashscreen requires a boolean, type {type(boolean)} supplied.")
        else: self._close_splashscreen = boolean


    def _check_user_input_types(self):
        user_variables = {"image_path": [self._image_path, str],
                          "initial_status_value": [self._initial_status_value, str],
                          "status_font": [self._status_font, tuple],
                          "status_text_colour": [self._status_text_colour, str],
                          "app_info": [self._app_info, str],
                          "app_info_font": [self._app_info_font, tuple],
                          "app_info_text_color": [self._app_info_text_color, str]}
        
        for name, var_list in user_variables.items():
            if var_list[1] == tuple:
                if len(var_list[0]) != 2: raise ValueError (f"{name} should only contain (font_as_str, size_as_int), {var_list[0]} was provided.")
                elif type(var_list[0][0]) != str: raise TypeError(f"{name} should only contain (font_as_str, size_as_int), {type(var_list[0][0])} was provided for font.")
                elif type(var_list[0][1]) != int: raise TypeError(f"{name} should only contain (font_as_str, size_as_int), {type(var_list[0][1])} was provided for size.")

            elif type(var_list[0]) == var_list[1]: continue
            
            else: raise TypeError(f"{name} must be type {var_list[1]}, type {type(var_list[0])} was given.")


    def _position_window(self) -> None:
        """Set the window to be in the middle of screen"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self._window_width = int(screen_width / 3)
        self._window_height = int(screen_height / 3)
        x_position = int((screen_width - self._window_width) / 2)
        y_position = int((screen_height - self._window_height) / 2)
        self.geometry(f"{self._window_width}x{self._window_height}+{x_position}+{y_position}")


    def _set_standalone_attributes(self) -> None:
        self.attributes("-topmost", 1)
        self.resizable(False,False)
        self.update_idletasks()
        self.overrideredirect(True)


    def _create_widgets(self) -> None:
        # Load the splash screen image        
        image = Image.open(self._image_path)
        image = image.resize((self._window_width, self._window_height))

        # Check how big the window is, affects how labels are created
        self._filler_label_required = False
        if self._window_height > 160:
            app_info_height = 80
            self._filler_label_required = True
        else: app_info_height = int(self._window_height / 2)
        
        # Create app_info label at top
        app_info_image = image.crop((0,0,self._window_width, app_info_height))
        app_info_image = ctk.CTkImage(app_info_image, size=[self._window_width, app_info_height])
        self._app_info_label = ctk.CTkLabel(self._canvas, image=app_info_image, corner_radius=0,
                                            text=self._app_info, font=self._app_info_font, text_color=self._app_info_text_color)
        
        # Create filler label if required
        if self._filler_label_required:
            filler_image = image.crop((0,app_info_height,self._window_width, self._window_height - app_info_height))
            filler_image = ctk.CTkImage(filler_image, size=[self._window_width, self._window_height - (app_info_height * 2)])
            self.filler_label = ctk.CTkLabel(self._canvas, image=filler_image, corner_radius=0, text="")

        
        # Create status label to inform user of progress at bottom
        self.splash_status_text = ctk.StringVar(value=self._initial_status_value)
        status_image = image.crop((0,self._window_height - app_info_height,self._window_width, self._window_height))
        status_image = ctk.CTkImage(status_image, size=[self._window_width, app_info_height])
        self._status_label = ctk.CTkLabel(self._canvas, image=status_image, corner_radius=0,
                                         textvariable=self.splash_status_text, font=self._status_font, text_color=self._status_text_colour)


    def _pack_widgets(self) -> None:
        # Pack the widgets
        self._app_info_label.pack(anchor="n", fill="both")
        if self._filler_label_required: self.filler_label.pack(anchor="n", fill="both")
        self._status_label.pack(anchor="n", fill="both")
        self._canvas.pack(fill="both")


    def _check_close(self) -> None:
        if self._close_splashscreen: self.destroy()
        else: self.after(500, self._check_close)
