class NotLanguageFileError(Exception):
    def __init__(self, m):
        super().__init__(m)




def load_lang_file(paths: list):
    langs={}
    temp={}


    for path in paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                lang=f.readlines()
            name=path.split('/')[-1].split('.')[0]
        except FileNotFoundError:
            NotLanguageFileError(f"Language file {path} not found.")
        for line in lang:
            if line[0] != "#":
                try:
                    line=line.replace("\n","")
                    key=line.split('=')[0]
                    value=line.split('=')[1]
                    temp.update({key:value})
                except IndexError:
                    continue
        langs.update({name:temp})
        temp={}
    return langs
