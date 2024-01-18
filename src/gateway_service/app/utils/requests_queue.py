import time
from threading import Thread
from datetime import datetime

from utils.settings import get_settings


class Request:
  def __init__(self, url, http_method, headers, data, timeout):
    self.url = url
    self.http_method = http_method
    self.headers = headers
    self.data = data
    self.timeout = timeout


class RequestQueue:
  gatewaySettings = get_settings()["services"]["gateway"]

  _req_queue: dict[str, Request] = {}
  _req_sender: Thread = None

  @staticmethod
  def add_http_request(
      url: str, 
      http_method, 
      headers={}, 
      data={},
      timeout=5
    ):

    RequestQueue._req_queue[url + http_method.__name__ + str(datetime.now())] = Request(
      url=url,
      http_method=http_method, 
      headers=headers,
      data=data, 
      timeout=timeout
    )
    if RequestQueue._req_sender is None:
      RequestQueue._req_sender = Thread(
        target=RequestQueue._req_sending
      )
      RequestQueue._req_sender.start()

  @staticmethod
  def _req_sending():
    while len(RequestQueue._req_queue.keys()) > 0:
      for req_key in RequestQueue._req_queue.keys():
        Thread(
          target=RequestQueue._req_send, 
          args=(req_key,)
        ).start()
      time.sleep(RequestQueue.gatewaySettings["timeout"])

    RequestQueue._req_sender = None

  @staticmethod
  def _req_send(key: str):
    req = RequestQueue._req_queue.get(key)
    if req is None:
      return

    try:
      resp = req.http_method(
        url=req.url,
        headers=req.headers,
        json=req.data,
        timeout=req.timeout
      )
      if resp.status_code < 500:
        del RequestQueue._req_queue[key]
    except Exception:
      print(f"Error {req.http_method.__name__}:", req.url)
