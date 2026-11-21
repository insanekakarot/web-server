import json
from threading import Lock

class Connections:
  def __init__(self):
    self.connections = set()
    self._connection_lock = Lock()

  def add_connection(self, *connections):
    """ Add new connection inside the set of connections using connection id;
    Use it for when adding new connection for performing actions or watching for it.
    """
    for connection in connections:
      if isinstance(connection, list) or isinstance(connection, set):
        for _conn in connection:
          if _conn in self.connections:
            return False
            
          self.connections.add(_conn)
          return True

      elif isinstance(connection, str):
        if connection in self.connections:
          return False
          
        self.connections.add(connection)
        return True

      else:
        raise ValueError("Values Should be in string, list, set with real values")


  def remove_connection(self, connection):
    """
    Remove the current using it's ID.
    """
    if isinstance(connection, str):
      if connection in self.connections:
        # print(connection, 'found')
        # print(connection, "Removing from Connections")
        self.connections.remove(connection)
        return True

      else:
        raise ValueError(f"There is no such a connection called {connection}")

    else:
      raise ValueError(f"Invalid Value! {connection}")
      


### Tests
# connections = Connections()
# domains = {"xyz.site", "abc.com"}
# connections.add_connection(domains)
# print(connections.connections)
# connections.remove_connection("abc.com")

# print(connections.connections)
