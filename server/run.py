from core import select_server,pan_handler

server = select_server.SelectServer()
server.run(pan_handler.PanHandler)