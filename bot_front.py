import kobukidriver as kobuki
import time

def main():    
    kobuki_instance = kobuki.Kobuki()
    while True:
        t1 = time.time()
        while(time.time()-t1<=8):
            kobuki_instance.move(255, 255, 0)
        kobuki_instance.move(0, 0, 0)
        t2 = time.time()
        while(time.time()-t2<=3):
            kobuki_instance.move(0, 255, 0)
        kobuki_instance.move(0, 0, 0)

main()