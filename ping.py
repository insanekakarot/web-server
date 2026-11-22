from logging import log
import subprocess
import time
import re


class Patterns:
  delay_pttrn = r"(?=time=(\d+ ms))"
  icmp_pttrn = r"(?=icmp_seq=(\d+))"
  ttl_pttrn = r"(?=ttl=(\d+))"

  transmitted_pttrn = r"(?=(\d+)\spackets\stransmitted)"
  loss_pttrn = r"(?=(\d+)(%)\spacket\sloss)"
  receive_pttrn = r"(?=(\d+)\sreceived)"


class Ping:
  global Patterns
  def __init__(self):
    self.patterns = Patterns

  def _parse_output(self, output, logs=True):
    # start = time.perf_counter()
    for line in output.splitlines():
      d_p = re.search(self.patterns.delay_pttrn, line)
      icmp_p = re.search(self.patterns.icmp_pttrn, line)
      ttl_p = re.search(self.patterns.ttl_pttrn, line)
      trs_p = re.search(self.patterns.transmitted_pttrn, line)
      los_p = re.search(self.patterns.loss_pttrn, line)
      recv_p = re.search(self.patterns.receive_pttrn, line)

      if d_p:
        if logs:
          log(f"Delay:                 {d_p.group(1)}")
        dp = d_p.group(1)

      if icmp_p:
        if logs:
          log(f"ICMP_SEQ:              {icmp_p.group(1)}")
        icmp = icmp_p.group(1)

      if ttl_p:
        if logs:
          log(f"TTL Time:              {ttl_p.group(1)}")
        ttl = ttl_p.group(1)

      if trs_p:
        if logs:
          log(f"Packets Transmitted:   {trs_p.group(1)}")
        transmitted_packets = trs_p.group(1)

      if los_p:
        if logs:
          log(f"Packets lost:          {los_p.group(1)}")
        loss_packets = los_p.group(1)

      if recv_p:
        if logs:
          log(f"Packets Recieved:      {recv_p.group(1)}")
        received_packets = recv_p.group(1)

      
    ping_result = {
        "delay": dp,
        "icmp": icmp,
        "ttl": ttl,
        "transmitted_packets": transmitted_packets,
        "packets_loss": loss_packets,
        "packets_received": received_packets
      }

    # end = time.perf_counter() - start
    # print(f"{round(end, 5)} seconds")

    return ping_result


  def _ping_address(self, address, counts, timeout, attempts: int = 3, retries_interval: int = 5):
    # print(address)
    cmd = ["ping", "-c", str(counts), address]
    log(f"Checking Connection to '{address}'")
    # print(cmd)
    _connection_established = False
    _continue_loop = True
    _attempts = 1
    while not _connection_established and _continue_loop:
      log(f"No. Of Attempts: {_attempts}")
      if _attempts > attempts:
        _continue_loop = False
        return False

      try:
        exec_output = subprocess.run(cmd, timeout=timeout, capture_output=True, text=True)
        ping_result = self._parse_output(exec_output.stdout, logs=False)

        print(ping_result)

        delay = ping_result.get("delay")
        packets_received = ping_result.get("packets_received")
        packets_transmitted = ping_result.get("transmitted_packets")
        packets_lost = ping_result.get("packets_loss")
        delay = str(delay).replace(" ms", "")
        
        if int(delay) < 1000 and packets_received == packets_transmitted:
          _connection_established = True
          _continue_loop = True

          log(f"Connection Established to '{address}'")
          return True

        elif not packets_received == packets_transmitted:
          log(f"{packets_lost}% Packets got lost!")
          if packets_lost >= 50:
            return True

          else:
            return False

        _attempts += 1

      except subprocess.TimeoutExpired:
        log("Timeout")
        if _attempts < attempts:
          log(f"Waiting {retries_interval} Seconds Before retrying...")  
          time.sleep(retries_interval)
        
        if _attempts >= attempts:
          return False

        _attempts += 1
        
  def check_ping(self, address, counts: int = 4, timeout: int = 10):
    is_connection_stable = self._ping_address(address, counts, timeout)
    if is_connection_stable:
      log("Connection Stable, we can continue next process!")

    else:
      log(f"Please Contact your Internet Service Provider!")


# Tests
# ping = Ping()
# ping.check_ping("<address>")
