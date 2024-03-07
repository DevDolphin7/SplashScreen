import splashscreen_ctk as splash
import threading, time


def do_jobs():
    set_splash_text(f"Doing something...")
    start_thread(do_something, "Hello,", "world")

    set_splash_text(f"Doing something else...")
    start_thread(do_something_else, "Goodbye,", "world!")
    
    set_splash_text("Loading complete!")
    test.close_splashscreen = True 


def start_thread(target, *args):
    # Use threading for complicated actions that would freeze tkinter / cause not responding warning.
    complex_action = threading.Thread(target=target, args=[arg for arg in args])
    complex_action.start()
    while complex_action.is_alive():
        time.sleep(1)


def do_something(text1, text2):
    print(text1, text2)
    time.sleep(5)


def do_something_else(text1, text2):
    print(text1, text2)
    time.sleep(5)  


def set_splash_text(text):
    # Note changes to splash text will not work if called from any other thread than main, e.g: it won't work if called from do_something_complex()
    test.splash_status_text.set(text)
    test.update()
    

test = splash.SplashScreen("path_to_image.jpg", # Can be any image file type that works with PILLOW / CTkImage, or bytes with io.BytesIO
                            initial_status_value="Loading...",
                            app_info="Your Application v1.0.0",
                            app_info_font=("helvetica", 36),
                            app_info_text_color="#333333",
                            status_font=("helvetica", 18),
                            status_text_colour="#222222")

test.after(5, do_jobs)
test.mainloop()
