import streamlit as st
import random
import os
from pathlib import Path
import logging
from datetime import datetime
from bs4 import BeautifulSoup
import chardet
import re
from src.components.cart import Cart
from typing import Dict, Any
import requests  # Add this for API calls
import io
import base64

logger = logging.getLogger(__name__)

# Add this at the top with other imports
SAMPLE_COUNTRIES = [
    "United States, New York",
    "United Kingdom, London",
    "Japan, Tokyo",
    "Germany, Berlin",
    "France, Paris",
    "Canada, Toronto",
    "Australia, Sydney",
    "Singapore",
    "South Korea, Seoul",
    "Netherlands, Amsterdam"
]

def detect_encoding(file_path):
    """Detect the encoding of a file using chardet."""
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def embed_local_images_as_base64(html_content, base_dir):
    """
    Replace all <img src="..."> tags with local paths in the HTML with base64-encoded data URIs.
    base_dir: directory to resolve relative image paths from.
    """
    def repl(match):
        src = match.group(1)
        if src.startswith('http://') or src.startswith('https://') or src.startswith('data:'):
            return match.group(0)  # leave remote/data images unchanged
        img_path = os.path.join(base_dir, src)
        if not os.path.exists(img_path):
            return match.group(0)  # leave unchanged if not found
        ext = os.path.splitext(img_path)[1].lower()
        if ext == '.png':
            mime = 'image/png'
        elif ext in ['.jpg', '.jpeg']:
            mime = 'image/jpeg'
        elif ext == '.gif':
            mime = 'image/gif'
        else:
            mime = 'application/octet-stream'
        with open(img_path, 'rb') as f:
            encoded = base64.b64encode(f.read()).decode('utf-8')
        return match.group(0).replace(src, f'data:{mime};base64,{encoded}')

    # Replace all <img src="...">
    return re.sub(r'<img[^>]+src=["\"](.*?)["\"]', repl, html_content)

def fill_agreement_template(html_content: str, seller_info: dict) -> str:
    """Fill the agreement template with seller information."""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Get current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Find and replace all text nodes
        for element in soup.find_all(string=True):
            if '[DATE]' in str(element):
                element.replace_with(str(element).replace('[DATE]', current_date))
            elif '[SUPPLIER NAME]' in str(element):
                element.replace_with(str(element).replace('[SUPPLIER NAME]', seller_info.get('seller', 'Unknown Seller')))
            elif '[SUPPLIER ADDRESS]' in str(element):
                supplier_address = random.choice(SAMPLE_COUNTRIES)
                element.replace_with(str(element).replace('[SUPPLIER ADDRESS]', supplier_address))
            elif '[CUSTOMER NAME]' in str(element):
                element.replace_with(str(element).replace('[CUSTOMER NAME]', "AMPA Procurement"))
            elif '[CUSTOMER ADDRESS]' in str(element):
                element.replace_with(str(element).replace('[CUSTOMER ADDRESS]', "Dubai, United Arab Emirates"))

        # Get all items for this seller
        seller_items = seller_info.get('items', [])
        if not seller_items:  # If no items list provided, treat seller_info as a single item
            seller_items = [seller_info]
            
        logger.info(f"Processing {len(seller_items)} items for seller {seller_info.get('seller', 'Unknown Seller')}")
            
        # Calculate total price for all items
        total_price = sum(float(item.get('price', 0)) * 3.65 for item in seller_items)
        logger.info(f"Total price calculated: AED {total_price:,.2f}")

        # Find the ordered list that contains the items
        ordered_list = soup.find('ol')
        if ordered_list:
            # Remove all existing list items
            for item in ordered_list.find_all('li'):
                item.decompose()
            
            # Create new list items for each product
            for item in seller_items:
                product_title = item.get('title', 'Unknown Product')
                product_price = float(item.get('price', 0)) * 3.65
                product_condition = item.get('condition', 'Not specified')
                
                # Create product description
                product_description = f"{product_title} - {product_condition} - AED {product_price:,.2f}"
                logger.info(f"Adding product to agreement: {product_description}")
                
                # Create new list item
                new_li = soup.new_tag('li')
                new_li['class'] = 'MsoNormal'
                new_li['style'] = 'mso-margin-top-alt:auto;mso-margin-bottom-alt:auto;mso-list:l4 level1 lfo3;tab-stops:list 36.0pt'
                
                # Create span for the text
                span = soup.new_tag('span')
                span['lang'] = 'EN-US'
                span['style'] = 'font-size:12.0pt;font-family:"Calibri",sans-serif;mso-fareast-font-family:"MS PGothic"'
                span.string = product_description
                
                new_li.append(span)
                ordered_list.append(new_li)
                logger.info(f"Successfully added product to list: {product_title}")

        # Find the PRICE heading and its following paragraph
        price_heading = soup.find('strong', string=lambda text: text and 'PRICE' in text)
        if price_heading:
            # Get the parent paragraph
            price_section = price_heading.find_parent('p')
            if price_section:
                # Find the next paragraph that contains the price description
                price_desc_para = price_section.find_next_sibling('p')
                if price_desc_para:
                    # Create a new paragraph for the price display
                    price_display = soup.new_tag('p')
                    price_display['style'] = 'font-size: 18pt; font-weight: bold; text-align: center; color: #000000; margin: 20px 0;'
                    
                    # If multiple items, show "Total Agreed Price", otherwise just "Agreed Price"
                    price_label = "Total Agreed Price" if len(seller_items) > 1 else "Agreed Price"
                    price_display.string = f"{price_label}: AED {total_price:,.2f}"
                    logger.info(f"Added price display: {price_label}: AED {total_price:,.2f}")
                    
                    # Insert the price display after the price description paragraph
                    price_desc_para.insert_after(price_display)
        
        # Update signature section
        signature_sections = soup.find_all('td')
        for section in signature_sections:
            if section.find(string=lambda text: text and 'SUPPLIER' in text):
                # Find the print name field (underlined field)
                name_field = section.find('u')
                if name_field:
                    name_field.string = seller_info.get('seller', 'Unknown Seller')
                # Find the date field
                date_fields = section.find_all('p')
                for field in date_fields:
                    if field.get_text() and 'Date' in field.get_text():
                        field.string = f"Date: {current_date}"
            elif section.find(string=lambda text: text and 'CUSTOMER' in text):
                # Find the print name field (underlined field)
                name_field = section.find('u')
                if name_field:
                    name_field.string = "AMPA Procurement Representative"
                # Find the date field
                date_fields = section.find_all('p')
                for field in date_fields:
                    if field.get_text() and 'Date' in field.get_text():
                        field.string = f"Date: {current_date}"
        
        logger.info("Successfully filled agreement template")
        return str(soup)
    except Exception as e:
        logger.error(f"Error filling agreement template: {str(e)}")
        raise

