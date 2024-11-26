# Chat-Based Food Ordering System

This project is a command-line-based food ordering system that uses a language model (LLM) to parse user input and generate an order summary. The application features a menu, extracts food items and their quantities from user input, calculates the total cost, and generates an invoice.

---

## Features

- **Dynamic User Input Parsing**: Accepts natural language input to specify food items and their quantities.
- **Menu Validation**: Differentiates between items on the menu and those that are not.
- **Invoice Generation**: Calculates the total cost and provides an itemized invoice.
- **Preprocessing**: Converts textual numbers (e.g., "two") into numeric values.

---

## Requirements

- Python 3.8 or later
- Google Generative AI SDK
- API Key for Google Generative AI (`GOOGLE_API_KEY`)

