from flask_testing import TestCase
from os.path import abspath, sep
from reddit.common.tools.env import ResourceLoader
from reddit.common.web.renderer import RenderFormat
from reddit.constants import ROOT, BASE
import json
import os
import unittest
from reddit.common.app import startup_app


class BasicTestCase(TestCase):
    '''
        base TestCase for all unit TestCase.
    '''

    def __init__(self, *args, **kwargs):
        super(BasicTestCase, self).__init__(*args, **kwargs)

    def create_app(self):
        if not os.environ.has_key(ResourceLoader.ENV_VAR_NAME):
            test_folder = os.path.abspath(os.path.join(BASE, './resources/test'))
            os.environ.setdefault(ResourceLoader.ENV_VAR_NAME, test_folder)
        app = startup_app()
        self._app = app
        return self._app

    def setUp(self):
        self.default_login()

    def tearDown(self):
        self.logout()


    def _build_parameters(self, data, kwargs):
        parameters = data or {}
        parameters.update(kwargs or {})
        if 'rformat' not in parameters:
            parameters['rformat'] = RenderFormat.JSON
        return json.dumps(parameters)

    def request(self, method, path, data=None, return_response=False, **kwargs):
        requestor = getattr(self.client, method)
        response = requestor(path,
                             data=self._build_parameters(data, kwargs),
                             content_type='application/json')
        if return_response:
            return response

        return self.get_result(response)


    def get_result(self, response):
        status = response.status_code
        self.assertEqual(status, 200,
            "Except status code 200, in fact: %s" % (response.data))
        result = json.loads(response.data)
        return result['result']

    def assert_failed_result(self, response, code, message=None):
        status = response.status_code
        self.assertTrue(status >= 400 and status < 500)

        result = json.loads(response.data)
        code_diff_message = "expect code is: %s, in fact: %s"
        msg_diff_message = "expect msg is : %s, in fact: %s"
        self.assertEqual(result['error_code'],
                         code,
                         code_diff_message % (code, result['error_code']))
        if message:
            self.assertEqual(result['error_msg'],
                             message,
                             msg_diff_message % (message, result['error_msg']))
        return result

    def assert_error_code(self, response, error_code, *args):
        msg = error_code[1].format(*args) if args else error_code[1]
        self.assert_failed_result(response, error_code[0], msg)

    def get_list(self, path, where=None, expect_size=None):
        if where:
            result = self.request('get', path, where=json.dumps(where))
        else:
            result = self.request('get', path)
        data = result['data']
        assert isinstance(data, list)
        if expect_size:
            error_msg = "length is {}, but the expert is {}".format(len(data), expect_size)
            self.assertEqual(expect_size, len(data), error_msg)
        return data