def group_items_by_seller(cart_items):
    """Group cart items by seller and return a dictionary of seller information with their items."""
    sellers = {}
    for item in cart_items:
        seller_name = item.get('seller', 'Unknown Seller')
        if seller_name not in sellers:
            # Create new seller entry with first item
            sellers[seller_name] = {
                'seller': seller_name,
                'items': [item]
            }
        else:
            # Add item to existing seller's items list
            sellers[seller_name]['items'].append(item)
    return sellers

@st.dialog("Email Template")
def show_email_dialog(supplier: Dict[str, Any]) -> None:
    """Display the email template dialog for a specific supplier."""
    try:
        if not supplier:
            st.error("No supplier data available")
            return
            
        # Email subject
        subject = st.text_input(
            "Subject",
            value=f"Inquiry about {supplier.get('title', 'product')} - AMPA Procurement Platform",
            key=f"email_subject_{supplier.get('id', hash(str(supplier)))}"
        )
        
        # Email body template
        default_body = f"""Dear {supplier.get('seller', 'Supplier')},

I am interested in your product "{supplier.get('title', 'product')} (Price: AED {float(supplier.get('price', 0)) * 3.65:,.2f})" and would like to discuss potential business opportunities. I found your listing through the AMPA Procurement Platform.

Product Details:
- {supplier.get('title', 'product')} (Price: AED {float(supplier.get('price', 0)) * 3.65:,.2f})

Please provide the following information:
1. Minimum Order Quantity (MOQ)
2. Lead Time
3. Payment Terms
4. Shipping Options and Costs
5. Product Specifications and Certifications

Looking forward to your response.

Best regards,
[Your Name]
AMPA Procurement Platform User
"""
        
        body = st.text_area(
            "Email Body",
            value=default_body,
            height=300,
            key=f"email_body_{supplier.get('id', hash(str(supplier)))}"
        )
        
        # --- Prepare the download data if available ---
        download_ready = False
        download_data = None
        download_filename = None

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
                    # Embed images as base64 before PDF conversion
                    base_dir = os.path.join(root_dir, 'assets', 'document_to_edit')
                    html_content = embed_local_images_as_base64(html_content, base_dir)
                    download_ready = True
                    download_data = html_content
                    download_filename = f"Supply_Agreement_{seller_name}.html"

        # Both buttons use st.button and will be styled identically by global style.css
        send_clicked = st.button("Send Email", key=f"send_email_button_{supplier.get('id', hash(str(supplier)))}")
        agreement_clicked = st.button("Agreement", key=f"agreement_button_{supplier.get('id', hash(str(supplier)))}")
        if agreement_clicked and download_ready:
            try:
                api_key = os.environ.get("PDFSHIFT_API_KEY")
                if not api_key:
                    st.error("PDFShift API key is not set. Please contact the administrator.")
                    st.stop()
                pdf_bytes = html_to_pdf_via_pdfshift(download_data, api_key)
                st.download_button(
                    label="Download Agreement (PDF)",
                    data=pdf_bytes,
                    file_name=download_filename.replace('.html', '.pdf'),
                    mime="application/pdf",
                    key=f"download_agreement_pdf_{hash(str(supplier))}"
                )
            except Exception as e:
                st.error(f"Failed to generate PDF: {e}")
        if send_clicked:
            st.success("Email has been sent successfully!")
            st.rerun()

    except Exception as e:
        logger.error(f"Error displaying email dialog: {str(e)}")
        st.error(f"Error displaying email dialog: {str(e)}")

