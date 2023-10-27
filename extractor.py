import json, logging, sys

## set up debug-level logger using basicConfig ----------------------
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S',
    handlers=[ logging.StreamHandler(sys.stdout) ] )
log = logging.getLogger( __name__ )


def run_code():
    """ Main function. Called by __main__.py """
    # load tracker-dict from json -----------------------------------
    tracker_dict: dict = load_tracker()
    # get list of URLs to process -----------------------------------
    urls_to_process: list = tracker_dict['urls_to_process']
    for url in urls_to_process:
        ## see if target PDF exists in downloaded-files
        pdf_path: str = ''
        pdf_path: str = check_for_pdf( url )
        ## if not, download it
        if not pdf_path:
            pdf_path: str = download_pdf( url )
        ## if so, extract image
        image_path: str = ''
        if pdf_path:
            image_path = extract_image( pdf_path )
        ## convert TIFF to JP2
        jp2_path: str = ''
        if image_path:
            jp2_path = convert_to_jp2( image_path, tracker_dict )
    return


def load_tracker():
    """ Load tracker-dict from json """
    tracker_dict: dict = {}
    try:
        with open( 'tracker.json', 'r' ) as f:
            tracker_dict = json.load( f )
    except FileNotFoundError:
        tracker_dict = {
            'urls_to_process': [],
            'urls_processed': [],
            'pdfs_downloaded': [],
            'images_extracted': [],
            'jp2s_created': [],
            'jp2s_uploaded': [],
            'jp2s_deleted': []
        }
    return tracker_dict  

if __name__ == '__main__':
    run_code()