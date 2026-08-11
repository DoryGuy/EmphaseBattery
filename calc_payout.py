#! /bin/python3

# pylint: disable=invalid-name,line-too-long,unused-argument

""" Calculate savings for investing in a home battery system
    Author: G.W. Powell
    Date: August 6, 2026
    copyright: All rights retained. No AI or LLM data scraping allowed.

    Assumption is that your solar array can provide both enough electricity to fully charge your battery
    and provide normal kw for the 4hrs that SDG&E sells power at super off peak rates ie 10am to 2pm.
    And that you use less than the full amount of your battery during peak hours ie 4pm to 9pm such that
    you can sell the excess back to the grid or would have had to buy it at peak rates.

    This also calculates the opportunity cost of not investing the cost of the battery and instead getting
    a safe steady return. (You still have to pay for the electricity you use)

    This simulation is for educational purposes only and does not imply actual savings. YMMV
"""

import signal
import sys

def ctrl_c_handler(signum, frame):
    """Function executed immediately when Ctrl+C is pressed."""
    print("\nCTRL C Trap activated! Exiting safely...")
    sys.exit(0)

# Register the handler function for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, ctrl_c_handler)


winter_peak_delivery_rate_default = 0.19990   # dollars per kw
winter_peak_delivery_rate = float(input(f"Enter winter peak delivery rate (default ${winter_peak_delivery_rate_default:.5f}): ").strip() or \
                             winter_peak_delivery_rate_default)
winter_peak_rate_default = 0.15409 # dollars per kw
winter_peak_rate = float(input(f"Enter winter peak rate (default ${winter_peak_rate_default:.5f}kw): ").strip() or \
                     winter_peak_rate_default)
winter_peak_rate += winter_peak_delivery_rate
winter_super_off_peak_rate_default = 0.03469
winter_super_off_peak_rate = float(input(f"Enter winter super off peak rate (default ${winter_super_off_peak_rate_default:.5f}kw): ").strip() or \
                               winter_super_off_peak_rate_default)
# The cost of charging the battery vs using the solar array mid day at super off peak rates.
winter_effective_rate = winter_peak_rate - winter_super_off_peak_rate
battery_max_output_default = 10.0 # kw
battery_max_output = float(input(f"Enter total max kw that your battery can supply during peak hours (default {battery_max_output_default:.2f}kw) ").strip() or \
                       battery_max_output_default)
# How long does it take for the battery to degrade to 70%
# Currently Enphase batteries are warrantied to have 70 at 15 years (end of warrenty)
battery_degrade_years_default = 15
battery_degrade_years = float(input(f"Enter number of years that it will take the battery to degrade to 70% (default {battery_degrade_years_default:.1f}): ") or \
                          battery_degrade_years_default)
battery_annual_degrade_amount = (battery_max_output * 0.30) / battery_degrade_years

num_days_at_winter_rates = 222 # Nov 1 thru May 31

summer_peak_delivery_rate_default = 0.25791
summer_peak_delivery_rate = float(input(f"Enter summer peak delivery rate (default ${summer_peak_delivery_rate_default:.5f}): ").strip() or \
                             summer_peak_delivery_rate_default)
summer_peak_rate_default = 0.41063 # dollars per kw
summer_peak_rate = float(input(f"Enter summer peak rate (default ${summer_peak_rate_default:.5f}kw): ").strip() or \
                     summer_peak_rate_default)
summer_super_off_peak_rate_default = 0.04168
summer_super_off_peak_rate = float(input(f"Enter summer super off peak rate (default ${summer_super_off_peak_rate_default:.5f}kw): ").strip() or \
                               summer_super_off_peak_rate_default)
summer_peak_rate += summer_peak_delivery_rate
# The cost of charging the battery vs using the solar array mid day.
summer_effective_rate = summer_peak_rate - summer_super_off_peak_rate
num_days_at_summer_rates = 153 # June 1 thru Oct 31

depreciated_battery_system_value_default = 20000
depreciated_battery_system_value = float(input(f"Enter new battery system value (default {depreciated_battery_system_value_default:.2f}) ").strip() or \
                      depreciated_battery_system_value_default)
battery_system_lifetime_default = 15 # 15 year depreciation
battery_system_lifetime = int(input(f"Enter battery warranty in years (default {battery_system_lifetime_default}) ").strip() or \
                      battery_system_lifetime_default)
battery_system_install_cost_default = 10500.00  # dollars
battery_system_install_cost = float(input(f"Enter your battery installation cost (default {battery_system_install_cost_default:.2f}) ") or \
                         battery_system_install_cost_default)

battery_annual_depreciation_amount = depreciated_battery_system_value / battery_system_lifetime

annual_electricity_rate_increase_default = 0.086 # SDG&E proposed rate increase in 2028
annual_electricity_rate_increase = float(input(f"Enter annual rate increase (default {annual_electricity_rate_increase_default}) ").strip() or \
                                    annual_electricity_rate_increase_default)

years_between_rate_increases_default = 2
years_between_rate_increases = int( input(f"Enter number of years between rate increases (default {years_between_rate_increases_default}): ").strip() or \
                                 years_between_rate_increases_default)

