#!/usr/bin/env python3

"""
bingo_cards.py
Rishith Kilaru '26
now maintained by D Evangelista '94.

inputs:
entries.txt is a textfile with each square text on a line

outputs:
bingo_cards.pdf is an 8.5x11" letter pdf with 2 bingo cards per sheet
"""

__version__ = "2026.06.25"

import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER

# Rishith hard coded the inputs instead of using argparse :(
input_list = "entries.txt" # file with input square text
output_pdf = "bingo_cards.pdf" # ofile pdf 
card_count = 200 # how many cards to generate; this covers all S&E
size = 5
board_count = 2 # 2up per page






def load_entries(filename):
    """
    load_entries(filename) reads the textfile and splits it into lines
    returning a list of strings
    """
    with open(filename, "r", encoding="utf-8") as f:
        entries = [line.strip() for line in f if line.strip()]
    return entries

def generate_card(entries):
    """
    generate_card(entries) makes a bingo card by randomly picking
    from the entries
    """
    picks = random.sample(entries, 24)
    card = [["" for _ in range(size)] for _ in range(size)]

    idx = 0
    for r in range(size):
        for c in range(size):
            if r ==2 and c ==2:
                card[r][c] = "FREE"
            else:
                card[r][c] = picks[idx]
                idx += 1
    return card




def draw_wrapped_text(c, text, element, response, width, height, is_free=False):
    """
    for generating each square
    """
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.alignment = TA_CENTER
    style.fontName = "Helvetica-Bold" if is_free else "Helvetica"
    style.fontSize = 10 if is_free else 8
    style.leading = style.fontSize + 1

    p = Paragraph(text, style)
    w, h = p.wrap(width - 6, height - 6)

    p.drawOn(c, element + (width - w) / 2, response + (height - h) / 2)

def draw_card(c, card, card_number, origin_y):
    """
    for generating a card
    """
    page_width, page_height = letter

    margin_x = 0.75 * inch
    margin_y = 0.5 * inch

    available_height = (page_height - 2 * margin_y) / board_count
    title_height = 0.35 * inch

    grid_size_px = min(page_width - 2 * margin_x, available_height - title_height - 0.25 * inch)

    cell_size = grid_size_px / size

    start_x = (page_width - grid_size_px) / 2
    start_y = origin_y + available_height - title_height - cell_size

    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(page_width / 2, origin_y + available_height - 0.25 * inch, "S&E Project Presentations Bingo")

    for r in range(size):
        for col in range(size):
            element = start_x + col * cell_size
            response = start_y - r * cell_size

            c.rect(element, response, cell_size, cell_size)

            text = card[r][col]
            draw_wrapped_text(
                c,
                text,
                element,
                response,
                cell_size,
                cell_size,
                is_free=(text =="FREE")
            )






if __name__ == "__main__":

    print("S&E Senior Project Bingo Card Generator, {0}".format(__version__))
    print("Rishith Chandra Kilaru '26\n")
    print("Generating {0} bingo cards".format(card_count))

    # load entries from textfile
    entries = load_entries(input_list)

    # create canvas to draw pdf
    c = canvas.Canvas(output_pdf, pagesize=letter)

    # set dimensions
    height = letter[1]
    card_height = (height - 2 * 0.5 * inch) / board_count

    for pos in range(card_count):
        position_on_page = pos % board_count
        origin_y = height - 0.5 * inch - (position_on_page + 1) * card_height

        card = generate_card(entries)
        draw_card(c, card, pos + 1, origin_y)

        if position_on_page ==board_count - 1:
            c.showPage()

    c.save()
    print("output written to {0}".format(output_pdf))
    print("done")
