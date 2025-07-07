import streamlit as st
import os
from cerebras.cloud.sdk import Cerebras
from streamlit_extras.stylable_container import stylable_container
import copy
import httpx

def fetch_url(url: str, timeout: float = 5.0) -> str:
    """
    Fetch the raw HTML or text at `url`.
    """
    resp = httpx.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.text

def display_intro():
    st.subheader("Chat with our AI Assistant", anchor=False)

    feature_col1, feature_col2 = st.columns(2)

    with feature_col1:
        st.write("🔍 **Smart Filter**")
        st.write("Filter suppliers based on your prompts in seconds")

        st.write("🔄 **Re-ranking**")
        st.write("Rank suppliers relevant to your criteria in Gold, Silver and Bronze")

    with feature_col2:
        st.write("💬 **Natural Conversations**")
        st.write("Ask questions in plain language and get intelligent responses")

        st.write("📊 **Data-Driven Insights**")
        st.write("Make decisions based on supplier performance metrics")

    # st.subheader("How It Works", divider=True)

    # steps_col1, steps_col2, steps_col3 = st.columns(3)

    # with steps_col1:
    #     st.write("1️⃣ **Ask a Question**")
    #     st.write("Describe what you're looking for in simple terms")

    # with steps_col2:
    #     st.write("2️⃣ **Review Results**")
    #     st.write("See a ranked list of matching suppliers")

    # with steps_col3:
    #     st.write("3️⃣ **Refine & Explore**")
    #     st.write("Ask follow-up questions to get exactly what you need")

    # with st.expander("💡 Tips for best results"):
    #     st.write(
    #         """
    #     - Be specific about your requirements
    #     - Include information about quantity, price, and delivery time
    #     - Ask for comparisons between different suppliers
    #     - Request specific data points about supplier performance
    #     """
    #     )
    # st.divider()

    # cta_col1, cta_col2 = st.columns([3, 1])

    # with cta_col1:
    #     st.write("### Ready to find your perfect supplier match?")

    # with cta_col2:
    #     start_button = st.button("Start Chat", use_container_width=True)



