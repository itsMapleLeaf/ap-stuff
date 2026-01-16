import asyncio
from asyncio.subprocess import DEVNULL
from pathlib import Path
import subprocess
import sys
import webview

from .lib.http import wait_until_reachable
from .lib.subprocess import ensure_killed


def __main():
    # tracker_thread = threading.Thread(
    #     target=lambda: asyncio.run(__run_tracker()),
    #     daemon=True,
    # )
    # tracker_thread.start()
    asyncio.run(__run_webview())


async def __run_webview():
    async with await __start_dev_server():
        view_url = "http://localhost:5173/"
        await wait_until_reachable(view_url, timeout_seconds=10)

        class Api:
            def log(self, *values):
                print(*values)

        webview.create_window(title="Saika", url=view_url, js_api=Api())
        webview.start(ssl=True, debug=True)


async def __start_dev_server():
    config = {
        "cwd": Path(__file__).parent / "web",
        "stdin": DEVNULL,
    }

    if sys.platform == "win32":
        config["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP

    server = await asyncio.subprocess.create_subprocess_exec(
        "bun",
        "dev",
        **config,
    )

    return ensure_killed(server)


async def __run_tracker():
    print("running tracker")

    from worlds.tracker.TrackerClient import TrackerGameContext, server_loop

    class SaikaContext(TrackerGameContext):
        updated = asyncio.Future()

        def __init__(self):
            super().__init__("localhost", None)

            self.set_callback(self.on_update)
            self.set_events_callback(self.on_update_events)

            self.auth = "MapleVoltex"
            self.server_task = asyncio.create_task(
                server_loop(self), name="server loop"
            )

            print("running generator")
            self.run_generator()

        def on_update(self, locations: list[str]):
            print(f"{locations=}")
            if not self.updated.done():
                self.updated.set_result(None)
            return True

        def on_update_events(self, events: list[str]):
            print(f"{events=}")
            return True

    ctx = SaikaContext()

    try:
        assert ctx.server_task
        await asyncio.wait(
            [ctx.server_task, ctx.updated],
            return_when=asyncio.FIRST_COMPLETED,
        )
    finally:
        await ctx.shutdown()


__main()
