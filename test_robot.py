import pytest

from robot import Robot, Direction, IllegalMoveException


@pytest.fixture
def robot():
    return Robot()


def test_constructor(robot):
    state = robot.state()

    assert state['direction'] == Direction.NORTH
    assert state['row'] == 10
    assert state['col'] == 1


# turns


def test_east_turn(robot):
    robot.turn()

    state = robot.state()
    assert state['direction'] == Direction.EAST


def test_south_turn(robot):
    for _ in range(2): robot.turn()

    state = robot.state()
    assert state['direction'] == Direction.SOUTH


def test_west_turn(robot):
    for _ in range(3): robot.turn()

    state = robot.state()
    assert state['direction'] == Direction.WEST


def test_north_turn(robot):
    for _ in range(4): robot.turn()

    state = robot.state()
    assert state['direction'] == Direction.NORTH


# illegal moves


def test_illegal_move_north(robot):
    for _ in range(9): robot.move()

    with pytest.raises(IllegalMoveException):
        robot.move()


def test_illegal_move_east(robot):
    robot.turn()

    for _ in range(9): robot.move()

    with pytest.raises(IllegalMoveException):
        robot.move()


def test_illegal_move_south(robot):
    for _ in range(2): robot.turn()

    with pytest.raises(IllegalMoveException):
        robot.move()


def test_illegal_move_west(robot):
    for _ in range(3): robot.turn()

    with pytest.raises(IllegalMoveException):
        robot.move()


# moves


def test_move_north(robot):
    robot.move()
    state = robot.state()
    assert state['row'] == 9
    assert state['col'] == 1


def test_move_east(robot):
    robot.turn()
    robot.move()
    state = robot.state()
    assert state['row'] == 10
    assert state['col'] == 2


def test_move_south(robot):
    # move north first to avoid illegal move
    robot.move()

    for _ in range(2): robot.turn()
    robot.move()
    state = robot.state()
    assert state['row'] == 10
    assert state['col'] == 1


def test_move_west(robot):
    # move east first to avoid illegal move
    robot.turn()
    robot.move()

    for _ in range(2): robot.turn()
    robot.move()
    state = robot.state()
    assert state['row'] == 10
    assert state['col'] == 1


# backtracking


def test_back_track_without_history(robot):
    robot.back_track()
    state = robot.state()
    assert state['direction'] == Direction.NORTH
    assert state['row'] == 10
    assert state['col'] == 1


def test_back_track_move(robot):
    initial_state = robot.state()

    robot.move()
    robot.back_track()

    assert robot.state() == initial_state


def test_back_track_turn(robot):
    initial_state = robot.state()

    robot.turn()
    robot.back_track()

    assert robot.state() == initial_state


def test_back_track_multiple_moves(robot):
    robot.move()
    robot.move()
    robot.move()
    robot.turn()
    robot.move()
    robot.turn()
    robot.move()
    robot.move()

    prev_state = robot.state()

    robot.turn()

    robot.back_track()

    assert robot.state() == prev_state


def test_back_track_all_moves(robot):
    initial_state = robot.state()

    actions = (
        robot.move,
        robot.turn,
        robot.move,
        robot.move,
        robot.turn,
        robot.move,
        robot.turn
    )

    for action in actions:
        action()

    for _ in range(len(actions)):
        robot.back_track()

    assert robot.state() == initial_state

