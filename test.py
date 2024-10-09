class Animal:
    def speak(self, line):
        return line

    def poo(self, line):
        return line



a = Animal()


poo = (getattr(a, 'speak'))

print(poo("Hello"))