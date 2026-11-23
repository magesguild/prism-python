"""
Project PRISM Interactive Terminal REPL & Command-Line Utility.
"""

import sys
from .client import PrismClient
from .exceptions import PrismError


def main():
    client = PrismClient()

    if len(sys.argv) > 1:
        expr = " ".join(sys.argv[1:])
        try:
            res = client.eval(expr)
            print(f"{res.result}  ({res.latency_us:.2f} µs)")
            sys.exit(0)
        except PrismError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    print("╔═══════════════════════════════════════════════════════════════════════════════════════╗")
    print("║                 PROJECT PRISM MATHEMATICAL ENGINE (prism-calc)                        ║")
    print("║            Mage's Guild Psychonautics LLC — Official Python SDK REPL                  ║")
    print("╚═══════════════════════════════════════════════════════════════════════════════════════╝")
    print("Connected to https://www.magesguild.io (Unauthenticated Trial Mode). Type 'exit' to quit.\n")

    session_id = "cli_repl"
    while True:
        try:
            line = input("prism>> ").strip()
            if not line:
                continue
            if line.lower() in ("exit", "quit", ":q"):
                print("Goodbye.")
                break
            res = client.eval(line, session_id=session_id)
            print(f"{res.result}  ({res.latency_us:.2f} µs)")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break
        except PrismError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
