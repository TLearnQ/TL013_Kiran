import socket
import logging
from logging.handlers import RotatingFileHandler
import json
import traceback

HOST = "0.0.0.0"
PORT = 9000

# ---------- Logging Setup ----------
def init_logger():
    logger = logging.getLogger("echo_server")
    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(
        "echo_server.log",
        maxBytes=200_000,
        backupCount=3
    )
    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    return logger


logger = init_logger()


def safe_log(level, msg):
    """Centralized safe logging so logging failures don't crash."""
    try:
        if level == "error":
            logger.error(msg)
        else:
            logger.info(msg)
    except Exception:
        print("Logging failure:", msg)


# ---------- Stats ----------
stats = {"processed": 0, "failed": 0}


# ---------- Connection Handler ----------
def handle_client(conn, addr):
    safe_log("info", f"Connection from {addr}")
    with conn:
        while True:
            try:
                data = conn.recv(4096)
                if not data:
                    break

                raw = data
                safe_log("info", f"Raw bytes: {raw}")

                try:
                    text = raw.decode("utf-8", errors="replace")
                except Exception:
                    text = "<decode failed>"
                    stats["failed"] += 1
                    safe_log("error", "Failed to decode bytes")
                else:
                    stats["processed"] += 1
                    safe_log("info", f"Decoded text: {text}")

                # Echo it back
                try:
                    conn.sendall(raw)
                except Exception:
                    stats["failed"] += 1
                    safe_log("error", "Failed to send data back to client")

            except Exception as e:
                stats["failed"] += 1
                safe_log("error", f"Socket error: {e}")
                safe_log("error", traceback.format_exc())
                break


# ---------- Main Loop ----------
def run_server():
    safe_log("info", f"Starting TCP echo service on port {PORT}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            s.bind((HOST, PORT))
            s.listen()
        except Exception as e:
            safe_log("error", f"Failed to start server: {e}")
            return

        safe_log("info", "Server ready")

        try:
            while True:
                try:
                    conn, addr = s.accept()
                    handle_client(conn, addr)
                except Exception as e:
                    stats["failed"] += 1
                    safe_log("error", f"Accept failed: {e}")
        except KeyboardInterrupt:
            safe_log("info", "Shutdown requested by user")
        finally:
            print("\n=== Summary ===")
            print(f"Processed: {stats['processed']}")
            print(f"Failed:    {stats['failed']}")
            safe_log("info", f"Summary: {stats}")


if __name__ == "__main__":
    run_server()
