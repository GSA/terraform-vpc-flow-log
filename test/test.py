import boto3
import subprocess
import unittest
import urllib

class TestStringMethods(unittest.TestCase):

    def get_terraform_output(self, name):
        result = subprocess.run(['terraform', 'output', name], stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8').strip()

    def get_log_group(self):
        return self.get_terraform_output('log_group_name')

    def get_flow_logs(self):
        client = boto3.client('logs')

        log_group = self.get_log_group()
        ip = self.get_my_ip()

        # hitting https://github.com/boto/boto3/issues/454
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

    def test_logs_present(self):
        events = self.get_flow_logs()
        self.assertGreater(len(events), 0)

if __name__ == '__main__':
    unittest.main()
