annual_salary = float(input("Enter your annual salary: "))
portion_saved = float(input("Enter the percent of your salary to save, as decimal: "))
total_cost = float(input("Enter the cost of your dream house: "))
semi_annual_raise = float(input("Enter the semi-annual raise, as decimal: "))

current_savings = 0
portion_down_payment = 0.25
#current_savings = float(input("Enter current savings: "))
r = 0.04
#money = 0
months = 0
month_salary = annual_salary/12
#month_savings = month_salary * portion_saved

down_payment = portion_down_payment * total_cost

while (current_savings < down_payment):
    month_savings = month_salary * portion_saved
    current_savings += (current_savings*r)/12
    current_savings += month_savings
    months += 1
    if (months % 6 == 0):
        month_salary += month_salary * semi_annual_raise 

print("It will take", months,"months")
    
