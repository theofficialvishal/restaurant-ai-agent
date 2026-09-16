import re
import random
from datetime import datetime, timezone
from typing import Optional, Literal
from pydantic import BaseModel, Field
from backend.graph.state import RestaurantState
from backend.app.menu import menu_repo
from backend.app.config import GROQ_API_KEY, GEMINI_API_KEY, LLM_MODEL



class OrderItem(BaseModel):
    dish_name: str = Field(
        description="The Indian dish requested (e.g. Butter Chicken, Paneer Tikka, Biryani, Dal Makhani, Garlic Naan, Gulab Jamun)."
    )
    quantity: int = Field(
        default=1,
        description="The requested quantity of the dish. Default to 1 if not specified."
    )

class ExtractedOrder(BaseModel):
    intent: Literal["ORDER", "INQUIRY", "OFF_TOPIC", "GREETING", "FINALIZE", "REQUEST_BILL"] = Field(
        default="ORDER",
        description="The user's intent. ORDER if ordering food, INQUIRY if asking about menu or prices, GREETING if saying hello or namaste, OFF_TOPIC if unrelated to food or restaurant, FINALIZE if user wants to cook the order, REQUEST_BILL if user wants the bill."
    )
    items: list[OrderItem] = Field(
        default_factory=list,
        description="List of dishes ordered with their quantities."
    )


def rule_based_extract(user_input: str) -> ExtractedOrder:
    """Deterministic fallback parser for testing and offline environments."""
    raw_text = user_input.strip().lower()
    # Normalize punctuation to spaces
    clean_text = re.sub(r'[^\w\s]', ' ', raw_text)
    clean_text = " ".join(clean_text.split())

    # Greetings
    greetings = ["hi", "hello", "hey", "namaste", "namaskar", "good morning", "good evening"]
    if any(clean_text == g or clean_text.startswith(g + " ") for g in greetings):
        return ExtractedOrder(intent="GREETING", items=[])

    # Inquiries
    inquiry_keywords = ["menu", "what do you have", "what's available", "kya milega", "options", "price", "rate"]
    if any(kw in clean_text for kw in inquiry_keywords) and not any(dish in clean_text for dish in ["butter chicken", "paneer", "biryani", "dal", "naan", "jamun"]):
        return ExtractedOrder(intent="INQUIRY", items=[])

    # Finalize intent
    finalize_keywords = ["that's it", "thats it", "cook it", "no more", "done", "finalize", "proceed", "no", "nothing else"]
    if any(clean_text == kw or clean_text.startswith(kw) or clean_text.endswith(kw) for kw in finalize_keywords):
        return ExtractedOrder(intent="FINALIZE", items=[])

    # Request bill intent
    bill_keywords = ["bill please", "generate bill", "check please", "bill", "invoice", "pay"]
    if any(kw in clean_text for kw in bill_keywords):
        return ExtractedOrder(intent="REQUEST_BILL", items=[])


    # Off-topic checks (e.g., coding, weather, math, general trivia)
    off_topic_keywords = [
        "python", "code", "weather", "world cup", "football", "cricket", "who is",
        "calculate", "essay", "song", "joke", "history", "capital of", "president"
    ]
    if any(kw in clean_text for kw in off_topic_keywords):
        return ExtractedOrder(intent="OFF_TOPIC", items=[])

    # Dish extraction
    all_dishes = [
        ("butter chicken", "Butter Chicken"),
        ("murg makhani", "Butter Chicken"),
        ("paneer tikka", "Paneer Tikka"),
        ("paneer", "Paneer Tikka"),
        ("hyderabadi biryani", "Hyderabadi Biryani"),
        ("biryani", "Hyderabadi Biryani"),
        ("dal makhani", "Dal Makhani"),
        ("dal", "Dal Makhani"),
        ("daal", "Dal Makhani"),
        ("garlic naan", "Garlic Naan"),
        ("naan", "Garlic Naan"),
        ("gulab jamun", "Gulab Jamun (2 pcs)"),
        ("jamun", "Gulab Jamun (2 pcs)"),
    ]

    word_to_num = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
        "ek": 1, "do": 2, "teen": 3, "char": 4, "paanch": 5
    }

    items = []
    
    # We can search for dishes and look behind for quantities
    for kw, canonical in all_dishes:
        # Find all occurrences of the dish in the text
        for match in re.finditer(rf'\b{kw}\b', clean_text):
            # Try to find a number right before the dish
            prefix = clean_text[:match.start()].strip().split()
            qty = 1
            if prefix:
                last_word = prefix[-1]
                if last_word.isdigit():
                    qty = int(last_word)
                elif last_word in word_to_num:
                    qty = word_to_num[last_word]
            
            # Avoid adding exact same dish multiple times if matched by different keywords
            # but if it's multiple of the same dish ordered separately, they get appended.
            items.append(OrderItem(dish_name=canonical, quantity=qty))

    if items:
        # Deduplicate items by dish_name (summing quantities if they appear multiple times)
        merged_items = {}
        for item in items:
            if item.dish_name in merged_items:
                merged_items[item.dish_name].quantity += item.quantity
            else:
                merged_items[item.dish_name] = item
        return ExtractedOrder(intent="ORDER", items=list(merged_items.values()))

    # If ordering keywords exist but dish is unknown (e.g., "pizza", "pasta", "burger")
    order_verbs = ["want", "give", "get", "order", "need", "plate", "bowl", "leke aao", "chahiye", "bring", "have"]
    if any(verb in clean_text for verb in order_verbs):
        # Extract the likely unknown noun
        words = clean_text.split()
        unknown_dish = " ".join([w for w in words if w not in ["i", "want", "give", "me", "order", "plate", "plates", "a", "an", "the", "please", "to", "chahiye", "do", "ek"]])
        # Look for quantity
        qty = 1
        num_match = re.search(r'\b(\d+)\b', clean_text)
        if num_match:
            qty = int(num_match.group(1))
        return ExtractedOrder(intent="ORDER", items=[OrderItem(dish_name=unknown_dish or clean_text, quantity=qty)])

    # Otherwise off-topic / unhandled
    return ExtractedOrder(intent="OFF_TOPIC", items=[])