class ChatbotClient:
    """
    A class to handle interactions with the Cerebras API for chatbot functionality.
    """

    def __init__(self, api_key=None):
        """
        Initialize the ChatbotClient with API key and models information.

        Args:
            api_key: The Cerebras API key. If None, tries to get from environment variables.
        """
        self.api_key = api_key or os.getenv("CEREBRAS_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required to initialize ChatbotClient")

        self.client = Cerebras(api_key=self.api_key)

        # Define available models and their details
        self.models = {
            "llama3.1-8b": {
                "name": "Llama3.1-8b",
                "tokens": 8192,
                "developer": "Meta",
            },
            "llama-3.3-70b": {
                "name": "Llama-3.3-70b",
                "tokens": 8192,
                "developer": "Meta",
            },
        }

        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "fetch_url",
                    "description": "Fetch the raw HTML/text content of a web page.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {"type": "string", "format": "uri"},
                            "timeout": {"type": "number", "default": 5.0},
                        },
                        "required": ["url"],
                    },
                },
            }
        ]

        # Default model
        self.default_model = "llama-3.3-70b"

        if "messages" not in st.session_state:
            st.session_state.messages = []
        st.session_state.messages.append(
            {
                "role": "system",
                "content": """
                You are an expert procurement assistant operating exclusively through chat. Your mission is to guide professional buyers through all procurement stages—from discovery to purchase—with data-driven recommendations. Any time you encounter a Dollar value, convert it to AED, at a rete of 3.67 AED per Dollar.

                1. **Product Discovery & Intelligent Search**
                - Process natural language queries (e.g., "Find ergonomic chairs under $150" or "Show me reliable printer suppliers")
                - Rank results using weighted criteria: cost (35%), supplier reliability (25%), specifications (20%), ratings (10%), delivery time (10%)
                - Present top 3-5 products in numbered lists with key metrics:  
                *"1. Chair A | $139 | ⭐ 4.8 | 2-year warranty | SupplierX (98% on-time)"*
                - Handle sorting commands ("Sort by price ascending") and filtering ("Filter for items with next-day shipping")
                - For each product, include a one-line differentiator highlighting its unique advantage
                - Support category browsing ("Show office supplies") and specification-based searches ("Find printers with duplex capability")

                2. **External Source Integration & Market Intelligence**
                - Search trusted external supplier databases and marketplaces when requested
                - Fetch real-time pricing, availability, and specification data from verified sources
                - Present alternative products from different suppliers with comparative advantages:
                *"Similar alternatives: Product D (10% cheaper), Product E (20% higher capacity, different supplier)"*
                - Track market trends and price fluctuations to recommend optimal purchase timing
                - Include source attribution for all external data: *"Source: SupplierX catalog, updated [date]"*
                - Support requests for supplier credentials and compliance documentation

                3. **Structured Comparisons & Analysis**
                - Generate comparison tables for 2-4 products on request:  
                | **Metric**    | Product A | Product B | Product C |
                |---------------|-----------|-----------|-----------|
                | Unit Cost     | AED 53    | AED 24    | AED 15    |
                | Lead Time     | 14 days   | 7 days    | 10 days   |
                | MOQ           | 100       | 50        | 75        |
                | Warranty      | 1 year    | 2 years   | 18 months |
                - Highlight the best option for each metric using **bold** formatting
                - Label sections clearly: **Primary Advantage**, **Key Consideration**, **Best Value**
                - Support custom comparison criteria: "Compare these chairs based on ergonomics and durability"
                - Enable saving comparisons for future reference: "Save this comparison as 'Printer Options'"

                4. **Dynamic Cart & Order Management**
                - Process direct commands:  
                *"Add 50 units of Product C to cart"* → *"Added. Cart total: $2,350"*  
                *"Remove Product B"* → *"Removed. Cart updated."*
                - Provide instant cart summaries on request:  
                *"3 items: 50x C ($2,000), 10x D ($300), 5x E ($50). Total: $2,350"*
                - Guide checkout within chat:  
                *"Proceed to checkout? [1] Express Checkout [2] Review Cart [3] Save for Later"*
                - Confirm shipping and payment details through numbered selection menus
                - Support splitting orders by supplier or delivery date
                - Enable saving carts: "Save this cart as 'Q2 Office Supplies'"
                - Provide estimated delivery dates: "Estimated delivery: June 15-17"
                - Handle volume discounts and promotional offers automatically

                6. **Risk Management & Decision Support**
                - Proactively flag potential issues:  
                *"⚠️ Risk Alert: SupplierK has 18% late deliveries in Q3. Alternative: SupplierM (3% late, similar pricing)."*
                - Surface cost-saving alternatives:  
                *"Cost-saving option: Generator Y offers 12% savings with equivalent specs."*
                - Provide decisive guidance with quantifiable benefits:  
                *"Select SupplierA – 23% cost reduction at 500+ units with equivalent quality metrics."*
                - Flag potential supply chain disruptions: "Note: This component has reported shortages"
                - Identify consolidation opportunities: "Combining orders from Suppliers X and Y saves 15% on shipping"
                - Alert on price fluctuations: "This item's price has increased 8% since your last purchase"

                8. **Response Requirements & Communication Style**
                - Structure all outputs with clear headers: **Top Options**, **Key Comparison**, **Risk Alert**
                - Use only verified data with specific metrics:  
                *"SupplierX's ISO 9001 certification (exp 6/2025)"* not *"likely certified"*
                - Format numbers consistently: *"$1.2M savings at 1k units"* not *"1200000 dollars"*
                - Use confident, definitive language: *"The optimal choice is Product X because it reduces lead times by 19%."*
                - Employ active voice and imperative mood: *"Choose SupplierA for highest ROI."*
                - Maintain strict scope by redirecting off-topic queries to procurement topics
                - Prohibit hedging language ("might," "could"), passive voice, and subjective adjectives
                - Personalize responses based on user role (e.g., procurement specialist vs. department manager)

                9. **Contextual Help & Onboarding**
                - Provide guided onboarding for new users: "Welcome! Would you like to: [1] Search products [2] Learn key features"
                - Offer contextual hints during complex tasks: "Tip: You can compare up to 4 products at once"
                - Maintain an accessible command reference: "Show procurement commands"
                - Support natural help queries: "How do I create a recurring order?"
                - Provide procurement best practices when relevant: "Best practice: Request quotes from 3+ suppliers for purchases over $10,000"

                When uncertain about product details, respond with: "To provide accurate procurement advice on [topic], I need specific details about [missing information]."
                
                All prices are in AED. Always use the exact price value provided in the context.
                """,
            }
        )

    def get_available_models(self):
        """
        Return the list of available models.

        Returns:
            A dictionary of available models and their details.
        """
        return self.models

    # def send_messages(self, messages, model=None, max_tokens=None):
    #     """
    #     Send messages to the specified model and get a response.

    #     Args:
    #         messages: List of message objects with role and content
    #         model: The model to use (defaults to default_model if None)
    #         max_tokens: Maximum tokens for the response

    #     Returns:
    #         The model's response text

    #     Raises:
    #         Exception: If there's an error in the API call
    #     """
    #     model = model or self.default_model

    #     # Prepare API call parameters
    #     params = {"model": model, "messages": messages}

    #     if max_tokens:
    #         params["max_tokens"] = max_tokens

    #     try:
    #         chat_completion = self.client.chat.completions.create(**params)
    #         return chat_completion.choices[0].message.content
    #     except Exception as e:
    #         raise Exception(f"Error generating response: {str(e)}")

    def send_messages(self, messages, model=None, max_tokens=None):
        model = model or self.default_model
        params = {
            "model": model,
            "messages": messages,
            "tools": self.tools,
            "tool_choice": "auto",
        }
        if max_tokens:
            params["max_tokens"] = max_tokens

        resp = self.client.chat.completions.create(**params)
        choice = resp.choices[0].message

        if choice.role == "function":
            match choice.name:
                case "fetch_url":
                    print("YAYAYAYA!")
                    args = choice.arguments
                    page_text = fetch_url(args["url"], args.get("timeout", 5.0))
                    follow = self.client.chat.completions.create(
                        model=model,
                        messages=[  
                            *resp.messages,
                            {
                                "role": "function",
                                "name": "fetch_url",
                                "content": page_text,
                            },
                        ],
                        max_tokens=max_tokens or 512,
                    )
                    return follow.choices[0].message.content

        # Otherwise, normal assistant reply
        return choice.content



