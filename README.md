A python program to help decide whether to install a battery to time shift the costs of electricity in the SDG&E system.
Any cost savings are theoretical and are not guaranteed, YMMV.

This simulation allows you to figure the depreciated value of the battery over the life of the warranty. It currently
does not degrade the capacity of the battery over time. (Which in real life will occur) And it assumes that you will
invest the annual electrical cost savings in a fund and not buy more avocado toast and lattes.

This program assumes that your solar system can provide both enough electricity to fully charge your battery
and provide normal kws of energy for the 4 hours that SDG&E sells power at super off peak rates ie 10am to 2pm M->F
and 12am to 2pm Sat/Sun.  And that you use less than the full amount of your battery during peak hours ie 4pm to 9pm daily that 
you can sell the excess power back to SDG&E or would have had to buy it at peak rates.

This program also calculates the opportunity cost of not investing in a battery and instead getting a safe steady
return. (You still have to pay for the electricity that you use). And it factors in the return on your annual savings
of electricity not purchased but instead invested.

I am not an investment councilor or financial advisor. I wrote this program to help me make the right decision for me. I
am updating it as I understand better the true costs and savings.

I wrote it in Python version 3, because it's easy to modify and I don't really care about fancy UI's or graphics. You can get that
from your Solar battery salesmen. The variable names are verbose so that you can read the code and understand the logic
without being an expert Python programmer.
