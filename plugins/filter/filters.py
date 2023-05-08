
class FilterModule(object):

    def filters(self):
        return {
            'extra_chains': self.return_user_defined_chains,
        }

    def return_user_defined_chains(self, output: list) -> list:
        std = ['INPUT', 'OUTPUT', 'FORWARD']
        return [l.split(' ')[1] for l in output if l.split(' ')[1] not in std]
