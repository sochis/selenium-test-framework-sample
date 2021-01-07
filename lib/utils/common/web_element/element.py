# pylint: disable=E1136
""" RNPS Element Module. """
from typing import cast, List, Optional, Union
from enum import Enum, auto
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException

from selenium.webdriver import Remote
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement

from .exceptions import MoveToError, FocusToError

logger = logging.getLogger(__name__)


class Method(Enum):
    """ Which selected Expected Conditions. """
    VISIBILITY = auto()
    INVISIBILITY = auto()
    PRESENCE = auto()


class FormatError(Exception):
    """ Invalid arguments error to format Element ID """


class Element:
    """ RNPS Element Utility class.
    Attributes:
        driver(Remote): Web Driver.
        id_(str): Element id. test_id or xpath.
        parent(Optional[WebElement]): Parent WebElement (default=None).
        xpath(bool): xpath flag.
    """
    def __init__(self,
                 driver: Remote,
                 id_: str,
                 parent: Union[WebElement, Remote],
                 xpath: bool = False) -> None:
        self.driver: Remote = driver
        self._parent = parent
        self._id = id_
        self.root: Union[Remote, WebElement] = self._parent

        if xpath:
            self.mode = By.XPATH
        else:
            self.mode = By.ID

    def __get_element(self,
                      target: str,
                      by: By,
                      method: Method = Method.VISIBILITY,
                      max_wait: int = 30) -> WebElement:
        """ Wait until Web Element of 'target' is 'method'.
        Arguments:
            target(str): target id.
            by(By): search target by.
            method(Method): type of expected condition.
            max_wait(int): maximum wait time for display elements (default=30sec).
        Returns:
            WebElement: An element with the specified test ID.
        Raises:
            TimeoutException: element is not found.
            ValueError: invalid method name.
        """
        try:
            if method == Method.VISIBILITY:
                elem = WebDriverWait(self.root, max_wait).until(
                    ec.visibility_of_element_located((by, target)))
            elif method == Method.INVISIBILITY:
                elem = WebDriverWait(self.root, max_wait).until(
                    ec.invisibility_of_element_located((by, target)))
            elif method == Method.PRESENCE:
                elem = WebDriverWait(self.root, max_wait).until(
                    ec.presence_of_element_located((by, target)))
            else:
                raise ValueError(f'Invalid method name: {method}')
        except TimeoutException as e:
            e.msg = f'Waiting for {max_wait} sec, but element with target of "{target}":"{by}":"{method}" is Not Found.'
            raise e
        return elem

    def __get_elements(self,
                       target: str,
                       by: By,
                       method: Method = Method.VISIBILITY,
                       max_wait: int = 30) -> List[WebElement]:
        """ Get list of Web Elements of 'target'.
        Arguments:
            target(str): target id.
            by(By): search method.
            method(Method): type of expected condition.
            max_wait(int): maximum wait time to find elements (default = 10sec).
        Returns:
            List[WebElements]: a list of WebElements.
        Raises:
            TimeoutException: element is not found.
            ValueError: invalid method name.
        """
        try:
            elem_list: List[WebElement]
            if method == Method.VISIBILITY:
                elem_list = WebDriverWait(self.root, max_wait).until(
                    ec.visibility_of_all_elements_located((by, target)))
            elif method == Method.PRESENCE:
                elem_list = WebDriverWait(self.root, max_wait).until(
                    ec.presence_of_all_elements_located((by, target)))
            else:
                raise ValueError(f'Invalid method name: {method}')
        except TimeoutException as e:
            e.msg = f'Waiting for {max_wait} sec, but element with target of "{target}":"{by}":"{method}" is Not Found.'
            raise e
        return elem_list

    def __move_to_element(self, element: WebElement) -> WebElement:
        """ Move to the displayed Web Element of 'target'.
        Arguments:
            element(str): webElement.
        Returns:
            WebElement: An element with the specified test ID.
        Raises:
            MoveToError: failed to move to element.
        """
        try:
            ActionChains(self.root).move_to_element(element).perform()
            logger.debug('Move to element of target : %s', self._id)
        except WebDriverException as e:
            raise MoveToError(
                f'Another exception occurred when trying to move to element "{self._id}":"{self.mode}"'
            ) from e
        return element

    def __click_element(self, element: WebElement) -> None:
        """ Move and click on Web Element.
        Arguments:
            element(str): webElement.
        Raises:
            MoveToError: failed to move to element.
        """
        try:
            element.location_once_scrolled_into_view  # pylint: disable=W0104
            element.click()
            logger.debug('Click element of target : %s', self._id)
        except TimeoutException as e:
            raise MoveToError(
                f'Failed to click to element with target "{self._id}":"{self.mode}"'
            ) from e

    def __format_element_id(self, *args: str, **kwargs: str) -> str:
        """ Format self._id
        Arguments:
            *args(str): values for positional arguments field in _id
            **kwargs(str): values for keyword arguments field in _id
        Returns:
            str: formatted _id
        Raises:
            FormatError: Invalid argument
        """
        try:
            return self._id.format(*args, **kwargs)
        except (IndexError, KeyError) as e:
            raise FormatError(
                f'The element must take arguments. element_id: {self._id}'
            ) from e

    def get(self,
            *args: str,
            method: Method = Method.PRESENCE,
            max_wait: int = 10,
            **kwargs: str) -> WebElement:
        """ Get Web Element.
        Arguments:
            method(Method): type of expected condition.
            max_wait(int): maximum wait time for display elements (default=10sec).
            *args(str): arguments for _id.
            **kwargs(str): keyword arguments for _id.
        Returns:
            WebElement: An element with the specified target.
        Raises:
            TimeoutException: element is not found.
            ValueError: invalid method name.
        """
        self._id = self.__format_element_id(*args, **kwargs)
        return self.__get_element(self._id,
                                  self.mode,
                                  method=method,
                                  max_wait=max_wait)

    def get_elements(self,
                     *args: str,
                     method: Method = Method.PRESENCE,
                     max_wait: int = 10,
                     **kwargs: str) -> List[WebElement]:
        """ Get List of Web Elements.
        Arguments:
            method(Method): type of expected condition.
            max_wait(int): max wait time to find elements (default = 10 sec).
            *args(str): arguments for _id.
            **kwargs(str): keyword arguments for _id.
        Returns:
            List[WebElement]: A list of web elements.
        Raises:
            TimeoutException: element is not found.
            ValueError: invalid method name.
        """
        self._id = self.__format_element_id(*args, **kwargs)
        elem_list = self.__get_elements(self._id,
                                        self.mode,
                                        method=method,
                                        max_wait=max_wait)
        return elem_list

    def get_attribute(self,
                      name: str,
                      *args: str,
                      max_wait: int = 10,
                      **kwargs: str) -> Optional[str]:
        """ Get Web Element Attribute.
        Arguments:
            name(str): attribute name.
            max_wait(int): maximum wait time for display elements (default=10sec).
            *args(str): arguments for _id.
            **kwargs(str): keyword arguments for _id.
        Returns:
            Optional[str]: return value if attribute exists, None otherwise.
        Raises:
            TimeoutException: element is not found.
        """
        elem = self.get(*args,
                        method=Method.PRESENCE,
                        max_wait=max_wait,
                        **kwargs)
        return cast(str, elem.get_attribute(name))

    def move_to(self, *args: str, max_wait: int = 10, **kwargs: str) -> None:
        """ Move to Web Element.
        Arguments:
            max_wait(int): maximum wait time for display elements (default=10sec).
            *args(str): arguments for _id.
            **kwargs(str): keyword arguments for _id.
        Raises:
            MoveToError: failed to move to element.
        """
        elem = self.get(*args,
                        method=Method.PRESENCE,
                        max_wait=max_wait,
                        **kwargs)
        self.__move_to_element(elem)

    def click(self, *args: str, max_wait: int = 10, **kwargs: str) -> None:
        """ Click Web Element.
        Arguments:
            max_wait(int): maximum wait time for display elements (default=10sec).
            *args(str): arguments for _id.
            **kwargs(str): keyword arguments for _id.
        Raises:
            MoveToError: failed to move to element.
        """
        elem = self.get(*args,
                        method=Method.PRESENCE,
                        max_wait=max_wait,
                        **kwargs)
        self.__click_element(elem)

    def focus(self,
              *args: str,
              max_wait: int = 10,
              prevent_scroll: bool = True,
              **kwargs: str) -> None:
        """ Focus to the displayed Web Element of 'target'.
        Arguments:
            max_wait(int): maximum wait time for display elements (default=10sec).
            prevent_scroll(bool): prevent scroll when focusing element (default=False).
            *args(str): arguments for _id.
            **kwargs(str): keyword arguments for _id.
        Raises:
            FocusToError: failed to focus to element.
        """
        try:
            elem = self.get(*args,
                            method=Method.PRESENCE,
                            max_wait=max_wait,
                            **kwargs)
            focus_to_element_js = "arguments[0].focus({'preventScroll': arguments[1]})"
            self.driver.execute_script(focus_to_element_js, elem,
                                       prevent_scroll)
        except WebDriverException as e:
            raise FocusToError(
                f'Failed to focus to element with target "{self._id}":"{self.mode}"'
            ) from e

    def send_keys(self,
                  keys: str,
                  *args: str,
                  max_wait: int = 10,
                  clear: bool = True,
                  **kwargs: str) -> None:
        """ SendKeys to Web Element.
        Arguments:
            keys(str): input keys.
            max_wait(int): maximum wait time for display elements (default=10sec).
            clear(bool): clear text before input text. when you send file, this should be False (default=True).
            *args:(str): arguments for _id.
            **kwargs(str): keyword arguments for _id.
        Raises:
            TimeoutException: element is not found.
        """
        elem = self.get(*args,
                        method=Method.PRESENCE,
                        max_wait=max_wait,
                        **kwargs)
        if clear:
            elem.clear()
        elem.send_keys(keys)

    def wait_for_text(self,
                      expected_text: str,
                      *args: str,
                      max_wait: int = 10,
                      value_flag: bool = False,
                      **kwargs: str) -> bool:
        """ Wait for expected text to be displayed in Web Element Text Attribute.
        Arguments:
            expected_text(str): value of text attribute.
            max_wait(int): maximum wait time for text attribute (default=10sec).
            value_flag(bool): search attribute value or not (default=False).
            *args(str): arguments for _id.
            **kwargs(str): keyword arguments for _id.
        Returns:
            bool: return True if expected value exists, False otherwise.
        """
        self._id = self.__format_element_id(*args, **kwargs)
        try:
            if value_flag:
                WebDriverWait(self.root, max_wait).until(
                    ec.text_to_be_present_in_element_value(
                        (self.mode, self._id), expected_text))
            else:
                WebDriverWait(self.root, max_wait).until(
                    ec.text_to_be_present_in_element((self.mode, self._id),
                                                     expected_text))

        except TimeoutException:
            logger.debug(
                f'Waiting for {max_wait} sec, but text attribute is not "{expected_text}".'
            )
            return False
        return True

    def is_displayed(self,
                     *args: str,
                     max_wait: int = 10,
                     **kwargs: str) -> bool:
        """ Web Element is displayed.
        Arguments:
            max_wait(int): maximum wait time for display elements (default=10sec).
            *args(str): arguments for _id.
            **kwargs(str): keyword arguments for _id.
        Returns:
            bool: return True if element displayed, False otherwise.
        """
        try:
            self.get(*args,
                     method=Method.PRESENCE,
                     max_wait=max_wait,
                     **kwargs)
        except TimeoutException:
            return False
        return True

    def is_hidden(self, *args: str, max_wait: int = 10, **kwargs: str) -> bool:
        """ Web Element is hidden.
        Arguments:
            max_wait(int): maximum wait time for element to become invisible (default=10sec).
            *args(str): arguments for _id.
            **kwargs(str): keyword arguments for _id.
        Returns:
            result(bool): return True if element is hidden, False otherwise.
        """
        try:
            self.get(*args,
                     method=Method.INVISIBILITY,
                     max_wait=max_wait,
                     **kwargs)
        except TimeoutException:
            return False
        return True
