import asyncio
import requests

urls = [
    "https://bemaniwiki.com/?SOUND+VOLTEX+%A2%E0/%B5%EC%B6%CA%A5%EA%A5%B9%A5%C8%28BOOTH%A1%C1III+GRAVITY+WARS%29",
    "https://bemaniwiki.com/?SOUND+VOLTEX+%A2%E0/%B5%EC%B6%CA%A5%EA%A5%B9%A5%C8%28IV+HEAVENLY+HAVEN%A1%C1EXCEED+GEAR%29",
    "https://bemaniwiki.com/?SOUND+VOLTEX+%A2%E0/%BF%B7%B6%CA%A5%EA%A5%B9%A5%C8",
]


async def main():
    tasks: list[asyncio.Task[str]] = []

    for url in urls:
        thread_coro = asyncio.to_thread(fetch_text, url)
        tasks.append(asyncio.create_task(thread_coro))

    results = await asyncio.gather(*tasks)

    # TODO: parse tables on page, extract content
    # see ./collect_sdvx_songs.js for how this is done as a script in the browser
    print([result[:50] for result in results])


def fetch_text(url: str):
    print(f"fetching {url}")
    with requests.get(url) as r:
        return r.text


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
