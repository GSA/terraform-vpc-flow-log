import boto3
import socket
import subprocess
import unittest
import urllib
import warnings

class TestStringMethods(unittest.TestCase):

    def can_connect_to_port(self, host, port):
        # https://stackoverflow.com/a/20541919
        s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((host, port))
        s.close()
        return result == 0

    def get_terraform_output(self, name):
        result = subprocess.run(['terraform', 'output', name], stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8').strip()

    def get_log_group(self):
        return self.get_terraform_output('log_group_name')

    def get_flow_logs(self):
        client = boto3.client('logs')

        log_group = self.get_log_group()
        ip = self.get_my_ip()

        response = client.filter_log_events(
            logGroupName=log_group,
            filterPattern=ip,
            limit=1
        )
        return response['events']

    def get_my_ip(self):
        url = 'http://checkip.amazonaws.com/'
        with urllib.request.urlopen(url) as response:
            content = response.read()
            return content.decode('utf-8').strip()

    def test_connect_to_test_instance(self):
        instance_ip = self.get_terraform_output('ip')
        self.assertTrue(self.can_connect_to_port(instance_ip, 22))

    def test_logs_present(self):
        # workaround for https://github.com/boto/boto3/issues/454
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', ResourceWarning)

            events = self.get_flow_logs()

        self.assertGreater(len(events), 0)

if __name__ == '__main__':
    unittest.main()
