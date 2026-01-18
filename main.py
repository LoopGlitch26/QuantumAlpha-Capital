"""
QuantumAlpha Capital - Elite Algorithmic Trading Platform
Professional-grade entry point for systematic alpha generation
"""

import signal
import sys
import asyncio
import atexit
from nicegui import ui, app

# Global reference to bot_service for cleanup
bot_service_ref = None

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    print("\n[INFO] QuantumAlpha Capital shutting down gracefully...")
    cleanup()
    sys.exit(0)

def cleanup():
    """Cleanup function called on exit"""
    global bot_service_ref
    if bot_service_ref and bot_service_ref.is_running():
        print("[INFO] Terminating market processor...")
        try:
            # Run the async stop in a new event loop if needed
            try:
                loop = asyncio.get_running_loop()
                # If we're here, we're in an async context
                asyncio.create_task(bot_service_ref.stop())
            except RuntimeError:
                # No running loop, create one
                asyncio.run(bot_service_ref.stop())
            print("[INFO] Market processor terminated successfully")
        except Exception as e:
            print(f"[WARN] Error terminating processor: {e}")

if __name__ in {"__main__", "__mp_main__"}:
    # Setup signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Register cleanup on exit
    atexit.register(cleanup)

    # Import and setup app on startup
    from src.gui.app import create_app, agent_service

    # Save reference to agent_service for cleanup
    bot_service_ref = agent_service

    # Call create_app to register all pages
    create_app()

    # Register shutdown handler with NiceGUI app
    async def on_app_shutdown():
        """Called when NiceGUI app is shutting down"""
        print("[INFO] QuantumAlpha Capital platform shutdown event triggered")
        cleanup()

    app.on_shutdown(on_app_shutdown)

    # Run in native desktop mode
    ui.run(
        native=True,              # Desktop mode via pywebview
        window_size=(1400, 900),  # Window dimensions
        fullscreen=False,
        title="QuantumAlpha Capital",
        favicon="⚡",
        dark=True,                # Dark theme
        reload=False,             # Disable hot reload in production
        show=True,                # Show window immediately
        port=8083,                # Use different port
        binding_refresh_interval=0.1  # Faster UI updates
    )