def extract_user_intent(user_input: str) -> ExtractedOrder:
    """Extract order entity and intent using Groq or Gemini if configured, otherwise fallback to rule-based."""
    system_prompt = (
        "You are an Indian Dhaba order intent extractor. "
        "Analyze the user's message and determine their intent:\n"
        "- ORDER: if ordering food. Extract the list of dishes requested and their quantities (default to 1).\n"
        "- INQUIRY: if asking about the menu or prices.\n"
        "- GREETING: if saying hello.\n"
        "- FINALIZE: if the user says 'no', 'nothing else', 'that's it', 'cook it', or otherwise indicates they are done ordering and want to finalize.\n"
        "- REQUEST_BILL: if the user asks for the bill or check.\n"
        "- OFF_TOPIC: if unrelated to dining."
    )

    # 1. Try Groq if configured
    if GROQ_API_KEY and GROQ_API_KEY.strip():
        try:
            from langchain_groq import ChatGroq
            llm = ChatGroq(
                model=LLM_MODEL,
                groq_api_key=GROQ_API_KEY,
                temperature=0.0,
            )
            structured_llm = llm.with_structured_output(ExtractedOrder)
            result = structured_llm.invoke([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ])
            if isinstance(result, ExtractedOrder):
                return result
        except Exception:
            # Fallback to next provider or rule-based parser
            pass

    # 2. Try Gemini if configured
    if GEMINI_API_KEY and GEMINI_API_KEY.strip():
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            llm = ChatGoogleGenerativeAI(
                model=LLM_MODEL,
                google_api_key=GEMINI_API_KEY,
                temperature=0.0,
            )
            structured_llm = llm.with_structured_output(ExtractedOrder)
            result = structured_llm.invoke([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ])
            if isinstance(result, ExtractedOrder):
                return result
        except Exception:
            pass

    # 3. Deterministic rule-based fallback
    return rule_based_extract(user_input)



