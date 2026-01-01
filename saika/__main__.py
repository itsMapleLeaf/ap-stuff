import asyncio
from asyncio.subprocess import DEVNULL, Process
from contextlib import asynccontextmanager
from pathlib import Path
import subprocess
import threading
import psutil
import requests
import webview


def __main():
    threading.Thread(
        target=lambda: asyncio.run(__run_tracker()),
        daemon=True,
    ).start()
    asyncio.run(__run_webview())


async def __run_webview():
    async with await __start_dev_server():
        view_url = "http://localhost:5173/"
        await __wait_until_reachable(view_url, timeout_seconds=3)

        class Api:
            def log(self, *values):
                print(*values)

        webview.create_window(title="Saika", url=view_url, js_api=Api())
        webview.start(ssl=True, debug=True)


async def __start_dev_server():
    server = await asyncio.subprocess.create_subprocess_exec(
        "bun",
        "dev",
        cwd=Path(__file__).parent / "web",
        stdin=DEVNULL,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
    )
    return __ensure_killed(server)


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


async def __wait_until_reachable(url: str, timeout_seconds: float):
    async with asyncio.timeout(timeout_seconds):
        while True:
            try:
                response = await asyncio.to_thread(requests.options, url)
                if response.ok:
                    break
                else:
                    print(f"{response.status_code=}")
            except (requests.HTTPError, requests.ConnectionError):
                print(f"failed to connect")

            print(f"retrying...")
            await asyncio.sleep(0.1)


@asynccontextmanager
async def __ensure_killed(process: Process):
    """Ensures every child processes of a given process are killed"""
    try:
        yield process
    finally:
        if process.pid is None or process.returncode is not None:
            return
        try:
            parent = psutil.Process(process.pid)
            for child in parent.children(recursive=True):
                print(f"killing child process {child.name()=} {child.pid=}")
                child.kill()
            print(f"killing parent process {parent.name()=} {parent.pid=}")
            parent.kill()
        except psutil.NoSuchProcess:
            pass


__main()
