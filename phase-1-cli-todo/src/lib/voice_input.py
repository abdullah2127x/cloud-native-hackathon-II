"""
Voice input utility for the todo application.
Provides voice-to-text functionality with fallback options.
"""
import speech_recognition as sr
import sys
import time
import threading
import keyboard
import socket
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from colorama import init, Fore, Style

# Initialize colorama for cross-platform color support
init()
console = Console()


def check_internet_connection():
    """
    Check if internet connection is available by trying to reach Google
    """
    try:
        # Try to connect to Google's DNS server
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False


def voice_to_text_with_internet_fallback():
    """
    Voice-to-text with online-first approach and offline fallback
    Continuous listening for up to 30 seconds or until ESC is pressed
    """
    console.print(Panel(Text("Voice Input for Todo", style="bold blue")))
    console.print("Press ESC to cancel voice input at any time")
    console.print("Listening will automatically stop after 10 seconds of silence")

    # Check internet connectivity first
    internet_available = check_internet_connection()
    if internet_available:
        console.print("[green]✓ Internet connection detected - Using online recognition[/green]")
        console.print("[blue]Speak now...[/blue]")
    else:
        console.print("[yellow]Offline mode - Using local recognition[/yellow]")
        console.print("[blue]Speak now...[/blue]")

    recognizer = sr.Recognizer()
    audio_source = sr.Microphone()

    # Adjust for ambient noise
    with audio_source as source:
        console.print("[cyan]Adjusting for ambient noise...[/cyan]")
        recognizer.adjust_for_ambient_noise(source, duration=1)

    console.print("[cyan]Listening... Speak now (or press ESC to cancel)[/cyan]")
    start_time = time.time()
    timeout_duration = 10  # 10 seconds timeout

    # Variable to store the result
    result_text = None
    stop_listening = False

    # Function to check for ESC key press
    def check_for_esc():
        nonlocal stop_listening
        while not stop_listening:
            if keyboard.is_pressed('esc'):
                stop_listening = True
                console.print("\n[yellow]ESC pressed - cancelling voice input...[/yellow]")
                break
            time.sleep(0.1)

    # Start the ESC key monitoring thread
    esc_thread = threading.Thread(target=check_for_esc, daemon=True)
    esc_thread.start()

    try:
        # Listen for audio
        with audio_source as source:
            # Listen with a timeout to allow for ESC checking
            audio = recognizer.listen(source, timeout=timeout_duration)

            # Process the audio
            console.print("[cyan]Processing speech...[/cyan]")

            if internet_available:
                # Try online recognition first (Google)
                try:
                    text = recognizer.recognize_google(audio)
                    console.print(f"[green]✓ Recognition successful: {text}[/green]")
                    result_text = text
                except sr.RequestError:
                    # Fallback to offline recognition (Sphinx)
                    try:
                        text = recognizer.recognize_sphinx(audio)
                        console.print(f"[green]✓ Recognition successful: {text}[/green]")
                        result_text = text
                    except:
                        console.print("[red]Could not understand the speech[/red]")
                        result_text = None
                except sr.UnknownValueError:
                    # Even if Google couldn't understand, try Sphinx
                    try:
                        text = recognizer.recognize_sphinx(audio)
                        console.print(f"[green]✓ Recognition successful: {text}[/green]")
                        result_text = text
                    except:
                        console.print("[red]Could not understand the speech[/red]")
                        result_text = None
            else:
                # Offline mode only
                try:
                    text = recognizer.recognize_sphinx(audio)
                    console.print(f"[green]✓ Recognition successful: {text}[/green]")
                    result_text = text
                except:
                    console.print("[red]Could not understand the speech[/red]")
                    result_text = None

    except sr.WaitTimeoutError:
        console.print("\n[yellow]Timeout reached - no speech detected[/yellow]")
        result_text = None
    except sr.UnknownValueError:
        console.print("\n[red]Could not understand the speech[/red]")
        result_text = None
    except sr.RequestError as e:
        console.print(f"\n[red]Error with speech recognition service: {e}[/red]")
        result_text = None
    except Exception as e:
        console.print(f"\n[red]Unexpected error occurred: {e}[/red]")
        result_text = None

    # Stop the ESC thread
    stop_listening = True
    esc_thread.join(timeout=0.1)

    return result_text


def get_voice_input():
    """
    Wrapper function to get voice input with error handling
    Returns the recognized text or None if cancelled/error occurred
    """
    try:
        result = voice_to_text_with_internet_fallback()
        return result
    except Exception as e:
        console.print(f"[red]Error during voice input: {e}[/red]")
        return None