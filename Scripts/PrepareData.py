from deep_learning_compression.Storage.Storage import Storage

if __name__ == "__main__":

    s = Storage()
    sets = s.GetAllDataSetInformation()

    print("Found following datasets:")
    [print(f"\t- {s.Name}") for s in sets]
    print("\n")

    s.DownloadAndPrepareAllDatasets()