def validate_input(state: RestaurantState) -> RestaurantState:
    """
    LangGraph Node: Validates the user input.
    Extracts intent, dish, and quantity, and verifies against menu availability.
    """
    if state.get("is_terminal"):
        new_state: RestaurantState = dict(state)
        new_state["is_valid"] = False
        new_state["workflow_status"] = "TERMINATED"
        new_state["assistant_response"] = (
            "This session has concluded. Please start a new session or reset to place an order. Namaste!"
        )
        return new_state

    user_input = state.get("current_input", "").strip()
    extracted = extract_user_intent(user_input)

    # Copy current state
    new_state: RestaurantState = dict(state)
    new_state["intent"] = extracted.intent
    new_state["parsed_items"] = [item.dict() for item in extracted.items]

    current_status = state.get("workflow_status")

    if current_status == "AWAITING_CONFIRMATION":
        if extracted.intent == "FINALIZE" or (extracted.intent == "ORDER" and not extracted.items):
            new_state["is_valid"] = True
            new_state["intent"] = "FINALIZE"
            new_state["workflow_status"] = "CONFIRMED"
            return new_state
        elif extracted.intent == "ORDER" and extracted.items:
            pass  # Proceed to validate new order items
        elif extracted.intent not in ["GREETING", "INQUIRY"]:
            new_state["is_valid"] = False
            new_state["assistant_response"] = "Please let me know if you want to add anything else or if I should start cooking the order."
            return new_state

    if current_status == "AWAITING_BILL":
        if extracted.intent == "REQUEST_BILL" or extracted.intent == "FINALIZE" or (extracted.intent == "ORDER" and not extracted.items):
            new_state["is_valid"] = True
            new_state["intent"] = "REQUEST_BILL"
            new_state["workflow_status"] = "BILL_REQUESTED"
            return new_state
        elif extracted.intent == "ORDER" and extracted.items:
            pass  # User ordering more food after serving.
        elif extracted.intent not in ["GREETING", "INQUIRY"]:
            new_state["is_valid"] = False
            new_state["assistant_response"] = "I can bring you the bill now. Just say 'bill please', or let me know if you want to order more food."
            return new_state

    if extracted.intent == "GREETING":
        new_state["is_valid"] = True
        new_state["validation_error"] = None
        new_state["workflow_status"] = current_status if current_status in ["AWAITING_CONFIRMATION", "AWAITING_BILL"] else "IDLE"
        new_state["assistant_response"] = (
            "Namaste! Welcome to Desi Dhaba. "
            "What delicious Indian dish would you like to enjoy today?"
        )
        return new_state

    if extracted.intent == "INQUIRY":
        new_state["is_valid"] = True
        new_state["validation_error"] = None
        new_state["workflow_status"] = current_status if current_status in ["AWAITING_CONFIRMATION", "AWAITING_BILL"] else "IDLE"
        all_items = menu_repo.get_all()
        menu_listing = ", ".join([f"{item.name} (₹{int(item.price)}, {item.available_qty} left)" for item in all_items])
        new_state["assistant_response"] = (
            f"Here is what's fresh on our Dhaba menu today: {menu_listing}. "
            "What can I get started for you?"
        )
        return new_state

    if extracted.intent == "OFF_TOPIC":
        new_state["is_valid"] = False
        new_state["validation_error"] = "off_topic"
        new_state["assistant_response"] = (
            "Sorry, I can only assist with restaurant dining and food orders at Desi Dhaba. "
            "Please choose a dish from our menu!"
        )
        return new_state

    if extracted.intent in ["FINALIZE", "REQUEST_BILL"] and current_status not in ["AWAITING_CONFIRMATION", "AWAITING_BILL"]:
        new_state["is_valid"] = False
        new_state["validation_error"] = "invalid_state"
        new_state["assistant_response"] = "We haven't started an order yet. What would you like to have?"
        return new_state

    # Intent is ORDER
    validated_items = []

    for item in extracted.items:
        dish_query = item.dish_name or ""
        menu_item = menu_repo.find_by_name(dish_query)

        if not menu_item:
            new_state["is_valid"] = False
            new_state["validation_error"] = f"Dish '{dish_query}' is not available on our menu."
            new_state["assistant_response"] = (
                f"Sorry! '{dish_query}' is not on our Desi Dhaba menu today. "
                "Would you like to try our famous Butter Chicken or Paneer Tikka instead?"
            )
            return new_state

        requested_qty = item.quantity
        if requested_qty <= 0:
            new_state["is_valid"] = False
            new_state["validation_error"] = "Quantity must be at least 1."
            new_state["assistant_response"] = "Please select at least 1 plate to place an order."
            return new_state

        if requested_qty > menu_item.available_qty:
            new_state["is_valid"] = False
            new_state["validation_error"] = (
                f"Requested {requested_qty} portions of {menu_item.name}, but only {menu_item.available_qty} are available."
            )
            new_state["assistant_response"] = (
                f"We only have {menu_item.available_qty} plates of {menu_item.name} available right now! "
                f"Please adjust your order."
            )
            return new_state

        validated_items.append({
            "id": menu_item.id,
            "name": menu_item.name,
            "quantity": requested_qty,
            "unit_price": menu_item.price
        })

    if not validated_items:
        new_state["is_valid"] = False
        new_state["validation_error"] = "No dishes found in the order."
        new_state["assistant_response"] = "Please specify a dish and quantity."
        return new_state

    # Valid order items!
    new_state["is_valid"] = True
    new_state["validated_items"] = validated_items
    new_state["validation_error"] = None
    new_state["workflow_status"] = "VALIDATING"
    
    dish_names = [f"{it['quantity']}x {it['name']}" for it in validated_items]
    new_state["assistant_response"] = (
        f"Great choice! {', '.join(dish_names)} are available and validated."
    )
    return new_state


