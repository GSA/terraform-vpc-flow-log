import boto3
from retrying import retry
import socket
import subprocess
import unittest
import urllib
import warnings


class TestVpcFlowLog(unittest.TestCase):

    def can_connect_to_port(self, host, port):
        # https://stackoverflow.com/a/20541919
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((host, port))
        s.close()
        return result == 0

    def get_terraform_output(self, name):
        cmd = ['terraform', 'output', name]
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8').strip()

    def get_log_group(self):
        return self.get_terraform_output('log_group_name')

    def is_result_empty(result):
        return not result

    # VPC flow logs can take a while to show up (over 22 minutes on 11/14/17), so retry until we get something
    @retry(
        retry_on_result=is_result_empty,
        wait_fixed=(5 * 1000),
        stop_max_delay=(25 * 60 * 1000)
    )
    def get_flow_logs(self):
        """Get flow logs pertaining to the test machine's IP address."""

        # indicate each try
        print('.', end='', flush=True)

        client = boto3.client('logs')

        log_group = self.get_log_group()
        ip = self.get_my_ip()

        response = client.filter_log_events(
            logGroupName=log_group,
            # only show events pertaining to the test machine
            filterPattern=ip,
            limit=1
        )
        return response['events']

    def get_my_ip(self):
        url = 'http://checkip.amazonaws.com/'
        with urllib.request.urlopen(url) as response:
            content = response.read()
            return content.decode('utf-8').strip()

    # Terraform will connect to the instance through its `provisioner`, but trigger here just in case that wasn't run from the same IP or something
    def test_connect_to_test_instance(self):
        instance_ip = self.get_terraform_output('ip')
        self.assertTrue(self.can_connect_to_port(instance_ip, 22))

    def test_events_present(self):
        print("\nFetching events", end='', flush=True)

        # workaround for https://github.com/boto/boto3/issues/454
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', ResourceWarning)

            events = self.get_flow_logs()

        print('')
        self.assertGreater(len(events), 0)

if __name__ == '__main__':
    unittest.main()
