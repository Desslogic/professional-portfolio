import random
import math
import time
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class PumpJackState:
    # Operational Parameters
    runtime: float = 0.0
    spm: float = 0.0
    status: bool = False
    motor_amps: float = 0.0
    motor_temp: float = 0.0
    gearbox_temp: float = 0.0
    crank_angle: float = 0.0
    rod_load: float = 0.0
    production_rate: float = 0.0
    
    # Target/Setpoint Parameters
    target_spm: float = 6.0
    target_production: float = 100.0
    target_runtime: float = 23.0  # hours per day
    
    # Alarm States
    high_motor_amps: bool = False
    high_gearbox_temp: bool = False
    high_rod_load: bool = False
    low_production: bool = False
    
    # Performance Metrics
    availability: float = 0.0
    performance: float = 0.0
    quality: float = 0.0
    oee: float = 0.0

class PumpJackSimulator:
    def __init__(self):
        self.state = PumpJackState()
        self.time_step = 0
        
        # Operating limits
        self.LIMITS = {
            'motor_amps': {'min': 20, 'max': 45, 'alarm': 42},
            'motor_temp': {'min': 30, 'max': 80, 'normal': 60},
            'gearbox_temp': {'min': 25, 'max': 70, 'alarm': 65},
            'rod_load': {'min': 1000, 'max': 5000, 'alarm': 4500},
            'production_rate': {'min': 0, 'max': 150, 'low_alarm': 40}
        }
    
    def simulate_step(self) -> Dict[str, Any]:
        """Simulate one time step and return current state"""
        self.time_step += 1
        
        # Update operational parameters
        if self.state.status:
            # Simulate normal operation with some variation
            self.state.runtime += 1/3600  # Add one second in hours
            
            # SPM variation around target
            self.state.spm = self.state.target_spm + random.uniform(-0.2, 0.2)
            
            # Simulate crank angle
            self.state.crank_angle = (self.time_step * self.state.spm * 360/60) % 360
            
            # Motor amps varies with crank angle
            base_amps = (self.LIMITS['motor_amps']['max'] + self.LIMITS['motor_amps']['min']) / 2
            amp_variation = math.sin(math.radians(self.state.crank_angle)) * 5
            self.state.motor_amps = base_amps + amp_variation
            
            # Temperature gradual increase during operation
            self.state.motor_temp += random.uniform(0, 0.1)
            self.state.motor_temp = min(self.state.motor_temp, self.LIMITS['motor_temp']['max'])
            
            self.state.gearbox_temp += random.uniform(0, 0.05)
            self.state.gearbox_temp = min(self.state.gearbox_temp, self.LIMITS['gearbox_temp']['max'])
            
            # Rod load varies with crank angle
            base_load = (self.LIMITS['rod_load']['max'] + self.LIMITS['rod_load']['min']) / 2
            load_variation = math.sin(math.radians(self.state.crank_angle)) * 1000
            self.state.rod_load = base_load + load_variation
            
            # Production rate calculation
            self.state.production_rate = (self.state.spm / self.state.target_spm) * \
                                       self.state.target_production * \
                                       random.uniform(0.95, 1.05)
        
        # Update alarm states
        self.state.high_motor_amps = self.state.motor_amps > self.LIMITS['motor_amps']['alarm']
        self.state.high_gearbox_temp = self.state.gearbox_temp > self.LIMITS['gearbox_temp']['alarm']
        self.state.high_rod_load = self.state.rod_load > self.LIMITS['rod_load']['alarm']
        self.state.low_production = self.state.production_rate < self.LIMITS['production_rate']['low_alarm']
        
        # Calculate performance metrics
        if self.time_step % 3600 == 0:  # Update performance metrics every hour
            self.calculate_performance_metrics()
        
        return self.state.__dict__
    
    def calculate_performance_metrics(self):
        """Calculate OEE and related metrics"""
        # Availability = Actual Runtime / Planned Runtime
        self.state.availability = min(self.state.runtime / (self.time_step/3600), 1.0)
        
        # Performance = Actual Production / Target Production
        self.state.performance = self.state.production_rate / self.state.target_production
        
        # Quality = Good Production / Total Production (simplified)
        self.state.quality = 0.98 if not self.state.low_production else 0.85
        
        # Overall Equipment Effectiveness
        self.state.oee = self.state.availability * self.state.performance * self.state.quality
    
    def start(self):
        """Start the pump jack"""
        self.state.status = True
    
    def stop(self):
        """Stop the pump jack"""
        self.state.status = False
    
    def set_target(self, parameter: str, value: float):
        """Set target parameters"""
        if hasattr(self.state, f"target_{parameter}"):
            setattr(self.state, f"target_{parameter}", value)

if __name__ == "__main__":
    simulator = PumpJackSimulator()
    simulator.start()
    
    # Simulate for 10 steps
    for _ in range(10):
        state = simulator.simulate_step()
        print(f"Time: {simulator.time_step}s")
        print(f"SPM: {state['spm']:.2f}")
        print(f"Production Rate: {state['production_rate']:.2f}")
        print(f"Motor Amps: {state['motor_amps']:.2f}")
        print("-" * 50)
        time.sleep(1)