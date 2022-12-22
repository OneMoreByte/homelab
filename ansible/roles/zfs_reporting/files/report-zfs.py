import aiohttp
import asyncio
import discord
import pyyaml
import logging

WEBHOOK = "{{ webhook }}"



async def send_good_news(msg: str, session: aiohttp.ClientSession):
    webhook = discord.Webhook.from_url(WEBHOOK, session=session)
    await webhook.send(msg)


async def parse_output():
    data = {
        "scan_status": {},
        "hardware": {},
    }
    proc = await asyncio.create_subprocess_shell(
        "zpool status",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, _ = await proc.communicate()
    output = stdout.decode().split("\n")
    print(output)
    scan_pos = [i for i in range(len(output)) if output[i].startswith('  scan')]
    config_pos = [i for i in range(len(output)) if output[i].startswith('config')]
    errors_pos = [i for i in range(len(output)) if output[i].startswith('errors')]
    print()
    if scan_pos and config_pos:
        data["scan_status"] = read_scan_data(output[scan_pos[0]:config_pos[0]])
    if config_pos and scan_pos:
        data["hardware"] = read_config_pool_data(output[config_pos[0]+1:errors_pos[0]])
    return data


def read_scan_data(lines: list[str]):
    scan_data = " ".join(lines)
    scan_data_words = scan_data.split()
    try:
        index = scan_data_words.index("errors")
        errors = scan_data_words[index - 1]
    except ValueError:
        errors = 0
    if scan_data.startswith("  scan: reslivered"):
        state = "reslivered",
    elif scan_data.startswith("  scan: scrub"):
        if scan_data.startswith("  scan: scrub in progress"):
            try:
                index = scan_data_words.index("done,")
                pct_done = scan_data_words[index - 1]
            except ValueError:
                pct_done = "????"
            state = f"scrubbing. {pct_done} done."
        else:
            state = "done scrubbing."
    else:
        logging.error(f"got unknown scan state. {lines}")
        state = "unknown scan state!"
    return {
        "state": state,
        "errors": errors,
    }


def config_line_to_dict(line: str) -> dict:
    line_data = line.split()
    return {
        "name": line_data[0],
        "state": line_data[1].lower(),
        "errors": {
            "read": line_data[2],
            "write": line_data[3],
            "checksum": line_data[4],
        }
    }


def read_config_pool_data(zpool_data: list[str]):
    pools = []
    # Skip column line
    for line in zpool_data[1:]:
        # 4 spaces is a drive
        if line.startswith("\t    "):
            data = config_line_to_dict(line)
            pools[-1]["vdevs"][-1]["devices"].append(data)
        # two spaces is a vdev
        elif line.startswith("\t  "):
            data = config_line_to_dict(line)
            data["devices"] = []
            pools[-1]["vdevs"].append(data)
        # no spaces is a pool
        elif line.startswith("\t"):
            data = config_line_to_dict(line)
            data["vdevs"] = []
            pools.append(data)
        # Anything else is probably garbage
        else:
            ...
    return pools



async def check():
    print("running a check")

   # async with aiohttp.ClientSession() as session:
        
    print(await parse_output())
    print("done")


asyncio.run(check())