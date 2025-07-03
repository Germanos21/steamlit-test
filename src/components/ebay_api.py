import requests
from typing import List, Dict, Any, Optional
import os
import random
from dotenv import load_dotenv

class EbayAPI:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("EBAY_CLIENT_ID")
        self.client_secret = os.getenv("EBAY_CLIENT_SECRET")
        if not self.client_id or not self.client_secret:
            raise ValueError("EBAY_CLIENT_ID and EBAY_CLIENT_SECRET must be set in .env file")
        self.auth_url = "https://api.ebay.com/identity/v1/oauth2/token"
        self.search_url = "https://api.ebay.com/buy/browse/v1/item_summary/search"
        self._access_token = None

    def _get_access_token(self) -> str:
        """Get or refresh the access token."""
        if self._access_token:
            return self._access_token

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "scope": "https://api.ebay.com/oauth/api_scope"
        }

        try:
            response = requests.post(
                self.auth_url,
                headers=headers,
                data=data,
                auth=(self.client_id, self.client_secret)
            )
            response.raise_for_status()
            self._access_token = response.json()["access_token"]
            return self._access_token
        except Exception as e:
            raise Exception(f"Failed to get access token: {str(e)}")

    def search_items(self, query: str, limit: int = 10, sort: str = None, filters: str = None) -> List[Dict[str, Any]]:
        """
        Search for items on eBay.
        
        Args:
            query (str): Search query
            limit (int): Maximum number of items to return
            sort (str): Sort order (e.g., 'price', '-price', 'bestMatch')
            filters (str): Comma-separated filter string
            
        Returns:
            List[Dict[str, Any]]: List of items found
        """
        headers = {
            "Authorization": f"Bearer {self._get_access_token()}",
            "X-EBAY-C-MARKETPLACE-ID": "EBAY_US"
        }
        params = {
            "q": query,
            "limit": limit
        }
        
        if sort:
            params["sort"] = sort
        if filters:
            params["filter"] = filters

        try:
            response = requests.get(self.search_url, headers=headers, params=params)
            response.raise_for_status()
            return response.json().get("itemSummaries", [])
        except Exception as e:
            raise Exception(f"Failed to search items: {str(e)}")

    def format_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Format an item for display."""
        # Positive reviews
        positive_comments = [
            "Great product, exactly as described!",
            "Fast shipping and excellent packaging.",
            "Item arrived in perfect condition.",
            "Very satisfied with my purchase.",
            "Seller was very professional and responsive.",
            "Product quality exceeded my expectations.",
            "Would definitely buy from this seller again.",
            "Item was exactly what I was looking for.",
            "Shipping was faster than expected.",
            "Excellent communication throughout the process.",
            "The item is perfect for my needs!",
            "Great value for the money.",
            "Seller went above and beyond.",
            "Item was better than expected.",
            "Very happy with this purchase.",
            "Product is exactly what I needed.",
            "Excellent quality and service.",
            "Would buy again in a heartbeat.",
            "Item arrived early and in perfect condition.",
            "Best purchase I've made in a while!"
        ]

        # Mixed/neutral reviews
        mixed_comments = [
            "The item was a bit smaller than I expected.",
            "Product works great, but shipping took longer than expected.",
            "Good quality for the price.",
            "Item arrived damaged, but seller quickly resolved the issue.",
            "Description was accurate, but item was a bit worn.",
            "Decent product, but could be better quality.",
            "Shipping was slow, but item was as described.",
            "Product works fine, but instructions were unclear.",
            "Item was okay, but not worth the price.",
            "Seller was helpful when I had questions.",
            "Product arrived late, but in good condition."
        ]

        # Negative reviews
        negative_comments = [
            "Item was different from the picture.",
            "Quality is not as good as expected.",
            "Shipping took too long.",
            "Product was damaged upon arrival.",
            "Seller was unresponsive to messages.",
            "Item was missing parts.",
            "Not worth the money spent.",
            "Poor packaging led to damage.",
            "Product stopped working after a few days.",
            "Description was misleading.",
            "Item was used, not new as described.",
            "Very disappointed with this purchase.",
            "Would not recommend this seller.",
            "Product was not as advertised.",
            "Terrible customer service.",
            "Item was broken when it arrived.",
            "Waste of money.",
            "Never buying from this seller again.",
            "Product was a complete disappointment."
        ]

        # Select comments based on a weighted random distribution
        # 60% chance of positive, 30% chance of mixed, 10% chance of negative
        comment_type = random.choices(
            ['positive', 'mixed', 'negative'],
            weights=[0.6, 0.3, 0.1],
            k=1
        )[0]

        if comment_type == 'positive':
            comments = random.sample(positive_comments, 5)
            rating = random.randint(4, 5)  # High ratings for positive comments
        elif comment_type == 'mixed':
            comments = random.sample(mixed_comments, 5)
            rating = random.randint(3, 4)  # Middle ratings for mixed comments
        else:
            comments = random.sample(negative_comments, 5)
            rating = random.randint(1, 3)  # Lower ratings for negative comments

        return {
            "title": item.get("title", "No title"),
            "price": item.get("price", {}).get("value", "N/A"),
            "image": item.get("image", {}).get("imageUrl", "assets/images/placeholder.png"),
            "condition": item.get("condition", "Unknown"),
            "seller": item.get("seller", {}).get("username", "Unknown"),
            "url": item.get("itemWebUrl", "#"),
            "verified": random.random() < 0.8,
            "rating": rating,
            "comments": comments
        }
