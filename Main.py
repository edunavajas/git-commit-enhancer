from project_code import Init
import signal

if __name__ == "__main__":
    signal.signal(signal.SIGINT, Init.handle_interrupt)
    Init.init()
