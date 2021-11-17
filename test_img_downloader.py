import unittest
import img_downloader
import os
import urllib.error

class TestImgDownloader(unittest.TestCase):

    # test method is_image_link from img_downloader
    def test_file_ending(self):
        # test if URL linked to a jpg file
        self.assertTrue(img_downloader.is_image_link('httywebserver.com/images/24174.jpg'))
        self.assertTrue(img_downloader.is_image_link('httpmewebsrv.com/img/testing.jpg'))
        # test if URL is not linked to a jpg file
        self.assertFalse(img_downloader.is_image_link('downloadlink'))
        self.assertFalse(img_downloader.is_image_link('httsomewebsrv.com/img/jpg'))
        self.assertFalse(img_downloader.is_image_link('httpomewebsrv.com/img/testing-jpg'))
    
    # test method clean_file_line from img_downloader
    def test_cleaning_line(self):
        self.assertEqual(img_downloader.clean_file_line('this is a string\n'), 'this is a string')
        self.assertEqual(img_downloader.clean_file_line('this is a string'), 'this is a string')
        self.assertEqual(img_downloader.clean_file_line('httpwebsrv.com/img/992147.jpg\n'), 'httpwebsrv.com/img/992147.jpg')
        self.assertEqual(img_downloader.clean_file_line('\n'), '')
    
    # test method download_image from img_downloader
    def test_download(self):
        self.assertFalse(img_downloader.download_image('httpsnot.reachable/url.jpg'))
        self.assertFalse(img_downloader.download_image('not a valid url'))

    def test_error_info(self):
        img_downloader._error_messages = []
        urls = ['downloadlink', 'not a valid url', 'httpsnot.reachable/url.jpg']
        img_downloader.is_image_link(urls[0])
        img_downloader.download_image(urls[1])
        img_downloader.download_image(urls[2])
        error_info = '\'{}\' is not linked to a jpg file.\n\'{}\' is not an URL.\n\'{}\' is not an URL.'.format(urls[0], urls[1], urls[2])
        self.assertEqual(img_downloader.generate_info_message('filename', 3, [True, False, False])[1], error_info)

    def test_error_return(self):
        self.assertEqual(len(img_downloader.generate_info_message('filename', 3, [True, False, True])), 3)
    
    def test_conclusion_info(self):
        conclusion_info = '\nOut of {} contained lines from the file \'filename\', {} images were downloaded.'.format(5, 3)
        self.assertEqual(img_downloader.generate_info_message('filename', 5, [True, False, True, False, True])[2], conclusion_info)
        
        conclusion_info = '\nOut of {} contained lines from the file \'filename\', {} images were downloaded.'.format(10, 0)
        self.assertEqual(img_downloader.generate_info_message('filename', 10, [])[2], conclusion_info)