def respond_retry(state: RestaurantState) -> RestaurantState:
    """
    LangGraph Node: Handles invalid/off-topic attempts within the 3-attempt allowance.
    Increments invalid_attempts counter and provides courteous guidance.
    """
    new_state: RestaurantState = dict(state)
    current_attempts = new_state.get("invalid_attempts", 0) + 1
    new_state["invalid_attempts"] = current_attempts
    new_state["workflow_status"] = "RETRY"
    new_state["is_terminal"] = False

    validation_error = new_state.get("validation_error")
    intent = new_state.get("intent")
    attempts_remaining = max(0, 3 - current_attempts)

    # Use the specific message already determined during validation, appending attempt guidance
    base_response = new_state.get("assistant_response", "")
    if intent == "OFF_TOPIC":
        response = (
            f"Sorry, I can only assist with restaurant dining and food orders at Desi Dhaba. "
            f"Please choose a dish from our menu! ({attempts_remaining} attempt(s) remaining)"
        )
    elif base_response:
        response = f"{base_response} ({attempts_remaining} attempt(s) remaining)"
    else:
        response = (
            f"Please choose an item from our menu and specify the quantity. "
            f"({attempts_remaining} attempt(s) remaining)"
        )

    new_state["assistant_response"] = response

    if "messages" in new_state:
        messages = list(new_state.get("messages", []))
        if new_state.get("current_input"):
            messages.append({"role": "user", "content": new_state["current_input"]})
        messages.append({"role": "assistant", "content": response})
        new_state["messages"] = messages

    return new_state


def terminate_session(state: RestaurantState) -> RestaurantState:
    """
    LangGraph Node: Terminal node reached after exceeding the 3 invalid attempts limit.
    Sets is_terminal = True and provides a polite farewell.
    """
    new_state: RestaurantState = dict(state)
    current_attempts = new_state.get("invalid_attempts", 0) + 1
    new_state["invalid_attempts"] = max(current_attempts, 3)
    new_state["is_terminal"] = True
    new_state["workflow_status"] = "TERMINATED"

    farewell = (
        "We can only assist with dining orders at Desi Dhaba at this time. "
        "As we couldn't proceed with your order after multiple attempts, we must conclude this session. "
        "Thank you for visiting Desi Dhaba. Namaste!"
    )
    new_state["assistant_response"] = farewell

    if "messages" in new_state:
        messages = list(new_state.get("messages", []))
        if new_state.get("current_input"):
            messages.append({"role": "user", "content": new_state["current_input"]})
        messages.append({"role": "assistant", "content": farewell})
        new_state["messages"] = messages

    return new_state


