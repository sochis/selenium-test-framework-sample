""" Decorator for RNPS POM. """
import logging
from typing import TypeVar, Mapping, Any, Union, Optional, Callable, Tuple, List, cast, Dict

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from .element import Element

logger = logging.getLogger(__name__)

# yapf: disable
# pylint: disable=E1136
Tclass = TypeVar('Tclass')

""" Type alias for possible values of Test ID Dictionary """
TestIDValueType = Union[
    str,  # TestID: 'popup'
    Tuple[str, By]]  # XPath: ('//*[@TestId="popup"]//Label[1]', By.XPATH)

AttrValue = Optional[Union[Element, List[Element]]]


# yapf: enable


def id_formatter(element_id: str, test_id_param: Dict[str, str]) -> str:
    """ format element_id string
    Arguments:
        element_id(str): raw element_id (path string in TEST_IDS.values)
        test_id_param(Dict[str, str]): keyword argument values
    Returns:
        str: formatted element_id
    """
    for key, value in test_id_param.items():
        element_id = element_id.replace(f'{{{key}}}', value)
    return element_id


def elements(test_ids: Mapping[str, object]) -> Callable[[Tclass], Tclass]:
    """ Decorator to add properties to a class.
    Arguments:
        test_ids(Mapping[str, object]): test_id dictionary object.
    Returns:
        class(Callable[[Tclass], Tclass]): Class with properties named by values in the test_ids dictionary.
    """

    def deco(cls: Tclass) -> Tclass:
        """ Sets up each property to be Element """
        value = None
        for test_id_key, value in test_ids.items():

            def get_attr(
                    self: Any,
                    test_id_value: TestIDValueType = cast(TestIDValueType, value)
            ) -> AttrValue:
                """ Returns an Element or Element List.
                Arguments:
                    self(Any): Component or Application Instance.
                    test_id_value(TestIDValueType): value of Test ID Dictionary.
                Returns:
                    AttrValue: None or Element or List[Element]
                Raises:
                    TimeoutException: WebElement is not found, only when specifying Component type.
                """
                parent_element = self.driver
                if 'parent_element' in vars(self):
                    parent_element = self.parent_element

                if isinstance(test_id_value, tuple):
                    element_id = test_id_value[0]
                    page_object_type = test_id_value[1]
                    if isinstance(element_id, str):
                        if hasattr(self, 'test_id_param'):
                            element_id = id_formatter(element_id,
                                                      self.test_id_param)
                        if page_object_type is By.XPATH:
                            return Element(self.driver, element_id,
                                           parent_element or self.driver, True)
                        if page_object_type is By.ID:
                            return Element(self.driver, element_id,
                                           parent_element or self.driver,
                                           False)
                    by = By.ID
                    if isinstance(element_id, tuple):
                        by = By.XPATH
                        element_id = element_id[0]

                    root = parent_element if parent_element else self.driver
                    try:
                        elems = WebDriverWait(root, 10).until(
                            ec.presence_of_all_elements_located(
                                (by, element_id)))
                    except TimeoutException as e:
                        e.msg = f'Waiting for 10 sec, but element "{element_id}":"{by}" is Not Found.'
                        raise e
                    return [page_object_type(self.driver, e) for e in elems]

                element_id = test_id_value
                if hasattr(self, 'test_id_param'):
                    element_id = id_formatter(test_id_value,
                                              self.test_id_param)
                return Element(self.driver, element_id, parent_element or self.driver, False)

            prop = property(get_attr)
            setattr(cls, test_id_key, prop)
        return cls

    return deco
