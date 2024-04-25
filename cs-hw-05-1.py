import asyncio
from pathlib import Path
import aiofiles
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


async def copy_file(source, output):
    """Асинхронно копіює файл у відповідну підпапку на основі його розширення у цільовій папці."""
    ext = source.suffix[1:]
    output_dir = output / ext
    # Створення підпапки, якщо вона не існує
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / source.name
    try:
        async with aiofiles.open(source, 'rb') as src, aiofiles.open(output_file, 'wb') as dst:
            content = await src.read()
            await dst.write(content)
        logging.info(
            f"Файл успішно скопійовано: {source} до {output_file}")
    except Exception as e:
        logging.error(
            f"Помилка при копіюванні файлу {source} до {output_file}: {e}")


async def read_folder(source_folder, output_folder):
    """Читає всі файли у вихідній папці та розподіляє їх у цільовій папці на основі розширення."""
    folder = Path(source_folder)
    tasks = []
    loop = asyncio.get_running_loop()
    # Використання executor для обходу директорії, щоб уникнути блокування
    files = await loop.run_in_executor(None, list, folder.iterdir())
    for entry in files:
        if entry.is_dir():
            # Рекурсивне читання підпапок
            task = asyncio.create_task(read_folder(entry, output_folder))
            tasks.append(task)
        else:
            task = asyncio.create_task(
                copy_file(entry, output_folder))  # Копіювання файлу
            tasks.append(task)
    await asyncio.gather(*tasks)


async def main(source_folder, output_folder):
    await read_folder(source_folder, output_folder)

if __name__ == "__main__":
    src_folder = Path("/path/to/source_folder")
    out_folder = Path("/path/to/output_folder")
    asyncio.run(main(src_folder, out_folder))
