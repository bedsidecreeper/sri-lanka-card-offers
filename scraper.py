import json
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Centralized output structure
offers_data = []

def generate_hashtags(title, bank_name, category, card_types):
    """Generates hashtag list for filtering on Android."""
    tags = set()
    
    # 1. Bank Tag
    tags.add(f"#{bank_name.replace(' ', '')}")
    
    # 2. Category Tag
    tags.add(f"#{category.replace(' ', '')}")
    
    # 3. Card Types (Credit/Debit)
    for c_type in card_types:
        tags.add(f"#{c_type}")

    # 4. Extract Discount Percentage dynamically using Regex (e.g., 20% -> #20PercentOff)
    discount_match = re.search(r'(\d+)%', title)
    if discount_match:
        tags.add(f"#{discount_match.group(1)}PercentOff")

    return list(tags)

def scrape_sampath_bank():
    print("Scraping Sampath Bank...")
    url = "https://www.sampath.lk/sampath-cards/credit-card-offer?firstTab=Other"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Scrape promotion cards (matches Sampath layout)
        cards = soup.select('.offer-card') or soup.find_all('div', class_=re.compile(r'card|offer'))
        
        for idx, card in enumerate(cards[:15]): # Limit to first 15 for demo
            title_el = card.find(['h3', 'h4', 'h5', 'p'])
            img_el = card.find('img')
            
            if title_el:
                title = title_el.text.strip()
                img_src = img_el['src'] if img_el and 'src' in img_el.attrs else ""
                if img_src and not img_src.startswith('http'):
                    img_src = f"https://www.sampath.lk{img_src}"

                hashtags = generate_hashtags(title, "SampathBank", "Hotels & Dining", ["CreditCard", "DebitCard"])
                
                offers_data.append({
                    "id": f"sampath_{idx}",
                    "bank_id": "sampath",
                    "bank_name": "Sampath Bank",
                    "title": title,
                    "merchant_name": title.split(' at ')[-1] if ' at ' in title else "Partner Merchant",
                    "category": "Hotels & Dining",
                    "thumbnail_url": img_src or "https://via.placeholder.com/300x150.png?text=Sampath+Bank",
                    "start_date": "2026-01-01",
                    "end_date": "2026-12-31",
                    "applicable_card_ids": ["sampath_mastercard", "sampath_visa"],
                    "hashtags": hashtags,
                    "full_details": f"Detailed terms for {title}. Valid for all Sampath Credit & Debit Cards."
                })
    except Exception as e:
        print(f"Error scraping Sampath Bank: {e}")

# Sample fallback generator for demonstration/testing
def populate_sample_sri_lankan_offers():
    print("Injecting fallback/mock offer data for testing...")
    sample_offers = [
        {
            "id": "combank_01",
            "bank_id": "combank",
            "bank_name": "Commercial Bank",
            "title": "25% Off Fresh Produce at Cargills Food City",
            "merchant_name": "Cargills Food City",
            "category": "Supermarkets",
            "thumbnail_url": "https://www.combank.lk/uploads/promotions/cargills-promo.jpg",
            "start_date": "2026-10-01",
            "end_date": "2026-10-31",
            "applicable_card_ids": ["combank_visa_credit", "combank_mastercard_credit"],
            "hashtags": ["#CommercialBank", "#Supermarkets", "#CreditCard", "#25PercentOff"],
            "full_details": "Enjoy 25% discount on fresh vegetables, fruits, and seafood at Cargills Food City outlets every Friday."
        },
        {
            "id": "hnb_01",
            "bank_id": "hnb",
            "bank_name": "Hatton National Bank",
            "title": "40% Off Room Bookings at Jetwing Hotels",
            "merchant_name": "Jetwing Hotels",
            "category": "Hotels",
            "thumbnail_url": "https://www.hnb.net/images/jetwing-promo.jpg",
            "start_date": "2026-10-01",
            "end_date": "2026-11-15",
            "applicable_card_ids": ["hnb_platinum_credit", "hnb_signature"],
            "hashtags": ["#HNB", "#Hotels", "#CreditCard", "#40PercentOff", "#Vacation"],
            "full_details": "Book your escape with HNB Platinum or Signature Credit Cards and receive a 40% discount on HB/FB rates."
        }
    ]
    offers_data.extend(sample_offers)

if __name__ == "__main__":
    scrape_sampath_bank()
    populate_sample_sri_lankan_offers()
    
    # Export to offers.json
    with open("offers.json", "w", encoding="utf-8") as f:
        json.dump(offers_data, f, indent=4, ensure_ascii=False)
        
    print(f"Successfully exported {len(offers_data)} offers to offers.json")
