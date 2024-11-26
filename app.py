import json
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')
import json

# Global menu with item prices
MENU = {
    "Chicken Sandwich": 5.99,
    "Fries": 2.49,
    "Burger": 6.99,
    "Soda": 1.99,
    "Salad": 4.99,
    "Pizza": 8.99,
    "Pasta": 7.49,
    "Ice Cream": 3.49,
    "Coffee": 2.99,
    "Tea": 2.49
}

PROMPT_TEMPLATE = """
You are an assistant for a chat-based food ordering system. Your job is to extract ordered food items and their quantities from customer input.

**Rules:**
1. The menu is as follows:
   - Chicken Sandwich: $5.99
   - Fries: $2.49
   - Burger: $6.99
   - Soda: $1.99
   - Salad: $4.99
   - Pizza: $8.99
   - Pasta: $7.49
   - Ice Cream: $3.49
   - Coffee: $2.99
   - Tea: $2.49

2. Respond in the following JSON format:
   {{
       "items_in_menu": [
           {{"name": "Chicken Sandwich", "quantity": 2}},
           {{"name": "Fries", "quantity": 1}}
       ],
       "items_not_in_menu": [
           {{"name": "Steak", "quantity": 1}}
       ]
   }}

3. Rules for mapping items:
   - Include items explicitly mentioned in the menu under the `items_in_menu` key.
   - Any item mentioned that is not in the menu must go under the `items_not_in_menu` key with its quantity.
   - Default the quantity to 1 if the user does not specify it.
   - For plural forms of menu items (e.g., "sandwiches" instead of "sandwich"), match the singular version in the menu.

4. Quantities:
   - If the user specifies vague terms like "a" or "an," map it to `quantity: 1`.
   - Quantities must always be integers.

5. Error Handling:
   - If no recognizable menu items or non-menu items are mentioned in the input, return:
     {{
         "items_in_menu": [],
         "items_not_in_menu": []
     }}

6. Always ensure:
   - Items in the `items_in_menu` must strictly match the menu.
   - Items in the `items_not_in_menu` must not be part of the menu.

**Customer Input:** "{user_input}"
"""

# Preprocess input to normalize numbers
def preprocess_input(user_input):
    words_to_numbers = {
        "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8,
        "nine": 9, "ten": 10, "a": 1, "an": 1
    }
    for word, num in words_to_numbers.items():
        user_input = user_input.replace(f" {word} ", f" {num} ")
    return user_input

# Mock LLM response function
def get_order_details(user_input):
    preprocessed_input = preprocess_input(user_input)
    prompt = PROMPT_TEMPLATE.format(user_input=preprocessed_input)

    try:
        response = model.generate_content(prompt)  # Replace this with your LLM call
        response_json = json.loads(response.text.strip())
        return response_json
    except json.JSONDecodeError:
        print("Error decoding JSON from LLM response.")
        return {"items_in_menu": [], "items_not_in_menu": []}
    except Exception as e:
        print("Unexpected error:", e)
        return {"items_in_menu": [], "items_not_in_menu": []}

# Calculate total cost and invoice
def calculate_invoice(order_details):
    total_cost = 0
    invoice = []

    for item in order_details["items_in_menu"]:
        name = item["name"].strip()
        quantity = item["quantity"]
        if name in MENU:
            price = MENU[name]
            cost = quantity * price
            invoice.append({"name": name, "quantity": quantity, "price_per_item": price, "total": cost})
            total_cost += cost

    return {"invoice": invoice, "total_cost": round(total_cost, 2)}

# Main function
def main():
    print("Welcome to the chat-based food ordering system!")
    print("Menu:")
    for item, price in MENU.items():
        print(f"{item}: ${price}")

    print("\nEnter your order (type 'done' to finish):")
    user_input = ""
    while True:
        line = input("> ")
        if line.lower() == "done":
            break
        user_input += line + " "

    order_details = get_order_details(user_input)
    if order_details["items_in_menu"]:
        invoice = calculate_invoice(order_details)
        print("Invoice Details:")
        for item in invoice["invoice"]:
            print(f"{item['quantity']}x {item['name']} @ ${item['price_per_item']}: ${item['total']}")
        print(f"Total Cost: ${invoice['total_cost']}")
    else:
        print("No valid items ordered from the menu.")

if __name__ == "__main__":
    main()

