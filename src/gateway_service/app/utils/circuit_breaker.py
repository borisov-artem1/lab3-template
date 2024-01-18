import requests
import time
from threading import Thread
from fastapi import status

from utils.settings import get_settings


class CircuitBreaker:
  gatewaySettings = get_settings()["services"]["gateway"]

  _fail_statistic = {}
  _service_state = {}
  _waiter: Thread = None

  @staticmethod
  def send_request(
      url: str, 
      http_method, 
      headers={}, 
      data={}, 
      params=None, 
      timeout=5
    ):
    resp = requests.Response()
    resp.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    if http_method is None:
      return resp

    host_url = url[url.find('://') + 3:]
    host_url = host_url[:host_url.find('/')]

    state = CircuitBreaker._service_state.get(host_url)
    if state == "unavailable":
      print(f"Service {host_url} is unavailable")
      return resp

    for _ in range(CircuitBreaker.gatewaySettings["max_num_of_fails"] + 1):
      try:
        resp = http_method(
          url=url, 
          headers=headers, 
          json=data, 
          params=params, 
          timeout=timeout
        )
        if resp.status_code < 500:
          CircuitBreaker._fail_statistic[host_url] = 0
          return resp
      except Exception:
        fail_num = CircuitBreaker._fail_statistic.get(host_url)
        if fail_num is None:
          CircuitBreaker._fail_statistic[host_url] = 1
        else:
          CircuitBreaker._fail_statistic[host_url] += 1

    fail_num = CircuitBreaker._fail_statistic.get(host_url)
    if fail_num is not None and \
      fail_num > CircuitBreaker.gatewaySettings["max_num_of_fails"]:
      print(f"The number fails for {host_url} is overflow")
      
      CircuitBreaker._fail_statistic[host_url] = 0
      CircuitBreaker._service_state[host_url] = "unavailable"
      if CircuitBreaker._waiter is None:
        CircuitBreaker._waiter = Thread(
          target=CircuitBreaker._wait_for_available
        )
        CircuitBreaker._waiter.start()

    return resp

  @staticmethod
  def _wait_for_available():
    is_end = False
    while not is_end:
      time.sleep(CircuitBreaker.gatewaySettings["timeout"])
      is_end = True
      for host_url in CircuitBreaker._service_state.keys():
        if CircuitBreaker._service_state[host_url] == "unavailable":
          Thread(
            target=CircuitBreaker._check_service_health, 
            args=(host_url,)
          ).start()
          is_end = False

    CircuitBreaker._waiter = None

  @staticmethod
  def _check_service_health(host_url: str):
    url = f"http://{host_url}/api/v1/manage/health"
    try:
      resp = requests.get(url, timeout=5)
      if resp.status_code == status.HTTP_200_OK:
        CircuitBreaker._service_state[host_url] = "available"
    except Exception:
      print("Error health:", url)
      