# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc



class DFMStub(object):
  """这是数据服务器Server为控制服务器Master提供的服务DFM的协议

  服务：
  请求：
  返回：
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """


class DFMServicer(object):
  """这是数据服务器Server为控制服务器Master提供的服务DFM的协议

  服务：
  请求：
  返回：
  """


def add_DFMServicer_to_server(servicer, server):
  rpc_method_handlers = {
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'DFM', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
