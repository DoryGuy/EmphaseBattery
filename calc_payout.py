#! /bin/python3

# pylint: disable=invalid-name,line-too-long

""" Calculate savings for investing in a home battery system
    Author: G.W. Powell
    Date: August 6, 2026
    copyright: All rights retained. No AI or LLM data scraping allowed.

    Assumption is that your solar array can provide both enough electricity to fully charge your battery
    and provide normal kw for the 4hrs that SDG&E sells power at super off peak rates ie 10am to 2pm.
    And that you use less than the full amount of your battery during peak hours ie 4pm to 9pm such that
    you can sell the excess back to the grid or would have had to buy it at peak rates.

    This also calculates the opportunity cost of not investing the cost of the battery and instead getting
    a safe steady return.
"""


winter_peak_rate_default = 0.15409 # dollars per kw
winter_peak_rate = float(input(f"Enter winter peak rate (default ${winter_peak_rate_default}kw): ").strip() or
                     winter_peak_rate_default)
winter_super_off_peak_rate_default = 0.03469
winter_super_off_peak_rate = float(input(f"Enter winter super off peak rate (default ${winter_super_off_peak_rate_default}kw): ").strip() or
                               winter_super_off_peak_rate_default)
# The cost of charging the battery vs using the solar array mid day at super off peak rates.
winter_effective_rate = winter_peak_rate - winter_super_off_peak_rate
battery_max_output_default = 10 # kw
battery_max_output = float(input(f"Enter total max kw that your battery can supply during peak hours (default {battery_max_output_default}kw) ").strip() or
                       battery_max_output_default)

num_days_at_winter_rates = 222 # Nov 1 thru May 31

summer_peak_rate_default = 0.41063 # dollars per kw
summer_peak_rate = float(input(f"Enter summer peak rate (default ${summer_peak_rate_default}kw): ").strip() or
                     summer_peak_rate_default)
summer_super_off_peak_rate_default = 0.04168
summer_super_off_peak_rate = float(input(f"Enter summer super off peak rate (default ${summer_super_off_peak_rate_default}kw): ").strip() or
                               summer_super_off_peak_rate_default)
# The cost of charging the battery vs using the solar array mid day.
summer_effective_rate = summer_peak_rate - summer_super_off_peak_rate
num_days_at_summer_rates = 153 # June 1 thru Oct 31

new_battery_value_default = 20000
new_battery_value = float(input(f"Enter new battery value (default {new_battery_value_default:.2f}) ").strip() or
                      new_battery_value_default)
new_battery_annual_depreciation_default = 0.10
new_battery_annual_depreciation = float(input(f"Enter new battery annual depreciation rate (default {new_battery_annual_depreciation_default:.2f}) ").strip() or
                      new_battery_annual_depreciation_default)
battery_install_cost_default = 10500.00  # dollars
battery_install_cost = float(input(f"Enter battery install cost (default {battery_install_cost_default:.2f}) ") or
                         battery_install_cost_default)

winter_savings = winter_effective_rate * battery_max_output * num_days_at_winter_rates
summer_savings = summer_effective_rate * battery_max_output * num_days_at_summer_rates

annual_possible_savings = winter_savings + summer_savings
annual_rate_increase_default = 0.086 # SDG&E proposed rate increase in 2028
annual_rate_increase = float(input(f"Enter annual rate increase (default {annual_rate_increase_default}) ").strip() or
                         annual_rate_increase_default)

hours_at_peak_rate = 4
winter_no_battery = winter_peak_rate * num_days_at_winter_rates * hours_at_peak_rate
summer_no_battery = summer_peak_rate * num_days_at_summer_rates * hours_at_peak_rate
annual_no_battery = winter_no_battery + summer_no_battery

total_possible_savings = 0.0
opportunity_cost = battery_install_cost
investment_annual_return_default = 0.05  # return on a safe investment
investment_annual_return = float(input(f"Enter annual investment return (default {investment_annual_return_default}) ").strip() or
                            investment_annual_return_default)

total_no_battery_cost = 0.0

for year in range (1,21,1):
    print(f"Year {year}:")
    print(f"    Possible savings: {annual_possible_savings:.2f}")
    total_possible_savings += annual_possible_savings
    annual_possible_savings *= 1 + annual_rate_increase
    opportunity_cost += opportunity_cost * investment_annual_return
    opportunity_return = opportunity_cost - battery_install_cost
    opportunity_cost = battery_install_cost + opportunity_return
    print(f"    Possible opportunity return {opportunity_return:.2f}")

    print(f"    No battery electrical cost for the year ${annual_no_battery:.2f} ")
    total_no_battery_cost += annual_no_battery
    annual_no_battery *= 1 + annual_rate_increase

    new_battery_value -= new_battery_value * new_battery_annual_depreciation
    print(f"    Battery value: {new_battery_value}")
    print("")

    if total_possible_savings >= battery_install_cost:
        break

print(f"Total possible savings {total_possible_savings:.2f}")

opportunity_cost -= battery_install_cost
print(f"Opportunity cost if you didn't buy a battery but invested the money. ${opportunity_cost:.2f}")

print(f"But total cost of electricty without a battery ${total_no_battery_cost:.2f}")
real_opportunity_cost = (opportunity_cost - total_no_battery_cost) - new_battery_value
if real_opportunity_cost > 0:
    print(f"You would be better off investing your money as you save ${real_opportunity_cost:.2f}")
else:
    real_opportunity_cost *= -1
    print(f"You should definitely buy a battery as you save ${real_opportunity_cost:.2f}")

if total_possible_savings < battery_install_cost:
    print("Your battery probably won't last long enough for you to recoup your costs.")
