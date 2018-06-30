from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.webdriver import WebDriver
from text_generator.text_generator import TextGenerator
from sample_page import SamplePage


# HTML ID's
COMMENT_BODY_ID = 'comment-body'
ERROR_MESSAGE_ID = 'error-page'

# HTML Text Link
SAMPLE_PAGE = 'Sample Page'

# HTML messages
ERROR_MESSAGE = 'ERROR: please enter a valid email address.'

# HMTL Form data
NAME = 'Pavel'
WRONG_EMAIL = 'awesome at ten dot net'
CORRECT_EMAIL = 'awesome@ten.net'

# Root directory to save data in case of screenshots
DIR = 'photos'


class TestSelenium:

    driver = None
    sample_page = None

        self.driver = WebDriver(command_executor='http://192.168.0.165:4444/wd/hub',
                                desired_capabilities=DesiredCapabilities.CHROME.copy())
        self.driver.get('http://store.demoqa.com')
        self.navigate_to_page(SAMPLE_PAGE)
        self.sample_page = SamplePage(self.driver)

        self.driver.close()
        self.driver.quit()
        self.driver = None
        self.sample_page = None

    def navigate_to_page(self, link_text):
        self.driver.find_element_by_link_text(link_text).click()
        self.driver.save_screenshot(f'{DIR}/{link_text}.png')

    @staticmethod
    def generate_string(size):
        # TODO I don't like how this string is generated
        text = TextGenerator()
        text.generate_dictionary(size)
        return ' '.join(map(str, text.get_dictionary()))

    def test_wrong_email_redirects_error_page(self, request):
        """
        Writes a comment with wrong email, saves a screenshot.
        Checks that error messages appears.
        :param request: pytest fixture with built in methods
        :return:
        """
        # when
        comment = self.generate_string(100)
        self.sample_page.write_comment(comment, NAME, WRONG_EMAIL)
        self.driver.save_screenshot(f'{DIR}/{request.node.name}.png')

        # then
        error = self.driver.find_element_by_id(ERROR_MESSAGE_ID)
        assert ERROR_MESSAGE in error.text

    def test_correct_email_adds_comment(self, request):
        """
        Writes a comment with correct email, saves a screenshot.
        Checks that comment was inserted and it has the correct value.
        :param request: pytest fixture with built in methods
        :return:
        """
        # when
        comment = self.generate_string(100)
        self.sample_page.write_comment(comment, NAME, CORRECT_EMAIL)

        # then
        # TODO self.driver.current_url works, but is a bit out of context, maybe it should be returned by .write_comment
        comment_found = self.sample_page.get_comment(self.driver.current_url)
        self.driver.save_screenshot(f'{DIR}/{request.node.name}.png')

        assert comment_found is not None
        assert comment == comment_found.find_element_by_class_name(COMMENT_BODY_ID).text

    def test_of_the_gods(self, request):
        """
        Does everything, writes a comment with wrong email, checks that error messages appears, goes back,
        writes a new comment with correct email, saves a screenshot, checks that comment was inserted and it
        has the correct value.
        :param request: pytest fixture with built in methods
        :return:
        """
        # Enter a comment with a wrong email & Check Error is displayed
        # when
        self.sample_page.write_comment(self.generate_string(100), NAME, WRONG_EMAIL)

        # then
        error = self.driver.find_element_by_id(ERROR_MESSAGE_ID)
        assert ERROR_MESSAGE in error.text

        # Navigate to Sample Page
        self.driver.back()

        # Enter a comment with a correct email & Check Comment is Received
        # when
        # Chrome keeps values previously typed
        self.sample_page.clear_fields()
        comment = self.generate_string(100)
        self.sample_page.write_comment(comment, NAME, CORRECT_EMAIL)

        # TODO self.driver.current_url works, but is a bit out of context, maybe it should be returned by .write_comment
        comment_found = self.sample_page.get_comment(self.driver.current_url)
        self.driver.save_screenshot(f'{DIR}/{request.node.name}.png')

        assert comment_found is not None
        assert comment_found.find_element_by_class_name(COMMENT_BODY_ID).text == comment
