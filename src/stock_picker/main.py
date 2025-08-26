import os
import warnings
import sys
from datetime import datetime

from stock_picker.crew import StockPicker

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the research crew with user input.
    """
    print("=== Stock Picker - Financial Research System ===\n")
    
    # Get sector from user
    print("Popular sectors: Technology, Energy, Healthcare, Finance, Consumer Goods")
    sector = input("Enter the sector you want to analyze: ").strip()
    
    if not sector:
        print("No sector provided. Using default: Energy")
        sector = "Energy"
    
    print(f"\n🔍 Starting analysis for sector: {sector}")
    print(f"📅 Analysis date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    inputs = {
        'sector': sector,
        "current_date": str(datetime.now())
    }

    result = StockPicker().crew().kickoff(inputs=inputs)

    print("\n\n" + "="*20 + " Final Decision " + "="*20 + "\n")
    print(result.raw)

if __name__ == '__main__':
    run()