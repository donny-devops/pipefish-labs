import importlib.util
import io
import socket
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "serve_preview.py"
_SPEC = importlib.util.spec_from_file_location("serve_preview", _SCRIPT)
assert _SPEC is not None and _SPEC.loader is not None
serve_preview = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(serve_preview)


class TestQuietRequestHandler(unittest.TestCase):
    def test_log_message_does_not_write_request_path(self):
        handler = serve_preview.QuietRequestHandler.__new__(serve_preview.QuietRequestHandler)
        buf = io.StringIO()
        with redirect_stderr(buf):
            handler.log_message("%s - %s", "GET /secret?token=abc HTTP/1.1", "200")
        self.assertEqual(buf.getvalue(), "")
        self.assertNotIn("secret", buf.getvalue())
        self.assertNotIn("token", buf.getvalue())


class TestPortBound(unittest.TestCase):
    def test_port_bound_true_for_non_http_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("127.0.0.1", 0))
        sock.listen(1)
        port = sock.getsockname()[1]
        try:
            self.assertTrue(serve_preview.port_bound(port))
            self.assertFalse(serve_preview.is_ready(port))
        finally:
            sock.close()

    def test_port_bound_false_when_nothing_listens(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
        sock.close()
        self.assertFalse(serve_preview.port_bound(port))


class TestMain(unittest.TestCase):
    def test_main_uses_bind_aware_probe_host_for_collision(self):
        port = 43123
        with (
            patch.object(serve_preview, "ensure_dist"),
            patch.object(
                serve_preview.sys,
                "argv",
                ["serve_preview.py", "--foreground", "--bind", "127.0.0.2", "--port", str(port)],
            ),
            patch.object(serve_preview, "is_ready", return_value=False) as is_ready,
            patch.object(serve_preview, "port_bound", return_value=False) as port_bound,
            patch.object(
                serve_preview.http.server,
                "ThreadingHTTPServer",
                side_effect=OSError(serve_preview.errno.EADDRINUSE, "Address already in use"),
            ),
            patch.object(serve_preview, "wait_ready") as wait_ready,
        ):
            self.assertEqual(serve_preview.main(), 0)

        is_ready.assert_called_once_with(port, "127.0.0.2")
        port_bound.assert_called_once_with(port, "127.0.0.2")
        wait_ready.assert_called_once_with(port, "127.0.0.2")

    def test_main_maps_wildcard_bind_to_loopback_for_readiness_checks(self):
        port = 43124
        with (
            patch.object(serve_preview, "ensure_dist"),
            patch.object(serve_preview.sys, "argv", ["serve_preview.py", "--bind", "0.0.0.0", "--port", str(port)]),
            patch.object(serve_preview, "is_ready", return_value=False) as is_ready,
            patch.object(serve_preview, "port_bound", return_value=False) as port_bound,
            patch.object(serve_preview, "spawn_detached"),
            patch.object(serve_preview, "wait_ready") as wait_ready,
        ):
            self.assertEqual(serve_preview.main(), 0)

        is_ready.assert_called_once_with(port, "127.0.0.1")
        port_bound.assert_called_once_with(port, "127.0.0.1")
        wait_ready.assert_called_once_with(port, "127.0.0.1")

    def test_main_maps_ipv6_wildcard_bind_to_loopback_for_readiness_checks(self):
        port = 43125
        with (
            patch.object(serve_preview, "ensure_dist"),
            patch.object(serve_preview.sys, "argv", ["serve_preview.py", "--bind", "::", "--port", str(port)]),
            patch.object(serve_preview, "is_ready", return_value=False) as is_ready,
            patch.object(serve_preview, "port_bound", return_value=False) as port_bound,
            patch.object(serve_preview, "spawn_detached"),
            patch.object(serve_preview, "wait_ready") as wait_ready,
        ):
            self.assertEqual(serve_preview.main(), 0)

        is_ready.assert_called_once_with(port, "::1")
        port_bound.assert_called_once_with(port, "::1")
        wait_ready.assert_called_once_with(port, "::1")

    def test_main_waits_on_requested_bind_for_non_http_occupied_port(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("127.0.0.1", 0))
        sock.listen(1)
        port = sock.getsockname()[1]
        try:
            with (
                patch.object(serve_preview, "ensure_dist"),
                patch.object(
                    serve_preview.sys,
                    "argv",
                    ["serve_preview.py", "--bind", "127.0.0.1", "--port", str(port)],
                ),
                patch.object(serve_preview, "is_ready", return_value=False) as is_ready,
                patch.object(serve_preview, "wait_ready", side_effect=SystemExit("preview failed")) as wait_ready,
            ):
                with self.assertRaises(SystemExit):
                    serve_preview.main()

            is_ready.assert_called_once_with(port, "127.0.0.1")
            wait_ready.assert_called_once_with(port, "127.0.0.1")
        finally:
            sock.close()


if __name__ == "__main__":
    unittest.main()
