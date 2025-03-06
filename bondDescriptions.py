# Import Libraries
import pandas as pd
import re
import numpy as np
from datetime import datetime

reference_year = datetime.now().year - 1

def categorize_bonds(df):
    
    # Ensure column name is standardized
    if 'Asset Name' in df.columns:
        bond_column = 'Asset Name'
    else:
        # Take the first column if 'Asset Name' is not found
        bond_column = df.columns[0]
    
    # Create a copy to avoid modifying the view
    df_categorized = df.copy()
    
    # Add categorization columns
    df_categorized['Issuer'] = df_categorized[bond_column].apply(extract_issuer)
    df_categorized['Sector'] = df_categorized['Issuer'].apply(identify_sector)
    df_categorized['Maturity_Year'] = df_categorized[bond_column].apply(extract_maturity_year)
    df_categorized['Bucket'] = df_categorized.apply(
        lambda row: maturity_bucket(row['Maturity_Year']), 
        axis=1
    )
        
    return df_categorized

def extract_issuer(bond_name):
    # Handle null values
    if pd.isna(bond_name):
        return "OTHER"
    
    # Convert to string if not already
    bond_name = str(bond_name)
    
    # Patterns to match issuers
    cash_patterns = [
        r'South African Rand',
        r'ZAR',
        r'Cash',
        r'MONEY MARKET'
    ]

    # Patterns to match issuers
    namibia_patterns = [
        r'NAMIBIA',
    ]
    
    government_patterns = [
        r'SOUTH AFRICA, REPUBLIC',
        r'REPUBLIC OF SOUTH',
        r'(?:^|\s)R\d{3}\b',  # R followed by 3 digits for SA govt bonds
        r'(?:^|\s)I2\d{3}\b',  # I2 followed by 3 digits for inflation-linked bonds
        r'GOVERNMENT',
        r'TREASURY',
        r'South Africa R\d+'
    ]
    
    bank_patterns = [
        r'STANDARD BANK',
        r'ABSA',
        r'NEDBANK',
        r'FIRSTRAND',
        r'INVESTEC',
        r'CAPITEC',
        r'AFRICAN BANK'
    ]

    insurance_patterns = [
        r'SANLAM',
        r'OLD MUTUAL',
        r'MOMENTUM',
        r'LIBERTY',
        r'DISCOVERY',
        r'SANTAM'
    ]
    
    municipal_patterns = [
        r'THEKWINI',
        r'CITY OF CAPE TOWN',
        r'TSHWANE',
        r'JOHANNESBURG',
        r'EKURHULENI',
        r'MUNICIPALITY',
        r'MUNICIPAL',
        r'METRO'
    ]

    soe_patterns = [
        r'ESKOM',
        r'NATIONAL ROADS AGENCY',
        r'RAND WATER',
        r'TRANSNET',
        r'SANRAL',
        r'DEVELOPMENT BANK OF',
        r'LAND BANK',
        r'AIRPORTS CO'
    ]    

    # Check for cash
    for pattern in cash_patterns:
        if re.search(pattern, bond_name, re.IGNORECASE):
            return 'CASH'
    
    # Check for government bonds
    for pattern in namibia_patterns:
        if re.search(pattern, bond_name, re.IGNORECASE):
            return 'NAM GOVERNMENT'

    # Check for government bonds
    for pattern in government_patterns:
        if re.search(pattern, bond_name, re.IGNORECASE):
            return 'SA GOVERNMENT'
    
    # Check for bank bonds
    for pattern in bank_patterns:
        if re.search(pattern, bond_name, re.IGNORECASE):
            # Determine which bank matched
            if re.search(r'STANDARD BANK', bond_name, re.IGNORECASE):
                return 'STANDARD BANK'
            elif re.search(r'ABSA', bond_name, re.IGNORECASE):
                return 'ABSA'
            elif re.search(r'NEDBANK', bond_name, re.IGNORECASE):
                return 'NEDBANK'
            elif re.search(r'FIRSTRAND', bond_name, re.IGNORECASE):
                return 'FIRSTRAND'
            elif re.search(r'INVESTEC', bond_name, re.IGNORECASE):
                return 'INVESTEC'
            elif re.search(r'CAPITEC', bond_name, re.IGNORECASE):
                return 'CAPITEC'
            elif re.search(r'AFRICAN BANK', bond_name, re.IGNORECASE):
                return 'AFRICAN BANK'
    
    # Check for insurance bonds
    for pattern in insurance_patterns:
        if re.search(pattern, bond_name, re.IGNORECASE):
            if re.search(r'SANLAM', bond_name, re.IGNORECASE):
                return 'SANLAM'
            elif re.search(r'OLD MUTUAL', bond_name, re.IGNORECASE):
                return 'OLD MUTUAL'
            elif re.search(r'MOMENTUM', bond_name, re.IGNORECASE):
                return 'MOMENTUM'
            elif re.search(r'LIBERTY', bond_name, re.IGNORECASE):
                return 'LIBERTY'
            elif re.search(r'DISCOVERY', bond_name, re.IGNORECASE):
                return 'DISCOVERY'
            elif re.search(r'SANTAM', bond_name, re.IGNORECASE):
                return 'SANTAM'
    
    # Check for municipal bonds
    for pattern in municipal_patterns:
        if re.search(pattern, bond_name, re.IGNORECASE):
            if re.search(r'THEKWINI', bond_name, re.IGNORECASE):
                return 'ETHEKWINI MUNICIPALITY'
            elif re.search(r'CITY OF CAPE TOWN', bond_name, re.IGNORECASE):
                return 'CITY OF CAPE TOWN'
            elif re.search(r'TSHWANE', bond_name, re.IGNORECASE):
                return 'CITY OF TSHWANE'
            elif re.search(r'JOHANNESBURG', bond_name, re.IGNORECASE):
                return 'CITY OF JOHANNESBURG'
            elif re.search(r'EKURHULENI', bond_name, re.IGNORECASE):
                return 'EKURHULENI METRO'
            else:
                return 'MUNICIPAL'
            
    # Check for SOE bonds
    for pattern in soe_patterns:
        if re.search(pattern, bond_name, re.IGNORECASE):
            if re.search(r'ESKOM', bond_name, re.IGNORECASE):
                return 'ESKOM'
            elif re.search(r'NATIONAL ROADS|SANRAL', bond_name, re.IGNORECASE):
                return 'SANRAL'
            elif re.search(r'RAND WATER', bond_name, re.IGNORECASE):
                return 'RAND WATER'
            elif re.search(r'TRANSNET', bond_name, re.IGNORECASE):
                return 'TRANSNET'
            elif re.search(r'DEVELOPMENT BANK', bond_name, re.IGNORECASE):
                return 'DEVELOPMENT BANK OF SA'
            elif re.search(r'LAND BANK', bond_name, re.IGNORECASE):
                return 'LAND BANK'
            elif re.search(r'AIRPORTS CO', bond_name, re.IGNORECASE):
                return 'AIRPORTS COMPANY SA'
            else:
                return 'SOE'
            
    # Check for securitization vehicles
    if re.search(r'THEKWINI FUND|NQABA|SA TAXI', bond_name, re.IGNORECASE):
        if re.search(r'THEKWINI FUND', bond_name, re.IGNORECASE):
            return 'THEKWINI FUND'
        elif re.search(r'NQABA', bond_name, re.IGNORECASE):
            return 'NQABA FINANCE'
        elif re.search(r'SA TAXI', bond_name, re.IGNORECASE):
            return 'SA TAXI'
        else:
            return 'SECURITIZATION'
    
    # Additional checks for specific corporates
    if re.search(r'MOBILE TELEPHONE NETWORKS|VODACOM|SASOL|GROWTHPOINT|REDEFINE|SHOPRITE|TELKOM|TOYOTA|NORTHAM PLATINUM| NINETY ONE', bond_name, re.IGNORECASE):
        if re.search(r'MOBILE TELEPHONE NETWORKS', bond_name, re.IGNORECASE):
            return 'MTN'
        elif re.search(r'VODACOM', bond_name, re.IGNORECASE):
            return 'VODACOM'
        elif re.search(r'SASOL', bond_name, re.IGNORECASE):
            return 'SASOL'
        elif re.search(r'GROWTHPOINT', bond_name, re.IGNORECASE):
            return 'GROWTHPOINT'
        elif re.search(r'REDEFINE', bond_name, re.IGNORECASE):
            return 'REDEFINE'
        elif re.search(r'SHOPRITE', bond_name, re.IGNORECASE):
            return 'SHOPRITE'
        elif re.search(r'TELKOM', bond_name, re.IGNORECASE):
            return 'TELKOM'
        elif re.search(r'TOYOTA', bond_name, re.IGNORECASE):
            return 'TOYOTA'
        elif re.search(r'NORTHAM PLATINUM', bond_name, re.IGNORECASE):
            return 'NORTHAM PLATINUM'
        elif re.search(r'NINETY ONE', bond_name, re.IGNORECASE):
            return 'NINETY ONE'
    
    # If no patterns match, try to extract a reasonable issuer name
    # Look for words that are all caps and might be an issuer
    caps_words = re.findall(r'([A-Z]{2,}(?:\s[A-Z]{2,})*)', bond_name)
    if caps_words:
        # Filter out common non-issuer terms
        filtered_words = [word for word in caps_words if not re.search(r'LIMITED|LTD|FRN|FIXED|FLOATING|BOND|NOTE', word, re.IGNORECASE)]
        if filtered_words:
            return filtered_words[0]
    
    return "OTHER"