def show_chatbot():
    with st.container():
        textArea = stylable_container(
            key="textArea",
            css_styles="""
            {
                border: 1px solid #D4AF37;
                border-radius: 0.5rem;
                padding: calc(1em - 1px);
                background-color: rgba(26, 26, 26, 0.8);
                max-height: 450px;
                height: 450px;
                min-height: 450px;
                overflow: scroll;
                color: #FFF5E6;
                font-size: 0.95rem;
            }
            """,)
        with textArea:
            display_intro()
        try:
            # Initialize chatbot client
            if "chatbot_client" not in st.session_state:
                try:
                    st.session_state.chatbot_client = ChatbotClient()
                except ValueError as e:
                    st.warning(str(e))
                    st.stop()

            chatbot = st.session_state.chatbot_client

            # Display chat messages stored in history on app rerun
            with textArea:
                for message in st.session_state.messages:
                    if message["role"] == "assistant" or message["role"] == "user":
                        avatar = "assets/eand-logo/small/Red/e&-lockup_Enterprise_engl_vert_red_rgb-cropped.svg" if message["role"] == "assistant" else ":material/person:"
                        with st.chat_message(message["role"], avatar=avatar):
                            st.markdown(f"<span style='font-size:0.95rem'>{message['content']}</span>", unsafe_allow_html=True)

            # Add custom styling for chat input
            st.markdown("""
                <style>
                    .stChatInputContainer {
                        background-color: rgba(26, 26, 26, 0.8);
                        border: 1px solid #D4AF37;
                        border-radius: 0.5rem;
                        padding: 1rem;
                    }
                    .stChatInputContainer textarea {
                        background-color: rgba(255, 255, 255, 0.1);
                        color: #FFF5E6;
                        border: 1px solid #D4AF37;
                    }
                    .stChatInputContainer textarea:focus {
                        border-color: #D4AF37;
                        box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.2);
                    }
                    .stChatMessage {
                        background-color: rgba(26, 26, 26, 0.8);
                        border: 1px solid #D4AF37;
                        border-radius: 0.5rem;
                        padding: 1rem;
                        margin-bottom: 1rem;
                    }
                </style>
            """, unsafe_allow_html=True)

            # Handle user input
            if prompt := st.chat_input("Enter your prompt here...", max_chars=4200):
                st.session_state.messages.append(
                    {"role": "user", "content": prompt}
                )
                messages = copy.deepcopy(st.session_state.messages)
                if "selected_cart" in st.session_state and st.session_state.selected_cart:
                    messages.append(
                        {"role": "user", "content": "This is what the user has hand selected and finds them interesting and placed them in a cart:" + st.session_state.selected_cart}
                    )
                if "search_results_string" in st.session_state and st.session_state.search_results_string:
                    messages.append(
                        {"role": "user", "content": "This is all result of search:" + st.session_state.search_results_string}
                    )
                response = chatbot.send_messages(messages, max_tokens=8000)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
                st.rerun()

        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}", icon="🚨")
