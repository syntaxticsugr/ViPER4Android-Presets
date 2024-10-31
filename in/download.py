import os
import gdown



def download_files(download_dir, file_ids):

    for author, file_id in file_ids.items():

        download_dir = f'{download_dir}/{author}'
        os.makedirs(download_dir, exist_ok=True)

        output = f'{download_dir}/{author}.zip'

        gdown.download(id=file_id, output=output)



if __name__ == "__main__":

    download_dir = 'in'

    file_ids = {
        'jadilson12': '19pn29medRLzy8m9uPzkPmpvPSgHIsbz7',
        'Joe0Bloggs': '19rEUl8QlBUWpgWrpaMxv2XnEVpZxXavV',
        'JohnFawkes': '19thPV8G2eOohh-ihUJadEL3bwqwgvd-G'
    }

    download_files(download_dir, file_ids)