def extract_maturity_year(bond_name, reference_year=datetime.now().year-1):
    if pd.isna(bond_name):
        return 0
        
    # Convert to string if not already
    bond_name = str(bond_name)
    
    # Pattern 1: Look for MM/YY format (e.g., 08/54)
    # This pattern should be checked first to capture the problematic case
    mm_yy_match = re.search(r'(\d{2})/(\d{2})', bond_name)
    if mm_yy_match:
        year = int(mm_yy_match.group(2)) 
        # Assume years less than 50 are in the 21st century, others in the 20th
        if year < 50:
            maturity_years = 2000 + year - reference_year
        else:
            maturity_years = 1900 + year - reference_year
        
        # Return 0 if matured or negative
        return max(0, maturity_years)
    
    # Pattern 2: Look for full date formats like "20410228" (YYYYMMDD)
    date_match = re.search(r'20(\d{2})(\d{2})(\d{2})', bond_name)
    if date_match:
        year = int("20" + date_match.group(1))
        maturity_years = year - reference_year
        return max(0, maturity_years)
    
    # Pattern 3: Look for spelled out month formats like "08 MAR 26", "MAR 26", "14 DEC 28"
    month_pattern = r'(?:JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)'
    month_year_match = re.search(r'(?:\d{1,2}\s+)?(' + month_pattern + r')\s+(\d{2})\b', bond_name, re.IGNORECASE)

    if month_year_match:
        # month = month_year_match.group(1)  # This captures the month name
        year = int(month_year_match.group(2))  # This captures the year
        
        # Now you can use both month and year in your logic
        if year < 50:
            maturity_years = 2000 + year - reference_year
        else:
            maturity_years = 1900 + year - reference_year
        return max(0, maturity_years)
    
    # Pattern 4: Look for standalone year format (20XX)
    standalone_year_match = re.search(r'\b20(\d{2})\b', bond_name)
    if standalone_year_match:
        year = int("20" + standalone_year_match.group(1))
        maturity_years = year - reference_year
        return max(0, maturity_years)
    
    # Pattern 5: Alternative date format "DD.MM.YYYY" or "MM.DD.YYYY"
    alt_date_match = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{4})', bond_name)
    if alt_date_match:
        year = int(alt_date_match.group(3))
        maturity_years = year - reference_year
        return max(0, maturity_years)
    
    # Pattern 6: Look for year mentions in formats like "DUE 2028"
    due_match = re.search(r'DUE\s+20(\d{2})', bond_name, re.IGNORECASE)
    if due_match:
        year = int("20" + due_match.group(1))
        maturity_years = year - reference_year
        return max(0, maturity_years)
    
    # Pattern 7: Look for perpetual bonds
    if re.search(r'PERP|PERPETUAL|20991231', bond_name, re.IGNORECASE):
        return 99  # Conventional value for perpetual bonds
    
    return 0


