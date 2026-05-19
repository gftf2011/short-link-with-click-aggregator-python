from short_link.main.factory.shortlink import batch


async def run() -> None:
    batch_controller = batch()
    await batch_controller.run()
