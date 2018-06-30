from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.webdriver import WebDriver
from text_generator.text_generator import TextGenerator

FORM_COMMENT_ID = 'comment'
FORM_NAME_ID = 'author'
FORM_EMAIL_ID = 'email'
FORM_ID = 'commentform'

COMMENT_BODY = 'comment-body'

LINK_SAMPLE_PAGE = 'Sample Page'

USERNAME = 'Pavel'
WRONG_EMAIL = 'awesome at ten dot net'
CORRECT_EMAIL = 'awesome@ten.net'

DIR = 'photos'


class TestSelenium:

    driver = None

    def setup_method(self):
        self.driver = WebDriver(command_executor='http://192.168.0.165:4444/wd/hub',
                                desired_capabilities=DesiredCapabilities.CHROME.copy())
        self.driver.get('http://store.demoqa.com')

    def teardown_method(self):
        self.driver.quit()
        self.driver = None

    def navigate_to_page(self, link_text):
        self.driver.find_element_by_link_text(link_text).click()
        self.driver.save_screenshot(f'{DIR}/{link_text}.png')

    @staticmethod
    def generate_string(size):
        # TODO I don't like how this string is generated
        text = TextGenerator()
        text.generate_dictionary(size)
        return ' '.join(map(str, text.get_dictionary()))

    def test_wrong_email_redirects_error_page(self):
        # given
        self.navigate_to_page(LINK_SAMPLE_PAGE)

        # when
        comment_form = self.driver.find_element_by_id(FORM_ID)
        comment_form.find_element_by_id(FORM_COMMENT_ID).send_keys(self.generate_string(100))
        comment_form.find_element_by_id(FORM_NAME_ID).send_keys(USERNAME)
        comment_form.find_element_by_id(FORM_EMAIL_ID).send_keys(WRONG_EMAIL)
        self.driver.save_screenshot(f'{DIR}/11-KO-wrong-email.png')
        comment_form.submit()

        # then
        self.driver.save_screenshot(f'{DIR}/12-KO-error-page.png')
        assert self.driver.title == 'Comment Submission Failure'

    def test_correct_email_adds_comment(self):
        # given
        self.navigate_to_page(LINK_SAMPLE_PAGE)

        # when
        comment = self.generate_string(100)
        comment_form = self.driver.find_element_by_id(FORM_ID)
        comment_form.find_element_by_id(FORM_COMMENT_ID).send_keys(comment)
        comment_form.find_element_by_id(FORM_NAME_ID).send_keys(USERNAME)
        comment_form.find_element_by_id(FORM_EMAIL_ID).send_keys(CORRECT_EMAIL)
        self.driver.save_screenshot(f'{DIR}/21-OK-good-email.png')
        comment_form.submit()

        # then
        self.driver.save_screenshot(f'{DIR}/22-OK-comment-post.png')
        # return url: http://store.demoqa.com/sample-page/#comment-620
        new_comment_id = self.driver.current_url.split('#')[-1]
        comment_found = self.driver.find_element_by_id(new_comment_id)
        assert comment_found is not None
        assert comment_found.find_element_by_class_name(COMMENT_BODY).text == comment

    def test_of_the_gods(self):
        # Enter a comment with a wrong email & Check Error is displayed
        # given
        self.navigate_to_page(LINK_SAMPLE_PAGE)

        # when
        comment_form = self.driver.find_element_by_id(FORM_ID)
        comment_form.find_element_by_id(FORM_COMMENT_ID).send_keys(self.generate_string(100))
        comment_form.find_element_by_id(FORM_NAME_ID).send_keys(USERNAME)
        comment_form.find_element_by_id(FORM_EMAIL_ID).send_keys(WRONG_EMAIL)
        self.driver.save_screenshot(f'{DIR}/31-GOD-KO-wrong-email.png')
        comment_form.submit()

        # then
        self.driver.save_screenshot(f'{DIR}/32-GOD-KO-error-page.png')
        assert self.driver.title == 'Comment Submission Failure'

        # Navigate back
        self.driver.back()

        # Enter a comment with a correct email & Check Comment is Received
        # given
        self.navigate_to_page(LINK_SAMPLE_PAGE)

        # when
        comment = self.generate_string(100)
        comment_form = self.driver.find_element_by_id(FORM_ID)
        comment_form.find_element_by_id(FORM_COMMENT_ID).send_keys(comment)
        comment_form.find_element_by_id(FORM_NAME_ID).send_keys(USERNAME)
        comment_form.find_element_by_id(FORM_EMAIL_ID).send_keys(CORRECT_EMAIL)
        self.driver.save_screenshot(f'{DIR}/33-GOD-OK-good-email-2.png')
        comment_form.submit()

        # then
        self.driver.save_screenshot(f'{DIR}/34-GOD-OK-comment-post.png')
        new_comment_id = self.driver.current_url.split('#')[-1]
        comment_found = self.driver.find_element_by_id(new_comment_id)
        assert comment_found is not None
        assert comment_found.find_element_by_class_name(COMMENT_BODY).text == comment
