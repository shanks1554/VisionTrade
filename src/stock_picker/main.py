import os
import warnings
import sys
from datetime import datetime
from dotenv import load_dotenv

from stock_picker.crew import StockPicker

# Load environment variables
load_dotenv()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the Indian stock research crew with user input.
    """
    print("=== Indian Stock Picker - NSE/BSE Financial Research System ===\n")
    
    # Get sector from user with Indian market sectors
    print("Popular Indian sectors:")
    print("• Banking & Financial Services")
    print("• Information Technology") 
    print("• Pharmaceuticals & Healthcare")
    print("• Fast Moving Consumer Goods (FMCG)")
    print("• Automotive & Auto Components")
    print("• Oil & Gas")
    print("• Metals & Mining")
    print("• Infrastructure & Real Estate")
    print("• Telecommunications")
    print("• Chemical & Petrochemicals")
    
    sector = input("\nEnter the Indian sector you want to analyze: ").strip()
    
    if not sector:
        print("No sector provided. Using default: Information Technology")
        sector = "Information Technology"
    
    print(f"\n🇮🇳 Starting Indian market analysis for sector: {sector}")
    print(f"📅 Analysis date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} IST")
    print(f"🏛️ Exchanges: NSE & BSE")
    print(f"💱 Currency: INR")
    print("-" * 60)
    
    inputs = {
        'sector': sector,
        "current_date": str(datetime.now())
    }

    try:
        # Debug: Print API key status
        google_key = os.getenv('GOOGLE_API_KEY')
        serper_key = os.getenv('SERPER_API_KEY')
        
        print(f"🔑 API Keys Status:")
        print(f"   Google API Key: {'✅ Set' if google_key else '❌ Not found'}")
        print(f"   Serper API Key: {'✅ Set' if serper_key else '❌ Not found'}")
        print("-" * 60)
        
        # Check if required API keys are set
        if not google_key:
            print("❌ Error: GOOGLE_API_KEY not found.")
            print("Please set at Google API key in your .env file.")
            return
            
        if not serper_key:
            print("❌ Error: SERPER_API_KEY not found in environment variables.")
            print("Please set your Serper API key for web search functionality.")
            return
        
        result = StockPicker().crew().kickoff(inputs=inputs)
        
        print("\n\n" + "="*25 + " Final Investment Decision " + "="*25 + "\n")
        print(result.raw)
        
        print(f"\n📊 Analysis completed for Indian {sector} sector")
        print("💡 Note: This is for informational purposes only. Please consult with a financial advisor before investing.")
        
    except Exception as e:
        print(f"❌ Error occurred during analysis: {str(e)}")
        print("Please try again or contact support.")

if __name__ == '__main__':
    run()