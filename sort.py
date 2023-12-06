import os
import shutil
import re
from concurrent.futures import ThreadPoolExecutor

def normalize(name):
    mapping = {
        # Кирилиця до латиниці
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'H', 'Ґ': 'G', 'Д': 'D', 'Е': 'E', 'Є': 'Ye',
        'Ж': 'Zh', 'З': 'Z', 'И': 'Y', 'І': 'I', 'Ї': 'Yi', 'Й': 'Y', 'К': 'K', 'Л': 'L',
        'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
        'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ю': 'Yu',
        'Я': 'Ya', 'ь': '', '’': ''
    }
    for cyr, lat in mapping.items():
        name = name.replace(cyr, lat)
        name = name.replace(cyr.lower(), lat.lower())

    name = re.sub(r'[^a-zA-Z0-9]', '_', name)
    return name

def unpack(archive_path, path_to_unpack):
    """Распаковка архива и сохранение оригинала."""
    unpack_folder = os.path.join(path_to_unpack, os.path.splitext(os.path.basename(archive_path))[0])
    os.makedirs(unpack_folder, exist_ok=True)
    shutil.unpack_archive(archive_path, unpack_folder)

def get_unique_name(path, name, ext):
    if not os.path.exists(os.path.join(path, name + ext)):
        return name + ext

    counter = 1
    new_name = name
    while os.path.exists(os.path.join(path, new_name + ext)):
        new_name = f"{name}_{counter}"
        counter += 1
    return new_name + ext

def move_file(new_path, target_folder, file_ext, file_name):
    if not os.path.exists(target_folder):
        os.mkdir(target_folder)
    new_file_name = get_unique_name(target_folder, normalize(file_name), '.' + file_ext.lower())
    shutil.move(new_path, os.path.join(target_folder, new_file_name))

def process_directory(directory, root, unpack_archives, executor):
    # Типи файлів для сортування
    image_exts = ['JPEG', 'PNG', 'JPG', 'SVG']
    video_exts = ['AVI', 'MP4', 'MOV', 'MKV']
    doc_exts = ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']
    audio_exts = ['MP3', 'OGG', 'WAV', 'AMR']
    archive_exts = ['ZIP', 'GZ', 'TAR', 'RAR']

    for file in os.listdir(directory):
        old_path = os.path.join(directory, file)
        if os.path.isdir(old_path):
            # Рекурсивний виклик для підкаталогів
            executor.submit(process_directory, old_path, root, unpack_archives, executor)
        else:
            file_name, file_ext = os.path.splitext(file)
            file_ext = file_ext[1:].upper()
            new_file_name = normalize(file_name) + '.' + file_ext.lower()
            new_path = os.path.join(directory, new_file_name)
            os.rename(old_path, new_path)

            # Переміщення файлів за типами
            if file_ext in image_exts:
                executor.submit(move_file, new_path, os.path.join(root, 'images'), file_ext, file_name)
            elif file_ext in video_exts:
                executor.submit(move_file, new_path, os.path.join(root, 'video'), file_ext, file_name)
            elif file_ext in doc_exts:
                executor.submit(move_file, new_path, os.path.join(root, 'documents'), file_ext, file_name)
            elif file_ext in audio_exts:
                executor.submit(move_file, new_path, os.path.join(root, 'audio'), file_ext, file_name)
            elif file_ext in archive_exts:
                archive_dest_path = os.path.join(root, 'archives', os.path.basename(new_path))
                shutil.move(new_path, archive_dest_path)

                if unpack_archives == 'yes':
                    # Розпакування архівів, якщо потрібно
                    executor.submit(unpack, archive_dest_path, os.path.join(root, 'archives'))
            else:
                # Обробка інших типів файлів
                other_folder = os.path.join(root, 'other')
                if not os.path.exists(other_folder):
                    os.mkdir(other_folder)
                new_file_name = get_unique_name(other_folder, normalize(file_name), '.' + file_ext.lower())
                shutil.move(new_path, os.path.join(other_folder, new_file_name))

def process_folder(folder_path, unpack_archives):
    with ThreadPoolExecutor() as executor:
        process_directory(folder_path, folder_path, unpack_archives, executor)

def clean_folder_interface():
    folder_path = input("Enter the path to the folder you want to sort: ")
    if not folder_path or not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        print("You did not enter the path to the folder!!!!")
    else:
        unpack_archives = input("Do you want to unpack archives? (yes/no): ").strip().lower()
        try:
            process_folder(folder_path, unpack_archives == 'yes')
            print("Clean completed successfully.")
        except Exception as e:
            print(f"Clean was not completed due to an error: {e}")

if __name__ == "__main__":
    clean_folder_interface()
