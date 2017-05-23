import random
 
class Spinner:
    @staticmethod
    def spin(content):

        start = content.find('{')
        end = content.find('}')
        if start == -1 and end == -1:
            return content
        elif start == -1:
            return content
        elif end == -1:
            raise "unbalanced brace"
        elif end < start:
            return content
        elif start < end:
            rest = Spinner.spin(content[start+1:])
            end = rest.find('}')
            if end == -1:
                raise "unbalanced brace"
            return content[:start] + random.choice(rest[:end].split('|')) + Spinner.spin(rest[end+1:])

