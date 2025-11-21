"""Unit tests for the auraxium._backoff sub module."""

import itertools
import unittest
import typing
from collections.abc import Generator

import auraxium._backoff as backoff


class ExpoGeneratorTest(unittest.TestCase):
    """Test the exponential backoff generator."""

    def test_no_wait_on_first_yield(self) -> None:
        """Test that the first yield is always 0.0 (no wait)."""
        gen = backoff.expo(base=2, factor=1, max_value=10)
        first_wait = next(gen)
        self.assertEqual(first_wait, 0.0)

    def test_exponential_growth(self) -> None:
        """Test that the generator yields exponentially growing values."""
        gen = backoff.expo(base=2, factor=1, max_value=100)
        waits = [next(gen) for _ in range(7)]
        expected_waits = [0.0, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0]
        self.assertEqual(waits, expected_waits)

    def test_max_value_enforcement(self) -> None:
        """Test that the generator respects the max_value parameter."""
        gen = backoff.expo(base=2, factor=1, max_value=10)
        waits = [next(gen) for _ in range(10)]
        expected_waits = [
            0.0, 1.0, 2.0, 4.0, 8.0, 10.0, 10.0, 10.0, 10.0, 10.0]
        self.assertEqual(waits, expected_waits)

    def test_different_base_and_factor(self) -> None:
        """Test the generator with different base and factor values."""
        gen = backoff.expo(base=3, factor=0.5, max_value=20)
        waits = [next(gen) for _ in range(6)]
        expected_waits = [0.0, 0.5, 1.5, 4.5, 13.5, 20.0]
        self.assertEqual(waits, expected_waits)


class OnExceptionDecoratorTest(unittest.TestCase):
    """Test the on_exception decorator."""

    def test_bad_arguments(self) -> None:
        """Ensure that we get some errors if we put in bad arguments."""
        with self.assertRaises(TypeError):
            bad_gen = typing.cast(Generator[float, None, None], lambda: 0.0)
            _ = backoff.on_exception(bad_gen, (), max_tries=1)
        with self.assertRaises(ValueError):
            _ = backoff.on_exception(backoff.expo(2, 1), (), max_tries=-1)
        with self.assertRaises(TypeError):
            async def async_gen() -> typing.Any:
                yield 1.0
            _ = backoff.on_exception(async_gen(), (), max_tries=1)  # type: ignore

    def test_decorator_returns_callable(self) -> None:
        """Ensure that the decorator returns a callable."""
        decorator = backoff.on_exception(
            backoff.expo(2, 1), (Exception,), max_tries=3)

        def sample_function() -> None:
            pass

        decorated_function = decorator(sample_function)
        self.assertTrue(callable(decorated_function))

    def test_can_decorate_coroutine_function(self) -> None:
        """Ensure that we can decorate an async function."""
        decorator = backoff.on_exception(
            backoff.expo(2, 1), (Exception,), max_tries=3)

        async def sample_coroutine() -> None:
            pass

        _ = decorator(sample_coroutine)

    def test_handlers_success(self) -> None:
        """Test that on_success and on_backoff handlers are called."""
        handlers_called = {
            'success': False,
            'backoff': False,
        }

        def dummy_gen() -> Generator[float, None, None]:
            for _ in itertools.count():
                yield 0.0

        def on_backoff(details: backoff.Details) -> None:
            self.assertEqual(details['tries'], 1)
            handlers_called['backoff'] = True

        def on_success(details: backoff.Details) -> None:
            self.assertEqual(details['tries'], 2)
            handlers_called['success'] = True

        @backoff.on_exception(
            dummy_gen(), (ValueError,), max_tries=3,
            on_backoff=on_backoff, on_success=on_success)
        def flaky_function() -> None:
            if not handlers_called['backoff']:
                raise ValueError('Simulated failure')

        flaky_function()

        self.assertTrue(handlers_called['backoff'])
        self.assertTrue(handlers_called['success'])

    def test_handlers_giveup(self) -> None:
        """Test that on_giveup handler is called for async functions."""
        handlers_called = {
            'backoff': False,
            'giveup': False,
        }

        def dummy_gen() -> Generator[float, None, None]:
            for _ in itertools.count():
                yield 0.01

        def on_backoff(details: backoff.Details) -> None:
            _ = details
            handlers_called['backoff'] = True

        def on_giveup(details: backoff.Details) -> None:
            self.assertEqual(details['tries'], 3)
            self.assertGreater(details['elapsed'], 0.01)
            handlers_called['giveup'] = True

        @backoff.on_exception(
            dummy_gen(), (ValueError,), max_tries=2,
            on_backoff=on_backoff, on_giveup=on_giveup)
        def always_failing_function() -> None:
            raise ValueError('Simulated failure')

        with self.assertRaises(ValueError):
            always_failing_function()
        self.assertTrue(handlers_called['backoff'])
        self.assertTrue(handlers_called['giveup'])
