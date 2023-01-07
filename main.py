from PhotoFolder import PhotoFolder

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    testFolder = PhotoFolder("/Users/siweihe/Desktop/日常")
    testFolder.construct_image_map()

    testFolder.override_file_time()
    testFolder.detect_duplicate_photo()
