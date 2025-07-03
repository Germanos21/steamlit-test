import streamlit as st
from data.supliers import all_supplier
from src.components.ebay_api import EbayAPI
from src.components.cart import Cart
from src.components.conf_variables import (
    CARDS_PER_PAGE,
    DEFAULT_PRICE_RANGE,
    PRICE_STEP,
    DEFAULT_ITEMS_PER_PAGE,
    ITEMS_PER_PAGE_OPTIONS,
    MAX_RETRIES,
    ERROR_MESSAGES,
    CATEGORIES,
    CONDITION_MAP,
    SORT_MAP
)
import math
from typing import List, Dict, Any, Callable, Optional, Tuple
import logging
import webbrowser
import os
from pathlib import Path
from src.components.document_viewer import open_supply_agreement, fill_agreement_template, detect_encoding, html_to_pdf_via_weasyprint
import io
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the absolute path to the application root directory
ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent
logger.info(f"Root directory: {ROOT_DIR}")

ASSETS_DIR = ROOT_DIR / 'assets'
DOCUMENTS_DIR = ASSETS_DIR / 'document_to_edit'

IMAGE_WIDTH = 300
IMAGE_HEIGHT = 200

ebay_api = EbayAPI()
cart = Cart()

if "cart_items" not in st.session_state:
    st.session_state.cart_items = []


def show_header(title: str, subtitle: str) -> None:
    with st.container():
        st.header(title, divider=True)
        st.caption(subtitle)


def show_image(image_path: str) -> None:
    try:
        st.image(image_path)
    except Exception:
        st.image("assets/images/placeholder.png")