hours_at_peak_rate = 4
winter_no_battery_cost = winter_peak_rate * num_days_at_winter_rates * hours_at_peak_rate
summer_no_battery_cost = summer_peak_rate * num_days_at_summer_rates * hours_at_peak_rate
annual_no_battery_cost = winter_no_battery_cost + summer_no_battery_cost

total_possible_electricity_cost_savings = 0.0
opportunity_cost_fund = battery_system_install_cost
investment_annual_return_default = 0.05  # return on a safe investment
investment_annual_return = float(input(f"Enter annual investment return (default {investment_annual_return_default}) ").strip() or \
                            investment_annual_return_default)

total_electrical_savings_investment = 0.0 # Money you make if you invest your annual electrical cost savings

total_no_battery_electricity_costs = 0.0
total_opportunity_return = 0.0
break_even_year = -1   # year that your investment pays off

years_to_run_simulation_for_default = 20
years_to_run_simulation = int( input(f"Enter years to run simulation for (default {years_to_run_simulation_for_default}: ").strip() or \
                            years_to_run_simulation_for_default)

years_to_run_simulation += 1  # we start at year 1 so the loop needs one more iteration.
for year in range (1,years_to_run_simulation,1):

    winter_savings = winter_effective_rate * battery_max_output * num_days_at_winter_rates
    summer_savings = summer_effective_rate * battery_max_output * num_days_at_summer_rates
    annual_possible_electricity_cost_savings = winter_savings + summer_savings

    print(f"End of Year {year}:")
    print(f"    Battery capacity: {battery_max_output:.1f}kw (est)")
    print(f"    Possible this year's electricity cost savings: ${annual_possible_electricity_cost_savings:.2f}")
    total_possible_electricity_cost_savings += annual_possible_electricity_cost_savings
    print(f"    Possible total electricity cost savings: ${total_possible_electricity_cost_savings:.2f}")
    if year % years_between_rate_increases == 0:
        winter_effective_rate *= 1 + annual_electricity_rate_increase
        summer_effective_rate *= 1 + annual_electricity_rate_increase

    opportunity_return = opportunity_cost_fund * investment_annual_return
    opportunity_cost_fund += opportunity_return
    total_opportunity_return += opportunity_return
    opportunity_cost_fund -= annual_no_battery_cost      # You have to pay for electricity that you used
    opportunity_cost_fund = max( opportunity_cost_fund, 0.0)
    if opportunity_return > 0:
        print(f"    Possible opportunity return ${opportunity_return:.2f}")
    else:
        print("    You are no longer earning anything from your opportunity fund.")

    print(f"    No battery additional electrical cost for the year ${annual_no_battery_cost:.2f} ")
    total_no_battery_electricity_costs += annual_no_battery_cost
    if year % years_between_rate_increases == 0:
        annual_no_battery_cost *= 1 + annual_electricity_rate_increase

    depreciated_battery_system_value -= battery_annual_depreciation_amount
    depreciated_battery_system_value = max( depreciated_battery_system_value,  0.0)
    print(f"    Current Battery value: ${depreciated_battery_system_value:.2f}")

    total_electrical_savings_investment += total_possible_electricity_cost_savings * investment_annual_return
    print(f"    electrical savings earnings if invested ${total_electrical_savings_investment:.2f}")

    # Enphase on their website says that the battery will degrade to 70% by year 15 but does not say how much
    # more the battery will degrade. So for the moment I'm just doing the initial degrade.
    if year < 16:
        battery_max_output -= battery_annual_degrade_amount

    if break_even_year == -1 and \
        (total_possible_electricity_cost_savings + total_electrical_savings_investment) >= \
          (battery_system_install_cost + total_opportunity_return):
        break_even_year = year

print("")
if break_even_year != 0:
    print(f"Your break even year is year {break_even_year}")
    print(" This is the year that your cost of installation plus the opportunity lost cost is less than")
    print(" the savings on your electrical bill plus the investment savings from those annual savings.")
print(f"Total possible electricity cost savings ${total_possible_electricity_cost_savings:.2f}")
total_possible_electricity_cost_savings += total_electrical_savings_investment
print(f"Total possible savings if annual electrical savings are invested: ${total_possible_electricity_cost_savings:.2f}")

investment_annual_return_percentage = investment_annual_return * 100
print(f"Total Opportunity return if you didn't buy a battery but invested the money {investment_annual_return_percentage:.2f}% ${total_opportunity_return:.2f}")

print(f"Total cost of electricity without a battery ${total_no_battery_electricity_costs:.2f}")

assets_with_battery_system = depreciated_battery_system_value + total_possible_electricity_cost_savings
assets_with_battery_system -= battery_system_install_cost
print(f"Assets with a battery ${assets_with_battery_system:.2f}")
assets_without_battery_system = (battery_system_install_cost + total_opportunity_return) - total_no_battery_electricity_costs
print(f"Assets without a battery ${assets_without_battery_system:.2f}")

if assets_with_battery_system > assets_without_battery_system:
    increased_value = assets_with_battery_system - assets_without_battery_system
    print(f"You should definitely buy a battery as your assets increased by ${increased_value:.2f}")
else:
    losses_value = assets_without_battery_system - assets_with_battery_system
    print(f"You would be better off investing your money as you lost ${losses_value:.2f}")
    print("Your battery probably won't last long enough for you to recoup your costs.")
