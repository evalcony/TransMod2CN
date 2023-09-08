import main
import utils

if __name__ == '__main__':
    line = "Wilson, I want to know why we're here. I never let anyone use some... bearomancy on me, taking the group away from Sendai and her enclave!"
    res = main.Solver(mode='debug').solve(line)
    print(res)