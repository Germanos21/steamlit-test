from typing import List, Dict, Any, Optional
import streamlit as st
import src.components.chatbot 

class Cart:
    """
    A class to manage a shopping cart for eBay items.
    """

    def __init__(self):
        """Initialize cart with items from session state."""
        if "cart_items" not in st.session_state:
            st.session_state.cart_items = []
        
        self.items = st.session_state.cart_items
        self.clean_data = []

        if "selected_cart" not in st.session_state:
            st.session_state.selected_cart = []

    def add_item(self, item: Dict[str, Any]) -> None:
        """
        Add an item to the cart.
        
        Args:
            item (Dict[str, Any]): The item to add to the cart
        """
        # Create a copy of the item to avoid modifying the original
        cart_item = item.copy()
        # Add a unique ID if not present
        if 'id' not in cart_item:
            cart_item['id'] = hash(cart_item.get('title', ''))
        
        self.items.append(cart_item)
        st.session_state.cart_items = self.items  # Update session state
        self.clean_data = self.prepare_data_to_chat()
        st.session_state.selected_cart = self.get_cart_data_string()
        
    def remove_item(self, item_id: Any) -> None:
        """
        Remove an item from the cart by its ID.
        
        Args:
            item_id (Any): The ID of the item to remove
        """
        self.items = [item for item in self.items if item.get('id') != item_id]
        st.session_state.cart_items = self.items  # Update session state
        st.session_state.selected_cart = self.get_cart_data_string()

    def is_item_in_cart(self, item_id: Any) -> bool:
        """
        Check if an item is in the cart.
        
        Args:
            item_id (Any): The ID of the item to check
            
        Returns:
            bool: True if the item is in the cart, False otherwise
        """
        return any(item.get('id') == item_id for item in self.items)
        
    def get_items(self) -> List[Dict[str, Any]]:
        """
        Get all items in the cart.
        
        Returns:
            List[Dict[str, Any]]: List of items in the cart
        """
        return self.items
        
    def clear(self) -> None:
        """Clear all items from the cart."""
        self.items = []
        st.session_state.cart_items = []  # Update session state
        
    def get_total(self) -> float:
        """
        Calculate the total price of all items in the cart.
        
        Returns:
            float: The total price of all items in the cart
        """
        total = 0.0
        for item in self.items:
            try:
                price = float(item.get('price', 0))
                total += price
            except (ValueError, TypeError):
                pass
        return total
        
    def display(self) -> None:
        """
        Display the cart contents using Streamlit.
        """
        if not self.items:
            st.info("Your cart is empty")
            return
        
        print(self.clean_data)
        st.header("Shopping Cart")
        
        total_price = 0
        for i, item in enumerate(self.items):
            with st.container(border=True):
                col1, col2 = st.columns([3, 2])
                
                with col1:
                    st.markdown(item["title"])
                    st.markdown(f"👤 **Seller:** {item['seller']}")
                    st.markdown(f"**Condition:** {item['condition']}")
                
                with col2:
                    try:
                        price = float(item['price']) * 3.65
                        total_price += price
                        st.metric("💰 **Price**", f"AED {price:,.2f}")
                        
                    except (ValueError, TypeError):
                        st.metric("💰 **Price**", "N/A")

                    st.markdown(f"⭐ **Rating:** {item.get('rating', 'Unknown')}")
                    
                    if st.button("Remove", key=f"remove_from_cart_{i}"):
                        self.remove_item(item.get('id', hash(item['title'])))
                        st.rerun()
        st.divider()
        st.metric("Total", f"AED {total_price:,.2f}")

        # if st.button("Export to chat"):
        #     try:
        #         chatbot = st.session_state.chatbot_client
        #     except:
        #         st.error("No Chatbot found")
        #     data = self.get_cart_data_string()
        #     response = chatbot.send_message(data)

        #     st.session_state.messages.append(
        #         {"role": "user", "content": data}
        #     )
        #     st.session_state.messages.append(
        #         {"role": "assistant", "content": response}
        #     )
            # st.rerun()


    def prepare_data_to_chat(self) -> List[Dict[str, Any]]:
        """
        Prepare cart data for AI chat by removing unnecessary fields.
        
        Returns:
            List[Dict[str, Any]]: List of cleaned cart items with only relevant fields
        """
        cleaned_items = []
        for item in self.items:
            cleaned_item = {
                'title': item.get('title', ''),
                'price': item.get('price', '0.00'),
                'condition': item.get('condition', 'Unknown'),
                'seller': item.get('seller', 'Unknown'),
                'comments': item.get('comments', 'Unknown'),
                'rating': item.get('rating', 'Unknown')
            }
            cleaned_items.append(cleaned_item)
        return cleaned_items


    def get_cart_data_string(self) -> str:
        """
        Convert cart items to a clean, pipe-delimited string format.
        
        Returns:
            str: Each item as "Title|Price|Condition|Seller" 
                Returns "empty" if cart is empty
                
        Example:
            "Item 1|10.00|New|SellerA\nItem 2|20.00|Used|SellerB"
        """
        if not self.items:
            return "empty"
        
        item_strings = []
        for item in self.items:
            try:
                item_str = (
                    f"{item.get('title', 'N/A')}|"
                    f"{item.get('price', '0.00')}|"
                    f"{item.get('condition', 'Unknown')}|"
                    f"{item.get('seller', 'Unknown')}|"
                    f"{item.get('comments', 'Unknown')}|"
                    f"{item.get('rating', 'Unknown')}"
                )
                item_strings.append(item_str)
            except Exception as e:
                print(f"Error formatting item: {e}")
                continue
        
        return "\n".join(item_strings)