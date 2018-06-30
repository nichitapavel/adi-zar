from selenium.common.exceptions import NoSuchElementException
from logging import getLogger

FORM_COMMENT_ID = 'comment'
FORM_NAME_ID = 'author'
FORM_EMAIL_ID = 'email'
FORM_ID = 'commentform'


class SamplePage:

    def __init__(self, driver):
        self.driver = driver
        self.logger = getLogger(self.__class__.__name__)

    def write_comment(self, comment, name, email):
        """
        Fills in the form fields with data and submit it.
        :param comment: String
        :param name: String
        :param email: String
        :return:
        """
        comment_form = self.driver.find_element_by_id(FORM_ID)
        comment_form.find_element_by_id(FORM_COMMENT_ID).send_keys(comment)
        comment_form.find_element_by_id(FORM_NAME_ID).send_keys(name)
        comment_form.find_element_by_id(FORM_EMAIL_ID).send_keys(email)
        comment_form.submit()

    def get_comment(self, comment_url):
        """
        Gets the last part of a url, it has the same name as the ID of the comment.
        :param comment_url: a string in url format i.e. http://store.demoqa.com/sample-page/#comment-620
        :return: WebElement if found, None otherwise
        """
        comment_id = comment_url.split('#')[-1]
        try:
            return self.driver.find_element_by_id(comment_id)
        except NoSuchElementException as e:
            self.logger.error(f'Comment with id: {comment_id}, not found in url: {comment_url}\n {e}')
            return None

    def clear_fields(self):
        """
        Just remove any text from the form fields
        :return:
        """
        comment_form = self.driver.find_element_by_id(FORM_ID)
        comment_form.find_element_by_id(FORM_COMMENT_ID).clear()
        comment_form.find_element_by_id(FORM_NAME_ID).clear()
        comment_form.find_element_by_id(FORM_EMAIL_ID).clear()
