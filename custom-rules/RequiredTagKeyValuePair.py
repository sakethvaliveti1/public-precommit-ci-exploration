from cfnlint.rules import CloudFormationLintRule
from cfnlint.rules import RuleMatch


required_tags_and_values = {
    "environment": ["dev", "uat", "prod"],
    "service": ["hello", "bye", "whatsup"],
    "resource": ["api", "compute", "storage"],
    "newtag": ["monday", "tuesday", "wednesday"]
}


class PropertiesTagsRequired(CloudFormationLintRule):
    """Check if Tags have required keys and values"""
    id = 'E9001'
    shortdesc = 'Required Tags exist and some have specific allowed values'
    description = 'Check if required Tags exist and validate values'
    tags = ['resources', 'tags']

    def match(self, cfn):
        """Check if required Tags exist and validate values"""

        matches = []

        required_tags = [key for key in required_tags_and_values]
        
        all_tags = cfn.search_deep_keys('Tags')
        all_tags = [x for x in all_tags if x[0] == 'Resources']
        for all_tag in all_tags:
            all_keys = [d.get('Key') for d in all_tag[-1]]
            all_values = [d.get('Value') for d in all_tag[-1]]
            dict_key_value = dict(zip(all_keys,all_values))
            for required_tag in required_tags:
                if required_tag not in all_keys:
                    message = '''Missing required tag " {0} " at {1}'''
                    matches.append(
                        RuleMatch(
                            all_tag[:-1],
                            message.format(required_tag, '/'.join(map(str, all_tag[:-1])))))
                if required_tag in dict_key_value:
                    require_tag_allowed_values = required_tags_and_values[required_tag]
                    if dict_key_value[required_tag] not in require_tag_allowed_values:
                        message = "Tag {0} does not have allowed values assigned at {1}. \n The allowed values for this tag are: {2} \n"
                        matches.append(
                            RuleMatch(
                                all_tag[:-1],
                                message.format(required_tag, '/'.join(map(str, all_tag[:-1])), ','.join(require_tag_allowed_values))))

        return matches
    
