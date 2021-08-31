class CPF:
    def __init__(self, cpf):
        self.is_valid = False

        self.validation(
            cpf.replace('.', '').replace('-', ''),
            self.somatory,
            self.verify
        )

    def somatory(self, digits, multiplier):
        somatory = 0
        
        for digit in digits:
            somatory += int(digit) * multiplier
            multiplier -= 1

        return somatory

    def validation(self, cpf, somatory, verify):
        if not verify(somatory(cpf[:-2], 10), int(cpf[-2])): return
        if not verify(somatory(cpf[:-1], 11), int(cpf[-1])): return

        self.is_valid = True

    def verify(self, somatory, digit):
        rest = somatory % 11

        if rest < 2:
            if digit != 0: return False

        else:
            if digit != 11 - rest: return False

        return True