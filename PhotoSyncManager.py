from PhotoFolder import PhotoFolder

class PhotoSyncManager:
    def __init__(self, srcFolder, dstFolder):
        self.srcFolder = PhotoFolder(srcFolder)
        self.dstFolder = PhotoFolder(dstFolder)

    def preProcess(self):
        raise NotImplementedError


    def startTransfer(self):
        raise NotImplementedError