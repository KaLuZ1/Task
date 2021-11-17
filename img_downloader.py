import sys
import urllib.request
import urllib.error

_error_messages = []

# check if URL ends with .jpg
def is_image_link(url):
    if not url.endswith('.jpg'):
        _error_messages.append('\'{}\' is not linked to a jpg file.'.format(url))
        return False
    return True

# remove next line (\n) from string if needed 
def clean_file_line(line):
    if line.endswith('\n'):
        return line[:-1]
    return line

# returns true when the image has been downloaded 
def download_image(url):
    image_name = url.split('/')[-1]   # get image name from link
    try:
        urllib.request.urlretrieve(url, image_name)   # download image
    except urllib.error.URLError:
        _error_messages.append('URL \'{}\' is not reachable.'.format(url))
        return False
    except ValueError:
        _error_messages.append('\'{}\' is not an URL.'.format(url))
        return False
    return True

# print out the result
def generate_info_message(filename, line_count, statistic):
    successful_downloads = len(list(filter(lambda x: x, statistic)))    # calculates how many images have been downloaded

    error_caption = 'The following lines could not be resolved:\n'
    error_info = '\n'.join(_error_messages)
    conclusion_info = '\nOut of {} contained lines from the file \'{}\', {} images were downloaded.'.format(line_count, filename, successful_downloads)

    info = [error_caption, error_info, conclusion_info]
    return info

def main(filename):
    file = open(filename, 'r')

    lines = file.readlines()     # get list of all lines
    urls = [clean_file_line(x) for x in lines]   # generate list without next line endings
    img_urls = filter(is_image_link, urls)      # filter the image links
    statistic = list(map(download_image, img_urls))    # download imges and safe statistic
    
    print(*generate_info_message(filename, len(lines), statistic), sep='\n')
    file.close 

if (__name__ == '__main__'):
    main(sys.argv[1])   # pass only the first parameter