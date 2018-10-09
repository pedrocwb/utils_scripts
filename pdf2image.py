import os 
import sys
import glob
import argparse
import logging
from wand.image import Image
from PIL import Image as Img

logging.basicConfig(format="%(asctime)s - %(module)s - %(levelname)s: %(message)s", level=logging.DEBUG)


class PdfConverter:
    
    def pdf2jpg(self, pdfpath, fileext, output):
        try:
            logging.info(pdfpath)
            base = os.path.basename(pdfpath)

            with Image(filename=pdfpath, resolution=200) as img:
                img.compression_quality = 80
                img.save(filename=output + "/" + os.path.splitext(base)[0] + "." + fileext)

        except Exception as err:
            logging.error("Error in converting to jpg", err)
            return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(dest="path", help="Folder or pdf file to be converted")
    parser.add_argument('--ext', dest='ext', help="File exentension", default="jpg")
    parser.add_argument('--output', dest='output', help="Output directory", default="output")

    args = parser.parse_args()

    files = []
    if os.path.isfile(args.path):
        if args.path.endswith(".pdf"):
            logging.info("Processing PDF file")
            files.append(args.path)
        else:
            logging.error("Only supports pdf files")
            sys.exit(1)
    
    if os.path.isdir(args.path):
        logging.info("Listing PDF files in folder %s" % args.path )
        files = sorted(glob.glob(args.path + '/*.pdf'))

    outdir  = args.output
    if not os.path.isdir(args.output):
        os.mkdir(args.output)

    extensions = ['jpg', 'jpeg', 'png', 'gif']
    if args.ext in extensions:
        fileext = args.ext
    else:
        logging.error("Extension not supported")
        sys.exit(1)

        
    cvt = PdfConverter()
    for f in files:
        cvt.pdf2jpg(f, fileext, outdir)