def take_order(state: RestaurantState) -> RestaurantState:
    """
    LangGraph Node: Confirms valid order item, reserves menu inventory,
    appends to order_items, and transitions workflow_status to ORDER_PLACED.
    """
    new_state: RestaurantState = dict(state)
    validated_items = new_state.get("validated_items", [])
    
    if not validated_items:
        new_state["workflow_status"] = "RETRY"
        new_state["assistant_response"] = "Something went wrong identifying the dishes. Please try ordering again."
        return new_state

    order_items = list(new_state.get("order_items", []))
    total_bill_addition = 0.0
    confirmed_names = []
    reserved_in_this_batch = []

    for item in validated_items:
        item_id = item["id"]
        quantity = item["quantity"]
        item_name = item["name"]
        unit_price = item["unit_price"]

        reserved = menu_repo.reserve_stock(item_id, quantity)
        if not reserved:
            # Rollback this batch's reservations
            for r_id, r_qty in reserved_in_this_batch:
                menu_repo.release_stock(r_id, r_qty)
                
            new_state["is_valid"] = False
            new_state["workflow_status"] = "RETRY"
            new_state["assistant_response"] = (
                f"Apologies, stock for {item_name} just ran out or is insufficient! Please try ordering again."
            )
            return new_state

        reserved_in_this_batch.append((item_id, quantity))
        item_total = round(unit_price * quantity, 2)
        total_bill_addition += item_total
        confirmed_names.append(f"{quantity}x {item_name}")

        order_item = {
            "dish_id": item_id,
            "dish_name": item_name,
            "unit_price": unit_price,
            "quantity": quantity,
            "item_total": item_total,
        }
        order_items.append(order_item)

    new_state["order_items"] = order_items

    # Successful order placement: reset invalid attempts
    new_state["workflow_status"] = "AWAITING_CONFIRMATION"
    new_state["invalid_attempts"] = 0

    response = (
        f"Order added! {', '.join(confirmed_names)} (₹{total_bill_addition:.2f}) "
        f"have been taken. Do you want to add anything else, or should we start cooking?"
    )
    new_state["assistant_response"] = response

    if "messages" in new_state:
        messages = list(new_state.get("messages", []))
        if new_state.get("current_input"):
            messages.append({"role": "user", "content": new_state["current_input"]})
        messages.append({"role": "assistant", "content": response})
        new_state["messages"] = messages

    return new_state


def cook_order(state: RestaurantState) -> RestaurantState:
    """
    LangGraph Node: Simulates kitchen cooking preparation.
    Can trigger simulated failures (via force_cooking_fail or random simulation).
    Updates cooking_status and workflow_status.
    """
    new_state: RestaurantState = dict(state)
    order_items = new_state.get("order_items", [])
    dish_names = [f"{it['quantity']}x {it['dish_name']}" for it in order_items]
    dish_name_str = ", ".join(dish_names) if dish_names else "your dishes"

    force_fail = new_state.get("force_cooking_fail")
    simulate_random = new_state.get("simulate_random_failures", False)
    should_fail = (force_fail is True) or (force_fail is None and simulate_random and random.random() < 0.15)

    if should_fail:
        new_state["cooking_status"] = "FAILED"
        new_state["workflow_status"] = "COOKING_FAILED"
        new_state["failure_reason"] = "Kitchen mishap: Dish over-simmered or burnt in tandoor."
        return new_state

    # Cooking succeeded
    new_state["cooking_status"] = "SUCCESS"
    new_state["workflow_status"] = "COOKING"
    new_state["failure_reason"] = None
    cook_msg = f"Our chef is preparing your hot and fresh {dish_name_str} with authentic Indian spices."
    new_state["assistant_response"] = cook_msg
    return new_state


def handle_cooking_failure(state: RestaurantState) -> RestaurantState:
    """
    LangGraph Node: Handles simulated kitchen cooking failure.
    Restores stock, removes failed dish from order_items, informs user warmly,
    and resets dish selection so user can pick another dish.
    """
    new_state: RestaurantState = dict(state)
    order_items = new_state.get("order_items", [])
    dish_names = [f"{it['quantity']}x {it['dish_name']}" for it in order_items]
    dish_name_str = ", ".join(dish_names) if dish_names else "your dishes"

    # Restore inventory in menu repository for ALL order items
    for item in order_items:
        menu_repo.release_stock(item["dish_id"], item["quantity"])

    # Remove the failed items from order_items
    new_state["order_items"] = []

    # Clear validated items so user must re-select
    new_state["validated_items"] = []
    new_state["is_valid"] = False
    new_state["workflow_status"] = "RESELECT_DISH"

    apology = (
        f"Sorry! We ran into a kitchen issue while preparing your {dish_name_str}. "
        f"Please choose another dish from our menu and we'll get it started for you!"
    )
    new_state["assistant_response"] = apology

    if "messages" in new_state:
        messages = list(new_state.get("messages", []))
        messages.append({"role": "assistant", "content": apology})
        new_state["messages"] = messages

    return new_state