def open_supply_agreement(seller_info: dict = None):
    """Triggers download of the Supply Agreement HTML file with filled details."""
    try:
        # Get the absolute path to the application root directory
        root_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent
        agreement_file = root_dir / 'assets' / 'document_to_edit' / 'Supply_Agreement_Arial.html'
        
        if agreement_file.exists():
            # First detect the file encoding
            encoding = detect_encoding(agreement_file)
            
            # Try reading with detected encoding, fallback to common encodings if that fails
            encodings_to_try = [encoding, 'utf-16', 'utf-8-sig', 'windows-1252', 'latin-1']
            html_content = None
            
            for enc in encodings_to_try:
                try:
                    with open(agreement_file, 'r', encoding=enc) as file:
                        html_content = file.read()
                        break
                except UnicodeDecodeError:
                    continue
            
            if html_content is None:
                raise ValueError("Could not read file with any known encoding")
                
            if seller_info:
                # Get cart instance
                cart = Cart()
                
                # Get all items from the same seller
                seller_name = seller_info.get('seller', 'Unknown Seller')
                seller_items = [
                    item for item in cart.items 
                    if item.get('seller') == seller_name
                ]
                
                if seller_items:
                    # Create a new seller_info dict with all items
                    seller_info = {
                        'seller': seller_name,
                        'items': seller_items
                    }
                
                # Fill the template with seller information
                html_content = fill_agreement_template(html_content, seller_info)
                # Embed images as base64 before PDF conversion
                base_dir = os.path.join(root_dir, 'assets', 'document_to_edit')
                html_content = embed_local_images_as_base64(html_content, base_dir)
                # PDF download button only
                try:
                    api_key = os.environ.get("PDFSHIFT_API_KEY")
                    if not api_key:
                        st.error("PDFShift API key is not set. Please contact the administrator.")
                        st.stop()
                    pdf_bytes = html_to_pdf_via_pdfshift(html_content, api_key)
                    st.download_button(
                        label="Agreement",
                        data=pdf_bytes,
                        file_name=f"Supply_Agreement_{seller_info.get('seller', 'Unknown')}.pdf",
                        mime="application/pdf",
                        key=f"download_agreement_pdf_{seller_info.get('id', hash(str(seller_info)))}"
                    )
                except Exception as e:
                    st.error(f"Failed to generate PDF: {e}")
                return True
        else:
            st.error(f"Supply Agreement file not found at: {agreement_file}")
            return False
    except Exception as e:
        logger.error(f"Error preparing Supply Agreement download: {str(e)}")
        st.error(f"Error preparing Supply Agreement download: {str(e)}")
        return False

def html_to_pdf_via_pdfshift(html_content: str, api_key: str) -> bytes:
    """Convert HTML to PDF using the PDFShift API (using X-API-Key header)."""
    url = "https://api.pdfshift.io/v3/convert/pdf"
    headers = {"X-API-Key": api_key}
    response = requests.post(
        url,
        headers=headers,
        json={"source": html_content}
    )
    if response.status_code == 200:
        return response.content
    else:
        raise RuntimeError(f"PDFShift API error: {response.status_code} {response.text}")