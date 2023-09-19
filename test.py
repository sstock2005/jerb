import aiohttp, io, asyncio, re

def isbb(input):
    match = re.search(r'filename=([A-Za-z0-9]+\.png)', input)
    if match:
        if "bb" in match.group(1):
            return True
        else:
            return False
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # windows bug
asyncio.run(main())