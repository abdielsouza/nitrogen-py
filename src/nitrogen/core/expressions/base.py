from typing import Set

class Expression:
    def dependencies(self) -> Set[str]:
        return set()
    
    def compile(self, backend):
        raise NotImplementedError()