def serve_order(state: RestaurantState) -> RestaurantState:
    """
    LangGraph Node: Simulates table service and food delivery.
    Can trigger simulated failures (via force_serving_fail or random simulation).
    Updates serving_status and workflow_status.
    """
    new_state: RestaurantState = dict(state)
    order_items = new_state.get("order_items", [])
    dish_names = [f"{it['quantity']}x {it['dish_name']}" for it in order_items]
    dish_name_str = ", ".join(dish_names) if dish_names else "your dishes"

    force_fail = new_state.get("force_serving_fail")
    simulate_random = new_state.get("simulate_random_failures", False)
    should_fail = (force_fail is True) or (force_fail is None and simulate_random and random.random() < 0.15)

    if should_fail:
        new_state["serving_status"] = "FAILED"
        new_state["workflow_status"] = "SERVING_FAILED"
        new_state["failure_reason"] = "Service mishap: Serving platter slipped on the tray."
        return new_state

    # Serving succeeded
    new_state["serving_status"] = "SUCCESS"
    new_state["workflow_status"] = "AWAITING_BILL"
    new_state["failure_reason"] = None
    serve_msg = f"Your delicious {dish_name_str} is served fresh and hot at your table! Let me know when you're ready for the bill."
    new_state["assistant_response"] = serve_msg
    return new_state


def handle_serving_failure(state: RestaurantState) -> RestaurantState:
    """
    LangGraph Node: Handles simulated serving mishap.
    Increments serving_retries, resets force_serving_fail to prevent infinite loop,
    informs customer of rush re-cook, and routes back to cook_order.
    """
    new_state: RestaurantState = dict(state)
    order_items = new_state.get("order_items", [])
    dish_names = [f"{it['quantity']}x {it['dish_name']}" for it in order_items]
    dish_name_str = ", ".join(dish_names) if dish_names else "your dishes"
    retries = new_state.get("serving_retries", 0) + 1
    new_state["serving_retries"] = retries
    new_state["force_serving_fail"] = False  # Reset flag so re-cook loop recovers
    new_state["workflow_status"] = "RE_COOKING"
    new_state["cooking_status"] = "COOKING"
    new_state["serving_status"] = "PENDING"

    mishap_msg = (
        f"Oops! We had a slight slip while serving your {dish_name_str}. "
        f"Don't worry, our kitchen is rushing a fresh hot preparation right away!"
    )
    new_state["assistant_response"] = mishap_msg

    if "messages" in new_state:
        messages = list(new_state.get("messages", []))
        messages.append({"role": "assistant", "content": mishap_msg})
        new_state["messages"] = messages

    return new_state


def generate_bill(state: RestaurantState) -> RestaurantState:
    """
    LangGraph Node: Calculates itemized bill, 5% GST, and grand total.
    Constructs BillSummary and transitions workflow_status to COMPLETED.
    """
    new_state: RestaurantState = dict(state)
    order_items = list(new_state.get("order_items", []))

    subtotal = round(sum(item.get("item_total", 0.0) for item in order_items), 2)
    tax = round(subtotal * 0.05, 2)  # 5% GST
    grand_total = round(subtotal + tax, 2)

    now_str = datetime.now(timezone.utc).isoformat()

    bill_summary = {
        "items": order_items,
        "subtotal": subtotal,
        "tax": tax,
        "grand_total": grand_total,
        "generated_at": now_str,
    }

    new_state["bill"] = bill_summary
    new_state["workflow_status"] = "COMPLETED"

    # Build formatted bill presentation for assistant response
    item_lines = [
        f"• {it['quantity']}x {it['dish_name']} @ ₹{it['unit_price']:.2f} = ₹{it['item_total']:.2f}"
        for it in order_items
    ]
    items_block = "\n".join(item_lines) if item_lines else "• No items ordered."

    slip_note = ""
    if new_state.get("serving_retries", 0) > 0:
        slip_note = " (prepared fresh after a quick kitchen rush!)"

    bill_message = (
        f"Your meal has been served hot and fresh{slip_note}! Here is your itemized bill:\n\n"
        f"{items_block}\n"
        f"────────────────────────\n"
        f"Subtotal: ₹{subtotal:.2f}\n"
        f"GST (5%): ₹{tax:.2f}\n"
        f"Grand Total: ₹{grand_total:.2f}\n\n"
        f"Thank you for dining with Desi Dhaba! Namaste and enjoy your meal!"
    )
    new_state["assistant_response"] = bill_message

    if "messages" in new_state:
        messages = list(new_state.get("messages", []))
        messages.append({"role": "assistant", "content": bill_message})
        new_state["messages"] = messages

    return new_state


