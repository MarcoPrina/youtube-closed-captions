from ytcc.download import Download
from pathlib import Path


def main():
    id = 'PL5Qa6yv61yWK-FO2GWxHozVCjdvKRwDBz'

    download = Download(playlist=True)

    captions_files = download.get_captions(id, 'it')

    Path("../Outputs").mkdir(parents=True, exist_ok=True)

    for video_id in captions_files:
        text_file = open("../Outputs/" + video_id + ".txt", "w")

        text_file.write(captions_files[video_id])

        text_file.close()

if __name__ == "__main__":
    main()
