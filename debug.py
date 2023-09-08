import main
import utils

if __name__ == '__main__':
    # line = "Wilson, I want to know why we're here. I never let anyone use some... bearomancy on me, taking the group away from Sendai and her enclave!"
    line = 'Snort, snort.［2］.'

    # 如果设置mode='debug'，则不会调用API，而且也会打印更详细的信息，而且不会有time.wait()
    res = main.Solver(mode='').solve(line)
    print(res)