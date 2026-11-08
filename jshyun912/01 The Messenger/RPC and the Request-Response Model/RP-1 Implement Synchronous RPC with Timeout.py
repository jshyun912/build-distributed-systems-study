#!/usr/bin/env python3
import sys
import json
import threading

class Node:
    def __init__(self):
        self.node_id = None
        self.node_ids = []
        self.next_msg_id = 0
        self.lock = threading.Lock()
        self.pending = {}  # msg_id -> threading.Event
        self.replies = {}  # msg_id -> reply body

    def send(self, dest, body):
        with self.lock:
            body["msg_id"] = self.next_msg_id
            msg_id = self.next_msg_id
            self.next_msg_id += 1
        message = {"src": self.node_id, "dest": dest, "body": body}
        print(json.dumps(message), flush=True)
        return msg_id

    def reply(self, request, body):
        body["in_reply_to"] = request["body"]["msg_id"]
        self.send(request["src"], body)

    def send_rpc(self, dest, body):
        msg_id = self.send(dest, body)
        self.pending[msg_id] = threading.Event()
        self.replies[msg_id] = {
            "type": "error",
            "code": 0,
        }

        return msg_id

    def wait_reply(self, msg_id, timeout=1.0):
        event:threading.Event = self.pending[msg_id]

        if not event.wait(timeout):
            body = []

        else: body = []

        self.send()

    def handle_reply(self, body):
        msg_id = body.get("in_reply_to")


        self.handle_reply[msg_id]


        pass

def main():
    node = Node()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        message = json.loads(line)
        body = message["body"]
        msg_type = body["type"]

        if msg_type == "init":
            node.node_id = body["node_id"]
            node.node_ids = body["node_ids"]
            node.reply(message, {"type": "init_ok"})
        elif msg_type == "echo":
            node.reply(message, {"type": "echo_ok", "echo": body["echo"]})
        elif msg_type == "proxy":
            msg_id = node.send_rpc(message["target"], message["inner"])
            threading.Thread(target=node.wait_reply, args=(msg_id, ))
        else:
            node.handle_reply(body)

if __name__ == "__main__":
    main()
