import pygame
import pytest
from project import check_borders, get_record, set_record, W, H

def test_check_borders_valid():
    pygame.init()
    field = [[0 for _ in range(W)] for _ in range(H)]
    figure = [pygame.Rect(5, 0, 1, 1), pygame.Rect(5, 1, 1, 1),
              pygame.Rect(6, 0, 1, 1), pygame.Rect(6, 1, 1, 1)]
    assert check_borders(figure, field) is True

def test_check_borders_collision():
    pygame.init()
    field = [[0 for _ in range(W)] for _ in range(H)]
    field[0][5] = (255, 0, 0)
    figure = [pygame.Rect(5, 0, 1, 1), pygame.Rect(5, 1, 1, 1),
              pygame.Rect(6, 0, 1, 1), pygame.Rect(6, 1, 1, 1)]
    assert check_borders(figure, field) is False

def test_get_record_creates_file(tmp_path):
    test_file = tmp_path / "record"
    assert get_record(test_file) == 0
    assert test_file.read_text() == "0"

def test_set_record_updates_high_score(tmp_path):
    test_file = tmp_path / "record"
    test_file.write_text("80")
    set_record(80, 120, test_file)
    assert test_file.read_text() == "120"
