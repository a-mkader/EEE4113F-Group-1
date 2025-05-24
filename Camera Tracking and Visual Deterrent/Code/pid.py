# pid.py
class PID:
    def __init__(self, Kp=1.0, Ki=0.0, Kd=0.0, output_limits=(0, 180)):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.min_output, self.max_output = output_limits

        self.integral = 0
        self.prev_error = 0
        self.prev_time = None

    def compute(self, error, current_time):
        if self.prev_time is None:
            self.prev_time = current_time
            return 0

        dt = current_time - self.prev_time
        self.prev_time = current_time

        if dt <= 0.0:
            return 0

        # PID terms
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        self.prev_error = error

        output = (self.Kp * error) + (self.Ki * self.integral) + (self.Kd * derivative)

        # Clamp output to limits with anti-windup
        if output > self.max_output:
            output = self.max_output
            # Undo last integral addition to prevent windup
            self.integral -= error * dt
        elif output < self.min_output:
            output = self.min_output
            self.integral -= error * dt

        return output

