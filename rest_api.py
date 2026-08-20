import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

notes = []
next_id = 1


def find_note(note_id):
    for note in notes:
        if note["id"] == note_id:
            return note
    return None


class NotesRequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        raw_body = self.rfile.read(length)
        return json.loads(raw_body)

    def _parse_path(self):
        path = urlparse(self.path).path
        parts = [part for part in path.split("/") if part]
        return parts

    def do_GET(self):
        parts = self._parse_path()

        if parts == ["notes"]:
            self._send_json(200, notes)
            return

        if len(parts) == 2 and parts[0] == "notes":
            note = find_note(self._to_id(parts[1]))
            if note is None:
                self._send_json(404, {"error": "Note not found"})
                return
            self._send_json(200, note)
            return

        self._send_json(404, {"error": "Not found"})

    def do_POST(self):
        global next_id
        parts = self._parse_path()

        if parts != ["notes"]:
            self._send_json(404, {"error": "Not found"})
            return

        try:
            data = self._read_json_body()
        except json.JSONDecodeError:
            self._send_json(400, {"error": "Invalid JSON"})
            return

        title = data.get("title")
        content = data.get("content", "")
        if not title:
            self._send_json(400, {"error": "'title' is required"})
            return

        note = {"id": next_id, "title": title, "content": content}
        notes.append(note)
        next_id += 1
        self._send_json(201, note)

    def do_PUT(self):
        parts = self._parse_path()

        if len(parts) != 2 or parts[0] != "notes":
            self._send_json(404, {"error": "Not found"})
            return

        note = find_note(self._to_id(parts[1]))
        if note is None:
            self._send_json(404, {"error": "Note not found"})
            return

        try:
            data = self._read_json_body()
        except json.JSONDecodeError:
            self._send_json(400, {"error": "Invalid JSON"})
            return

        if "title" in data:
            note["title"] = data["title"]
        if "content" in data:
            note["content"] = data["content"]

        self._send_json(200, note)

    def do_DELETE(self):
        parts = self._parse_path()

        if len(parts) != 2 or parts[0] != "notes":
            self._send_json(404, {"error": "Not found"})
            return

        note = find_note(self._to_id(parts[1]))
        if note is None:
            self._send_json(404, {"error": "Note not found"})
            return

        notes.remove(note)
        self._send_json(200, {"message": "Note deleted"})

    def _to_id(self, raw_id):
        try:
            return int(raw_id)
        except ValueError:
            return -1

    def log_message(self, format, *args):
        pass


def run_server(host="localhost", port=8000):
    server = HTTPServer((host, port), NotesRequestHandler)
    print(f"Notes REST API running at http://{host}:{port}")
    print("Endpoints:")
    print("  GET    /notes")
    print("  GET    /notes/<id>")
    print("  POST   /notes")
    print("  PUT    /notes/<id>")
    print("  DELETE /notes/<id>")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown()


if __name__ == "__main__":
    run_server()
