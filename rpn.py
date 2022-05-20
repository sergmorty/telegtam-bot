from collections import deque
import operator
import math

class RPN():
    def __init__(self, s):
        self.data = self.converter(s)
        
    def _tokenizator(self, s):
        num = ''
        tokens = []
        for ch in s:
            if ch.isnumeric():
                num +=ch
            else:
                if num != '':
                    tokens.append(int(num))
                    num = ''
                if ch == '-' and (not tokens or tokens[-1] == '('):
                    num += ch
                elif ch in '()+-*/!^':
                    tokens.append(ch)
        if num != '':
            tokens.append(int(num))
        
        return tokens
    
    def converter(self, s):
        prior = {'-':1, '+':1, '*':2, '/':2, '^':3, '!':3, '(': -1}
        rpn = []
        stack = deque()
        for item in self._tokenizator(s):
            if type(item) == int or item == '!':
                rpn.append(item)
            elif item == '(':
                stack.append(item)
            elif item == ')':
                while stack[-1] != '(':
                    rpn.append(stack.pop())
                stack.pop()
            elif item in '-+*/^':
                while stack and prior[stack[-1]] >= prior[item]:
                    rpn.append(stack.pop())
                stack.append(item)
        while stack:
            rpn.append(stack.pop())
        return rpn
                
    def calc(self):
        stack = []
        oper = {'+':operator.add,
                '-':operator.sub,
                '*':operator.mul,
                '/':operator.truediv,
                '^':pow,
                '!':math.factorial
                    }
        for item in self.data:
            operand = []
            if isinstance(item, int) or isinstance(item, int):
                stack.append(item)
            else:
                count = 2
                if item in '!':
                    count = 1
                for _ in range(count):
                    operand.append(stack.pop())
                operand.reverse()
                stack.append(oper[item](*operand))
        return stack[-1]

if __name__ == '__main__':
    rpn = RPN('5!^2/4+3')
    print(rpn.calc())