from simulation import Simulation
from threading import Thread

def main():
    sim = Simulation()
    
    sim_thread = Thread(target=sim.start_simulation, daemon=True)
    input_thread = Thread(target=sim.input_listener, daemon=True)
    
    sim_thread.start()
    input_thread.start()
    
    sim_thread.join()
    input_thread.join()
    print("Программа завершена.")

if __name__ == "__main__":
    main()