def identify_sector(issuer):
    """Identify the economic sector based on the issuer"""
    issuer_upper = issuer.upper()
    
    if 'CASH' in issuer_upper:
        return 'Cash'

    if 'GOVERNMENT' in issuer_upper:
        return 'Sovereign'
    
    if 'NINETY ONE' in issuer_upper:
        return 'Corp Bond'
    
    if any(bank in issuer_upper for bank in ['STANDARD BANK', 'ABSA', 'NEDBANK', 'FIRSTRAND', 'INVESTEC']):
        return 'Banking'
    
    if any(bank in issuer_upper for bank in ['LIBERTY', 'SANTAM', 'SANLAM', 'OLD MUTUAL', 'MOMENTUM']):
        return 'Insurance'
    
    if 'REDEFINE' in issuer_upper or 'GROWTHPOINT' in issuer_upper:
        return 'Real Estate'
    
    if any(bank in issuer_upper for bank in ['ESKOM', 'SANRAL', 'RAND WATER', 'TRANSNET']):
        return 'SOE'
    
    if any(bank in issuer_upper for bank in ['ETHEKWINI', 'CITY OF TSHWANE', 'CAPE TOWN']):
        return 'Municipal'
        
    return 'Credit'

def maturity_bucket(maturity_year):
    
    # Default to bucket
    bucket = "0-3 years"
    
    # Maturity Bucket
    if not pd.isna(maturity_year):
        # time_to_maturity = maturity_year - current_year
        time_to_maturity = maturity_year
        
        if time_to_maturity < 3:
            bucket = "0-3 years"
        elif time_to_maturity < 7:
            bucket = "3-7 years"
        elif time_to_maturity < 12:
            bucket = "7-12 years"
        else:
            bucket = "12+ years"
    
    return bucket