def show_ebay_card(item: Dict[str, Any]) -> None:
    with st.container(border=True):
        st.markdown("""
            <style>
                div[data-testid="stContainer"] {
                    background: linear-gradient(135deg, 
                        rgba(26, 26, 26, 0.95) 0%,
                        rgba(75, 15, 30, 0.95) 50%,
                        rgba(26, 26, 26, 0.95) 100%
                    );
                    border: 1px solid #D4AF37;
                    border-radius: 0.5rem;
                    padding: 1rem;
                    margin-bottom: 1rem;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }
                div[data-testid="stContainer"]:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 10px 20px rgba(212, 175, 55, 0.3);
                    border: 1px solid #D4AF37;
                }
                div[data-testid="stMetric"] {
                    background: linear-gradient(135deg, 
                        rgba(139, 0, 0, 0.3) 0%,
                        rgba(75, 15, 30, 0.3) 100%
                    );
                    border: 1px solid #D4AF37;
                    border-radius: 0.5rem;
                    padding: 0.5rem;
                }
                div[data-testid="stMarkdown"] {
                    color: #FFF5E6;
                }
                h1, h2, h3, h4 {
                    color: #FFF5E6;
                    border-bottom: 2px solid #D4AF37;
                    padding-bottom: 0.5rem;
                }
                .product-title {
                    font-size: 1.1rem !important;
                    font-weight: 600;
                    color: #FFF5E6;
                    margin: 0.5rem 0 0.5rem 0;
                }
                .seller-name {
                    font-size: 1.4rem !important;
                    font-weight: 500;
                    color: #FFF5E6;
                    margin-bottom: 0.5rem;
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                }
                .price-metric {
                    font-size: 1.1rem !important;
                    font-weight: 500;
                    color: #FFD700;
                }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<div class='seller-name'>\U0001F464 {item['seller']}</div>", unsafe_allow_html=True)
            
        with st.container():
            col1, col2, col3 = st.columns([1, 8, 1], gap='small')
            with col2:
                show_image(item["image"])
        
        st.markdown(f"<div class='product-title'>{item['title']}</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1], gap="small")
        with col1:
            try:
                price = float(item['price']) * 3.65
                st.metric("💰 Price", f"AED {price:.2f}")
            except (ValueError, TypeError):
                st.metric("💰 Price", "N/A")
        with col2:
            st.markdown(f"**{item['condition']}**")
            unique_key = f"add_to_cart_{item.get('id', hash(item['title']))}"
            
            # Check if item is already in cart
            item_id = item.get('id', hash(item['title']))
            is_in_cart = cart.is_item_in_cart(item_id)
            
            if is_in_cart:
                if st.button("Remove from cart", key=unique_key):
                    cart.remove_item(item_id)
                    st.rerun()
            else:
                if st.button("Add to cart", key=unique_key):
                    cart.add_item(item)
                    st.rerun()
        col1, col2 = st.columns([2, 1])                    
        with col1:    
            st.markdown(f"[View on eBay]({item['url']})")
        with col2:
            status = "✅ Verified" if item.get("verified", False) else "❌ Not Verified"
            st.markdown(f"**{status}**")


def show_supplier_card(supplier: Dict[str, Any]) -> None:
    with st.container(border=True):
        st.markdown("""
            <style>
                div[data-testid="stContainer"] {
                    background: linear-gradient(135deg, 
                        rgba(26, 26, 26, 0.95) 0%,
                        rgba(75, 15, 30, 0.95) 50%,
                        rgba(26, 26, 26, 0.95) 100%
                    );
                    border: 1px solid #D4AF37;
                    border-radius: 0.5rem;
                    padding: 1rem;
                    margin-bottom: 1rem;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }
                div[data-testid="stContainer"]:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 10px 20px rgba(212, 175, 55, 0.3);
                    border: 1px solid #D4AF37;
                }
                div[data-testid="stMetric"] {
                    background: linear-gradient(135deg, 
                        rgba(139, 0, 0, 0.3) 0%,
                        rgba(75, 15, 30, 0.3) 100%
                    );
                    border: 1px solid #D4AF37;
                    border-radius: 0.5rem;
                    padding: 0.5rem;
                }
                div[data-testid="stMarkdown"] {
                    color: #FFF5E6;
                }
                h1, h2, h3, h4 {
                    color: #FFF5E6;
                    border-bottom: 2px solid #D4AF37;
                    padding-bottom: 0.5rem;
                }
                .product-title {
                    font-size: 1.1rem !important;
                    font-weight: 600;
                    color: #FFF5E6;
                    margin: 0.5rem 0 0.5rem 0;
                }
            </style>
        """, unsafe_allow_html=True)
        
        with st.container():
            st.markdown(f"<div class='product-title'>{supplier['name']}</div>", unsafe_allow_html=True)
            show_image(supplier["image"])
        with st.container():
            st.caption(f"📍 {supplier['location']}")
            
            col1, col2 = st.columns([2, 1], gap="small")
            with col1:
                st.metric("🚚 Delivery Time", supplier["delivery_time"])
            with col2:
                status = "✅ Verified" if supplier["verified"] else "❌ Not Verified"
                st.markdown(f"**{status}**")
                st.metric("💰 Price", f"${supplier['price']:.2f}")
                
            st.markdown(f"⭐ **Rating:** {supplier['rating']}/5.0")


def show_items_grid(items: List[Dict[str, Any]]) -> None:
    with st.container(border=True):
        st.markdown("""
            <style>
                div[data-testid="stContainer"] {
                    background: linear-gradient(135deg, 
                        rgba(26, 26, 26, 0.95) 0%,
                        rgba(75, 15, 30, 0.95) 50%,
                        rgba(26, 26, 26, 0.95) 100%
                    );
                    border: 1px solid #D4AF37;
                    border-radius: 0.5rem;
                    padding: 1rem;
                    margin-bottom: 1rem;
                }
            </style>
        """, unsafe_allow_html=True)
        
        for i in range(0, len(items), 3):
            cols = st.columns(3)
            row_items = items[i:i + 3]
            
            for col, item in zip(cols, row_items):
                with col:
                    show_ebay_card(item) if "title" in item else show_supplier_card(item)


def show_pagination(current_page: int, total_pages: int) -> None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        prev, _, next = st.columns([1, 2, 1])
        
        with prev:
            if st.button("⬅️ Previous", disabled=current_page == 0):
                st.session_state.page -= 1
                st.rerun()
                
        with next:
            if st.button("Next ➡️", disabled=current_page >= total_pages - 1):
                st.session_state.page += 1
                st.rerun()
                
        st.caption(f"Page {current_page + 1} of {total_pages}")


def sort_items(items: List[Dict[str, Any]], sort_by: str) -> List[Dict[str, Any]]:
    """Sort items based on the selected sort option."""
    try:
        # Get the sort key from SORT_MAP, defaulting to "Best Match"
        sort_key = SORT_MAP.get(sort_by, "bestMatch")
        
        # Sort the items based on the selected criteria
        if sort_key == "price":
            return sorted(items, key=lambda x: float(x.get("price", 0)))
        elif sort_key == "-price":
            return sorted(items, key=lambda x: -float(x.get("price", 0)))
        elif sort_key == "endTime":
            return sorted(items, key=lambda x: x.get("endTime", ""))
        elif sort_key == "newlyListed":
            return sorted(items, key=lambda x: x.get("listingDate", ""))
        else:  # bestMatch
            return items
    except Exception as e:
        logger.error(f"Error sorting items: {str(e)}")
        return items


def show_search_form() -> None:
    with st.form(key="search_form"):
        col1, col2 = st.columns(2, gap="large")
        
        with col1:  
            search_query = st.text_input("Product name")
            st.time_input("Expected shipment time")
            st.text_input("Location")
            
        with col2:
            max_price = st.slider(
                "Price",
                min_value=0,
                max_value=1000,
                value=0,
                step=1,
                format="%d",
            )
            st.radio("Verify", options=["Yes", "No"])
            st.number_input("Age", min_value=0)
            
        if st.form_submit_button("Search") and search_query:
            try:
                st.session_state.page = 0
                items = ebay_api.search_items(search_query)
                st.session_state.search_results = [ebay_api.format_item(item) for item in items]
                st.session_state.has_search = True
            except Exception as e:
                st.error(f"Error searching eBay: {str(e)}")


def validate_category(category: str, subcategory: Optional[str] = None) -> bool:
    """Validate if the selected category and subcategory are valid."""
    try:
        if category not in CATEGORIES:
            logger.error(f"Invalid category: {category}")
            return False
        
        if subcategory and category != "All Categories":
            if subcategory not in CATEGORIES[category]:
                logger.error(f"Invalid subcategory: {subcategory} for category: {category}")
                return False
        
        return True
    except Exception as e:
        logger.error(f"Error validating category: {str(e)}")
        return False


def handle_search_error(error: Exception) -> None:
    """Handle search errors and display appropriate messages."""
    error_message = str(error).lower()
    
    if "api" in error_message:
        st.error(ERROR_MESSAGES["api_error"])
    elif "category" in error_message:
        st.error(ERROR_MESSAGES["invalid_category"])
    elif "subcategory" in error_message:
        st.error(ERROR_MESSAGES["invalid_subcategory"])
    else:
        st.error(ERROR_MESSAGES["search_failed"])
    
    logger.error(f"Search error: {str(error)}")


def initialize_session_state() -> None:
    """Initialize session state variables for category selection with validation."""
    try:
        if "selected_category" not in st.session_state:
            st.session_state.selected_category = "All Categories"
        if "selected_subcategory" not in st.session_state:
            st.session_state.selected_subcategory = None
            
        # Validate existing session state
        if not validate_category(st.session_state.selected_category, st.session_state.selected_subcategory):
            st.session_state.selected_category = "All Categories"
            st.session_state.selected_subcategory = None
            st.warning("Invalid category selection was reset.")
    except Exception as e:
        logger.error(f"Session state initialization error: {str(e)}")
        st.error(ERROR_MESSAGES["session_error"])


def get_button_text() -> str:
    """Generate the text for the category selection button based on current selection."""
    try:
        if st.session_state.selected_category == "All Categories":
            return "Select Category"
        
        if not validate_category(st.session_state.selected_category, st.session_state.selected_subcategory):
            return "Select Category"
        
        text = st.session_state.selected_category
        if st.session_state.selected_subcategory:
            text += f" > {st.session_state.selected_subcategory}"
        return text
    except Exception as e:
        logger.error(f"Error getting button text: {str(e)}")
        return "Select Category"


def build_search_filters(condition: str, price_range: int) -> List[str]:
    """Build the filter string for the eBay API search with validation."""
    try:
        filters = []
        if condition != "Any" and condition in CONDITION_MAP:
            filters.append(f"conditions:{{{CONDITION_MAP[condition]}}}")
        if price_range < DEFAULT_PRICE_RANGE[1]:
            filters.append(f"price:[..{price_range}]")
        return filters
    except Exception as e:
        logger.error(f"Error building filters: {str(e)}")
        return []


def build_search_query() -> str:
    """Build the search query using selected category and subcategory with validation."""
    try:
        if not validate_category(st.session_state.selected_category, st.session_state.selected_subcategory):
            return ""
            
        if st.session_state.selected_category == "All Categories":
            return st.session_state.category_search if "category_search" in st.session_state else ""
        
        query = st.session_state.selected_category
        if st.session_state.selected_subcategory:
            query += f" {st.session_state.selected_subcategory}"
        
        # Add category search term if it exists
        if "category_search" in st.session_state and st.session_state.category_search:
            query += f" {st.session_state.category_search}"
            
        return query
    except Exception as e:
        logger.error(f"Error building search query: {str(e)}")
        return ""


@st.dialog("Select Category")
def category_dialog() -> None:
    """Display the category selection dialog with validation."""
    try:
        st.markdown("### Select Category")
        
        # Main category selection
        main_category = st.selectbox(
            "Main Category",
            options=list(CATEGORIES.keys()),
            index=0,  # Always start with first category
            key="dialog_main_category_select"
        )
        
        # Subcategory selection
        subcategory = None
        if main_category != "All Categories" and CATEGORIES[main_category]:
            subcategory = st.selectbox(
                "Subcategory",
                options=CATEGORIES[main_category],
                index=0,  # Always start with first subcategory
                key="dialog_subcategory_select"
            )
        
        # Dialog buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Apply", key="dialog_apply_category"):
                if validate_category(main_category, subcategory):
                    st.session_state.selected_category = main_category
                    st.session_state.selected_subcategory = subcategory
                    st.rerun()
                else:
                    st.error("Invalid category selection. Please try again.")
        with col2:
            if st.button("Cancel", key="dialog_cancel_category"):
                st.rerun()
    except Exception as e:
        logger.error(f"Error in category dialog: {str(e)}")
        st.error("An error occurred in the category selection. Please try again.")


def perform_search(search_query: str, filters: List[str], sort_by: str, items_per_page: int) -> List[Dict[str, Any]]:
    """Perform the eBay search with retry logic."""
    for attempt in range(MAX_RETRIES):
        try:
            items = ebay_api.search_items(
                search_query,
                limit=items_per_page,
                sort=SORT_MAP[sort_by],
                filters=",".join(filters) if filters else None
            )
            return [ebay_api.format_item(item) for item in items]
        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                raise e
            logger.warning(f"Search attempt {attempt + 1} failed: {str(e)}")
            continue


def show_ebay_search_form() -> None:
    """Display the eBay search form with category selection and filters."""
    try:
        initialize_session_state()
        
        with st.container():
            col1, col2 = st.columns(2, gap="large")
            
            with col1:
                st.markdown("""
                    <style>
                    div[data-testid="stButton"] button {
                        height: 2em;
                        width: 100%;
                        white-space: normal;
                        padding: 0.5em;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                col_button, col_input = st.columns([1, 3], gap="small")
                with col_button:
                    st.markdown("Choose Category")
                    if st.button(get_button_text(), key="main_category_button"):
                        category_dialog()
                with col_input:
                    st.markdown("")
                    st.text_input("Search within category", key="category_search", placeholder="Enter search term...")
                
                condition = st.selectbox(
                    "Condition",
                    options=["Any", "New", "Used", "Refurbished", "For parts or not working"],
                    index=0,
                    key="main_condition_select"
                )
                location = st.selectbox(
                    "Location",
                    options=["Worldwide", "United States", "Europe", "Asia", "Australia"],
                    index=0,
                    key="main_location_select"
                )
                
            with col2:
                price_range = st.slider(
                    "Maximum Price (DHS)",
                    min_value=DEFAULT_PRICE_RANGE[0],
                    max_value=DEFAULT_PRICE_RANGE[1],
                    value=DEFAULT_PRICE_RANGE[1],
                    step=PRICE_STEP,
                    format="%d",
                    key="main_price_slider"
                )
                sort_by = st.selectbox(
                    "Sort by",
                    options=list(SORT_MAP.keys()),
                    index=0,
                    key="main_sort_select"
                )
                items_per_page = st.selectbox(
                    "Items per page",
                    options=ITEMS_PER_PAGE_OPTIONS,
                    index=0,
                    key="main_items_per_page_select"
                )
                
                _, col_right = st.columns([5, 1], gap="small")
                with col_right:
                    if st.button("Search eBay", key="main_search_button", type="primary"):
                        try:
                            st.session_state.page = 0
                            
                            filters = build_search_filters(condition, price_range)
                            search_query = build_search_query()
                            
                            items = perform_search(search_query, filters, sort_by, items_per_page)
                            
                            st.session_state.search_results = items
                            st.session_state.has_search = True
                        except Exception as e:
                            handle_search_error(e)
    except Exception as e:
        logger.error(f"Error in search form: {str(e)}")
        st.error("An unexpected error occurred. Please try again later.")


def get_data_string() -> str:
    if "search_results" not in st.session_state:
        st.session_state.search_results = []
    item_strings = []
    for item in st.session_state.search_results:
        item_strings.append(f"{item.get('title', 'N/A')}|{item.get('price', '0.00')}|{item.get('condition', 'Unknown')}|{item.get('seller', 'Unknown')}|{item.get('comments', 'Unknown')}|{item.get('rating', 'Unknown')}")
    return "\n".join(item_strings)

def show_search_results() -> None:
    """Display the search results with sorting options."""
    st.header("Suppliers Listings")
    
    if "page" not in st.session_state:
        st.session_state.page = 0
    if "has_search" not in st.session_state:
        st.session_state.has_search = False
    if "search_results" not in st.session_state:
        st.session_state.search_results = []
    st.session_state.search_results_string = get_data_string()
    # print(st.session_state.search_results_string)

    items = st.session_state.search_results if st.session_state.has_search and st.session_state.search_results else all_supplier
    sorted_items = items
    
    total_pages = math.ceil(len(sorted_items) / CARDS_PER_PAGE)
    start_idx = st.session_state.page * CARDS_PER_PAGE
    current_items = sorted_items[start_idx:start_idx + CARDS_PER_PAGE]
    
    show_items_grid(current_items)
    show_pagination(st.session_state.page, total_pages)


@st.dialog("Email Template")
def show_email_dialog(supplier: Dict[str, Any]) -> None:
    """Display the email template dialog for a specific supplier."""
    try:
        if not supplier:
            st.error("No supplier data available")
            return
            
        st.markdown("### Email Template")
        # Email subject
        subject = st.text_input(
            "Subject",
            value=f"Inquiry about {supplier.get('title', 'product')} - AMPA Procurement Platform",
            key=f"email_subject_{supplier.get('id', hash(str(supplier)))}"
        )
        # Email body template
        default_body = f"""Dear {supplier.get('seller', 'Supplier')},\n\nI am interested in your product \"{supplier.get('title', 'product')}\" and would like to discuss potential business opportunities. I found your listing through the AMPA Procurement Platform.\n\nProduct Details:\n- {supplier.get('title', 'product')} (Price: AED {float(supplier.get('price', 0)) * 3.65:.2f})\n\nPlease provide the following information:\n1. Minimum Order Quantity (MOQ)\n2. Lead Time\n3. Payment Terms\n4. Shipping Options and Costs\n5. Product Specifications and Certifications\n\nLooking forward to your response.\n\nBest regards,\n[Your Name]\nAMPA Procurement Platform User\n"""
        body = st.text_area(
            "Email Body",
            value=default_body,
            height=300,
            key=f"email_body_{supplier.get('id', hash(str(supplier)))}"
        )
        # Email template buttons (no custom CSS, both use Streamlit buttons)
        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            if st.button("Send Email", key=f"send_email_button_{supplier.get('id', hash(str(supplier)))}"):
                st.success("Email has been sent successfully!")
                st.rerun()
        with col2:
            cart = Cart()
            root_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent
            agreement_file = root_dir / 'assets' / 'document_to_edit' / 'Supply_Agreement_Arial.html'
            if agreement_file.exists():
                encoding = detect_encoding(agreement_file)
                html_content = None
                for enc in [encoding, 'utf-16', 'utf-8-sig', 'windows-1252', 'latin-1']:
                    try:
                        with open(agreement_file, 'r', encoding=enc) as file:
                            html_content = file.read()
                            break
                    except UnicodeDecodeError:
                        continue
                if html_content:
                    seller_name = supplier.get('seller', 'Unknown Seller')
                    seller_items = [item for item in cart.items if item.get('seller') == seller_name]
                    if seller_items:
                        seller_info = {'seller': seller_name, 'items': seller_items}
                        html_content = fill_agreement_template(html_content, seller_info)
                        pdf_bytes = html_to_pdf_via_weasyprint(html_content)
                        st.download_button(
                            label="Agreement",
                            data=pdf_bytes,
                            file_name=f"Supply_Agreement_{seller_name}.pdf",
                            mime="application/pdf",
                            key=f"download_agreement_pdf_{supplier.get('id', hash(str(supplier)))}"
                        )
                
    except Exception as e:
        logger.error(f"Error in email dialog: {str(e)}")
        st.error(f"An error occurred while preparing the email template: {str(e)}")

def show_cart() -> None:
    """Display the shopping cart contents"""
    if not cart.items:
        st.info("Your cart is empty")
        return
        
    st.header("Shopping Cart", divider="red")
    
    st.markdown("""
        <style>
            div[data-testid="stContainer"] {
                background: linear-gradient(135deg, 
                    rgba(26, 26, 26, 0.95) 0%,
                    rgba(75, 15, 30, 0.95) 50%,
                    rgba(26, 26, 26, 0.95) 100%
                );
                border: 1px solid #D4AF37;
                border-radius: 0.5rem;
                padding: 1rem;
                margin-bottom: 1rem;
            }
            div[data-testid="stMetric"] {
                background: linear-gradient(135deg, 
                    rgba(139, 0, 0, 0.3) 0%,
                    rgba(75, 15, 30, 0.3) 100%
                );
                border: 1px solid #D4AF37;
                border-radius: 0.5rem;
                padding: 0.5rem;
            }
            /* Reduce font size of metric value in cart */
            div[data-testid="stMetricValue"] {
                font-size: 1.3rem !important;
            }
            div[data-testid="stMarkdown"] {
                color: #FFF5E6;
            }
            h1, h2, h3, h4 {
                color: #FFF5E6;
                border-bottom: 2px solid #D4AF37;
                padding-bottom: 0.5rem;
            }
        </style>
    """, unsafe_allow_html=True)
    
    total_price = 0
    for i, item in enumerate(cart.items):
        with st.container(border=True):
            col1, col2 = st.columns([3, 2])
            
            with col1:
                st.markdown(f"<span style='color: #FFF5E6; font-size: 1.05rem; font-weight: 500;'>{item['title']}</span>", unsafe_allow_html=True)
                st.markdown(f"👤 **Seller:** {item['seller']}")
                st.markdown(f"**Condition:** {item['condition']}")
                st.markdown(f"⭐ **Rating:** {item.get('rating', 'Unknown')}")
            
            with col2:
                try:
                    price = float(item['price']) * 3.65
                    total_price += price
                    st.metric("💰 **Price**", f"AED {price:.2f}")
                except (ValueError, TypeError):
                    st.metric("💰 **Price**", "N/A")

                # Replace rating with Contact button
                if st.button("Contact", key=f"contact_supplier_{i}"):
                    show_email_dialog(item)
                
                if st.button("Remove", key=f"remove_from_cart_{i}"):
                    cart.remove_item(item.get('id', hash(item['title'])))
                    st.rerun()
    
    st.divider()
    st.metric("Total", f"AED {total_price:.2f}")
