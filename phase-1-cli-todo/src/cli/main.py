"""
Main entry point for the CLI Todo Application.
"""
# from .interactive_cli import InteractiveCLI
from src.cli.interactive_cli import InteractiveCLI


def main():
    """
    Main function to start the CLI application.
    """
    cli = InteractiveCLI()
    cli.run()


if __name__ == "__main__":
    main()