#FINE3300A - Assignment #1
#Adam Jaffar - 219564350
#Description:
# - Design a class called MortgagePayment
# - Compute payment options (monthly, semi-monthly, bi-weekly, weekly, rapid bi-weekly, and rapid weekly)
# - Class should be initialized with:
#         - prevailing interest rate (Ex. quoted rate)
#         - amortization period
# - Create a method/function called payments that:
#         - takes the principle amount and returns a tuple of the periodic payments, in the respective order as above

# Formula for the PVA (Present Value of Annuity factor):
#         - r = periodic rate, n = periods 
#         - PVA(r, n) = (1 - (1 + r)^-n) / r

# Note to self: Fixed rate mortages are quoted as semi-annually compounded rates

# Refrences used: StackOverFlow, Google, Lecture Slides, The Python Book, AI for debugging

class MortgagePayment:
    def __init__(self, quoted_rate: float, amortization_yrs: int):
        # intialize with quoted intrest rate and the amoritization period
        self.quoted_rate = float(quoted_rate)
        self.amortization_yrs = int(amortization_yrs)

    # private functions
    def __effective_annual_rate(self):
        # convert semi-annual quoted rate into effective annual rate (EAR)
        semi_an_quoted = self.quoted_rate / 100.0
        ear = (1 + semi_an_quoted / 2) ** 2 - 1
        return ear
    
    def __periodic_rate(self, payments_per_year: int):
        # turn EAR into the per-period rate
        ear = self.__effective_annual_rate()
        r = (1 + ear) ** (1 / payments_per_year) - 1
        return r
    
    def __pva(self, r, n):
        # pv of an annuity factor
        return (1 - (1 + r) ** (-n)) / r
    
    def __payment(self, payments_per_year: int, principal: float):
        r = self.__periodic_rate(payments_per_year)
        n = payments_per_year * self.amortization_yrs
        pva = self.__pva(r, n)
        return float(principal) / pva
    
    # public functions for each pymt level
    def monthly_pymt(self, principal: float):
        return self.__payment(12, principal)
    
    def semi_monthly_pymt(self, principal: float):
        return self.__payment(24, principal)

    def bi_weekly_pymt(self, principal: float):
        return self.__payment(26, principal)

    def weekly_pymt(self, principal: float):
        return self.__payment(52, principal)

    def rapid_biweekly_pymt(self, principal: float):
        return self.__payment(12, principal) / 2.0

    def rapid_weekly_pymt(self, principal: float):
        return self.__payment(12, principal) / 4.0
    
    def payments(self, principal: float):
         # Making a tuple here in the way specified:
        # (monthly, semi-monthly, bi-weekly, weekly, rapid bi-weekly, rapid weekly)
        p = float(principal)
        return (
            self.monthly_pymt(p),
            self.semi_monthly_pymt(p),
            self.bi_weekly_pymt(p),
            self.weekly_pymt(p),
            self.rapid_biweekly_pymt(p),
            self.rapid_weekly_pymt(p),
        )


# Part 2: Exchange Rates
import csv

class ExchangeRates:
#Reads USD/CAD from a CSV and converts between USD and CAD
# Assumes the CSV has a column named USD/CAD

    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.usd_cad = None 
        self._load_usd_cad()

    def _load_usd_cad(self):
        # get the last USD/CAD rate from the csv
        with open(self.csv_file_path) as f:
            reader = csv.DictReader(f)
            last_value = None
            for row in reader:
                if row["USD/CAD"]:
                    last_value = float(row["USD/CAD"])
        self.usd_cad = last_value

    def convert(self, amount, from_currency, to_currency):
        #convert between USD and CAD using the rate
        amt = float(amount)
        rate = self.usd_cad  #1 USD = rate CAD

        if from_currency == "USD" and to_currency == "CAD":
            return amt * rate
        elif from_currency == "CAD" and to_currency == "USD":
            return amt / rate
        else:
            #same currency
            return amt


# terminal 

def __print_pymts_two_decimals(label, value):
    #formatting to 2 decimals
    print(f"{label}: ${value:.2f}")

def run_assignment1():
    #Part 1: Mortgage Payments
    print("Part 1: Mortgage Payments")
    principal = float(input("Enter mortgage principal (e.g., 3000000): ").strip())
    quoted_rate = float(input("Enter quoted annual rate % (e.g., 7.5): ").strip())
    amort_years = int(input("Enter amortization (years, e.g., 25): ").strip())

    mortgage = MortgagePayment(quoted_rate=quoted_rate, amortization_yrs=amort_years)
    monthly, semi_monthly, bi_wkly, wkly, rapid_bi_wkly, rapid_wkly = mortgage.payments(principal)

    print()
    __print_pymts_two_decimals("Monthly Payment", monthly)
    __print_pymts_two_decimals("Semi-monthly Payment", semi_monthly)
    __print_pymts_two_decimals("Bi-weekly Payment", bi_wkly)
    __print_pymts_two_decimals("Weekly Payment", wkly)
    __print_pymts_two_decimals("Rapid Bi-weekly Payment", rapid_bi_wkly)
    __print_pymts_two_decimals("Rapid Weekly Payment", rapid_wkly)

    #Part 2: Exchange Rates
    print("\nPart 2: Exchange Rates (USD to/from CAD) ")
    csv_path = input("Enter path to csv for exchange rate (Note: make sure there is a USD/CAD column): ").strip()
    amount = float(input("Enter amount to convert (e.g., 1000000): ").strip())
    #.upper() to make sure sure if even the user inputs lowercase 'cad', the program will still run as expected
    from_currency = input("From currency (USD or CAD): ").strip().upper()
    to_currency = input("To currency (USD or CAD): ").strip().upper()

    er = ExchangeRates(csv_path)
    converted = er.convert(amount, from_currency, to_currency)
    #making sure no matter if user does upper or lower case, the program can read the input properly
    print("\n")
    print(f"{amount:.2f} {from_currency.upper()} = {converted:.2f} {to_currency.upper()}\n")


# Run the program
run_assignment1()