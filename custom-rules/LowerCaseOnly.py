from cfnlint.rules import CloudFormationLintRule
from cfnlint.rules import RuleMatch
import re


class TagValueValidation(CloudFormationLintRule):
    """Check if specifc Tags are using allowed values"""
    id = 'E9002'
    shortdesc = 'Check if specifc Tags are using allowed values'
    description = 'Check if specifc Tags are using allowed values'
    tags = ['resources', 'tags']

    def match(self, cfn):
        """Check if specifc Tags are using allowed values"""

        matches = []

        all_tags = cfn.search_deep_keys('Tags')
        all_tags = [x for x in all_tags if x[0] == 'Resources']
        for resource_and_its_tags in all_tags:
            #print(resource_and_its_tags)
            all_keys = [d.get('Key') for d in resource_and_its_tags[-1]]
            all_values = [d.get('Value') for d in resource_and_its_tags[-1]]
            key_value_pairs = list(zip(all_keys,all_values))
            regex = "^[0-9a-z-]+$"
            for pair in key_value_pairs:
                key_in_lowercase = re.match(regex, pair[0])
                value_in_lowercase = re.match(regex, pair[1])
                if not key_in_lowercase:
                    message = '''Tag key name should be all lower case and only dashes allowed. Provided value: {0} at {1}'''
                    matches.append(
                        RuleMatch(
                            resource_and_its_tags[:-1],
                            message.format(pair[0], '/'.join(map(str, resource_and_its_tags[:-1])))))
                if not value_in_lowercase:
                    message = '''Value assigned to tag {0} should be all lower case and only dashes allowed. Provided value: {1} at {2}'''
                    matches.append(
                        RuleMatch(
                            resource_and_its_tags[:-1],
                            message.format(pair[0], pair[1], '/'.join(map(str, resource_and_its_tags[:-1])))))

        return matches

