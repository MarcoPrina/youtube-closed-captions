from ytcc.download import Download


def main():
    video_id = 'fsLrmfA_QF8'
    download = Download()
    # Language is optional and default to "en"
    # YouTube uses "en","fr" not "en-US", "fr-FR"
    captions = download.get_captions(video_id, 'it')

    text_file = open("Output.txt", "w")

    text_file.write(captions)

    text_file.close()

if __name__ == "__main__":
    main()

