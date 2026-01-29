import streamlit as st
import requests
import google.generativeai as genai
import os

# Configure Gemini API
# Replace 'YOUR_GEMINI_API_KEY' with your actual Gemini API key
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY"))

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-pro')

MCP_SERVER_URL = "http://127.0.0.1:5001"

st.title("Agentic Commerce Product Discovery")

@st.cache_data
def get_products():
    try:
        response = requests.get(f"{MCP_SERVER_URL}/ucp/products")
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching products from MCP server: {e}")
        return []

products = get_products()

if products:
    st.sidebar.header("Available Products")
    for product in products:
        st.sidebar.write(f"- {product['name']} (${product['price']})")

user_query = st.text_input("What are you looking for today?")

if user_query:
    st.write(f"Searching for: {user_query}")

    # Use Gemini to understand the user's intent and filter products
    # This is a simplified example. In a real scenario, Gemini would extract entities
    # like product names, categories, price ranges, etc.
    prompt = f"Given the following products and their attributes (name, description, price, category, gtin, brand, offers): {json.dumps(products)}\n\nUser query: {user_query}\n\nBased on the user query, identify relevant filtering criteria (e.g., product name, category, price range). Return a JSON object with keys for each filtering criterion and their values. For price range, use 'min_price' and 'max_price'. If no specific criteria are found, return an empty JSON object. Example: {{'category': 'Electronics', 'min_price': 100, 'max_price': 500}}" # noqa

    try:
        response = model.generate_content(prompt)
        filter_criteria_str = response.text.strip()
        try:
            filter_criteria = json.loads(filter_criteria_str)
        except json.JSONDecodeError:
            st.error(f"Gemini returned invalid JSON: {filter_criteria_str}")
            filter_criteria = {}

        filtered_products = products
        if filter_criteria:
            if 'category' in filter_criteria:
                filtered_products = [p for p in filtered_products if p.get('category') == filter_criteria['category']]
            if 'min_price' in filter_criteria:
                filtered_products = [p for p in filtered_products if p.get('price', 0) >= filter_criteria['min_price']]
            if 'max_price' in filter_criteria:
                filtered_products = [p for p in filtered_products if p.get('price', float('inf')) <= filter_criteria['max_price']]
            if 'name' in filter_criteria:
                # Basic case-insensitive name filtering
                name_query = filter_criteria['name'].lower()
                filtered_products = [p for p in filtered_products if name_query in p.get('name', '').lower()]

        if filtered_products:
            st.subheader("Relevant Products:")
            for product in filtered_products:
                st.write(f"### {product['name']}")
                st.write(f"**Category:** {product['category']}")
                st.write(f"**Price:** ${product['price']}")
                st.write(f"**Description:** {product['description']}")
                if 'offers' in product and product['offers'] and 'url' in product['offers'][0]:
                    st.write(f"**Buy here:** {product['offers'][0]['url']}")
                st.markdown("---")
        else:
            st.write("No products found matching your query.")

    except Exception as e:
        st.error(f"Error with Gemini API: {e}")
        st.write("Please ensure your GEMINI_API_KEY is correctly set.")
