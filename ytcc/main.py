from ytcc.download import Download


def main():
    video_id = 'PL5Qa6yv61yWK-FO2GWxHozVCjdvKRwDBz'

    download = Download(playlist=True)

    captions_files = download.get_captions(video_id, 'it')

    for id in captions_files:
        text_file = open(id + ".txt", "w")

        text_file.write(captions_files[id])

        text_file.close()

if __name__ == "__main__":
    main()

