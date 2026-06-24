import asyncio

from fastmcp import Client

from backend.core.config import settings


async def main():
    client = Client(settings.mcp_server_url)

    async with client:
        tools = await client.list_tools()
        print("TOOLS:")
        for tool in tools:
            print("-", tool.name)


if __name__ == "__main__":
    asyncio.run(main())