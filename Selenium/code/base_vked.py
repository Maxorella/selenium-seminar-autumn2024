import time
from contextlib import contextmanager
import json
import pytest
from _pytest.fixtures import FixtureRequest
from ui.locators.vked_locators import AuthPageLocators

CLICK_RETRY = 3


class BaseCaseVkEd:
    authorize = True
    driver = None

    @contextmanager
    def switch_to_window(self, current, close=False):
        for w in self.driver.window_handles:
            if w != current:
                self.driver.switch_to.window(w)
                break
        yield
        if close:
            self.driver.close()
        self.driver.switch_to.window(current)


    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest):
        self.driver = driver
        self.config = config

        self.login_page = (request.getfixturevalue('login_vked_page'))
        self.email = (request.getfixturevalue('credentials_vked'))['email']
        self.password = (request.getfixturevalue('credentials_vked'))['password']
        self.profile_fi = (request.getfixturevalue('credentials_vked'))['profile_fi']

        if self.authorize:
            self.login_page.click(AuthPageLocators.REG_BTN_LOC, 5)
            self.login_page.click(AuthPageLocators.GO_WITH_EMAIL_BTN_LOC, 5)
            self.login_page.enter_field(AuthPageLocators.EMAIL_INP_LOC, self.email, 5)
            self.login_page.enter_field(AuthPageLocators.PASSWORD_INP_LOC, self.password, 5)
            print("here1")
            # self.login_page.click(AuthPageLocators.SUBMIT_ENTER_BTN_LOC, 10)
            print("here2")
            self.login_page.check_text(AuthPageLocators.PROFILE_FIO_LOC, self.profile_fi, 10) #TODO из userdata.json
