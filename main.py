from ytcc.download import Download
from pathlib import Path


def main():
    id = 'PL4cUxeGkcC9jticTs2l6Nt2lsybNW0-4O'

    download = Download(playlist=len(id) > 12)

    captions_files = download.get_captions(id, 'it')

    Path("../Outputs").mkdir(parents=True, exist_ok=True)

    for video_id in captions_files:
        text_file = open("../Outputs/" + video_id + ".txt", "w")

        text_file.write(captions_files[video_id])

        text_file.close()


if __name__ == "__main__":
    main()
