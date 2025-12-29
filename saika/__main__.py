import asyncio
import signal
import webview


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


def __backend():
    try:
        asyncio.run(__run_tracker(), debug=True)
    except:
        print("am die")


class Api:
    def log(self, *values):
        print(*values)


window = webview.create_window(
    title="d",
    url="http://localhost:5173/",
    js_api=Api(),
)

webview.start(ssl=True, func=__backend)
