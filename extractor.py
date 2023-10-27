import json, logging, pprint, sys
from pdf2image import convert_from_path

## set up debug-level logger using basicConfig ----------------------
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S',
    handlers=[ logging.StreamHandler(sys.stdout) ] )
log = logging.getLogger( __name__ )


def run_code():
    """ Main function. Called by __main__.py """
    ## load tracker-dict from json ----------------------------------
    tracker_dict: dict = load_tracker()
    ## get list of URLs to process ----------------------------------
    urls_to_process: list = tracker_dict['urls_to_process']

    ## extract image from PDF ---------------------------------------
    image_path = extract_image( '../downloaded_pdfs/test.pdf' )

    # process each URL ----------------------------------------------
    # for url in urls_to_process:
    #     ## see if target PDF exists in downloaded-files
    #     pdf_path: str = ''
    #     # pdf_path: str = check_for_pdf( url )
    #     ## if not, download it
    #     if not pdf_path:
    #         # pdf_path: str = download_pdf( url )
    #         pass
    #     ## if so, extract image
    #     image_path: str = ''
    #     if pdf_path:
    #         # image_path = extract_image( pdf_path )
    #         pass
    #     ## convert TIFF to JP2
    #     jp2_path: str = ''
    #     if image_path:
    #         # jp2_path = convert_to_jp2( image_path, tracker_dict )
    #         pass

    return


def extract_image( pdf_path: str ) -> str:
    """ Load PDF, extract image, save image, return image path. """
    log.debug( f'pdf_path, ```{pdf_path}```' )
    # Convert PDF to image
    images = pdf2image.convert_from_path(pdf_path)

    # Determine image type and extension
    image_type = images[0].format.lower()
    if image_type == 'jpeg':
        extension = 'jpg'
    elif image_type == 'png':
        extension = 'png'
    else:
        raise ValueError(f'Unsupported image type: {image_type}')

    # Save image to file with appropriate extension
    image_path = os.path.splitext(pdf_path)[0] + '.' + extension
    images[0].save(image_path, image_type.upper())

    return image_path



def load_tracker():
    """ Load tracker-dict from json """
    log.debug( 'loading tracker-dict from json' )
    tracker_dict: dict = {}
    try:
        with open( '../tracker/tracker.json', 'r' ) as f:
            tracker_dict = json.load( f )
    except FileNotFoundError:
        tracker_dict = {
            'urls_to_process': [],
            'urls_processed': [],
            'pdfs_downloaded': [],
            'images_extracted': [],
            'jp2s_created': [],
        }
        tracker_jsn = json.dumps( tracker_dict )
        with open( '../tracker/tracker.json', 'w' ) as f:
            f.write( tracker_jsn )
    assert tracker_dict != {}, 'tracker_dict is empty'
    log.debug( f'tracker_dict: {pprint.pformat(tracker_dict)}' )
    return tracker_dict  

if __name__ == '__main__':
    run_code()