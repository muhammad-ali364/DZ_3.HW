import asyncio
from bot.bot import main

if __name__ == "__main__":
    try:
        # Для новых версий Python используем asyncio.run
        asyncio.run(main())
    except RuntimeError as e:
        # Если loop уже закрыт или существует
        if "event loop is closed" in str(e):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(main())
            loop.close()
        else:
            raise
